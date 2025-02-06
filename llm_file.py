import re, json
import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from init import TAVILY_API_KEY, tavily_url

# Define your desired data structure.
class llm_status(BaseModel):
    status: str = Field(
        description="""Answer to weather this question can directly be answer by model.....Always 'YES' or 'NO'

IF the user message can be answered based on the above prompt, chat history and your knowledge, then 'YES'.
ELSE, 'NO'.
""")
    answer: str = Field(
        description="""Required output of the model correnponding to if the question can we answered or not by the model

IF 'status': 'YES', then answer the user message based on below rules

Response has to be :
- Answer has to be in the HINDI language. Even the numbers have to be in hindi text Eg: 13/१३ has to be written as तेरह.
- HAS TO BE IN MARKDOWN FORMAT
- DO NOT REPEAT THE PROMPT
- CLEAR and INFORMATIVE
- If user asks a DIRECT and SIMPLE question, then give CONCISE and to the point answer.
- If user asks a BROAD and OPEN ENDED question, then you can give a longer and COMPREHENSIVE answer.
- Directly address the user's query or statement.
- If the output is short, then give PLAIN TEXT OUTPUT.
- If the output is long and more than 1 paragraph, then give a well ORGANISED OUTPUT with proper headings numerical pointers.
- Your tone should always be PROFESSIONAL and ARTICULATE, yet FRIENDLY and HUMAN-LIKE.

IF 'status': 'NO', then provide a crisp formatted question in english based on the chat history and user message which can be searched on web to get the answer. Only provide the question, no explaination needed.
""")

def get_answer_status(llm, user_query, history, date_time):
    parser = JsonOutputParser(pydantic_object = llm_status)
    prompt = PromptTemplate(
        template = """
        You are highly intelligent and dedicated **Feminine** AI Assistant created by Aditya Patil.
        Your primary function is to assist users by providing accurate information, answering questions, and engaging in meaningful conversation.
        You are equipped with a vast knowledge base and are capable of understanding complex topics.

        **Chat History:**
        {history}

        **User Message:**
        {query}

        IF the user message can be answered based on the above prompt, chat history and your knowledge, then output must look like:
        {yes}

        ELSE, provide a question based on the above prompt, chat history and user message which can be searched on web to get the answer.:
        {no}

        Answer the user query.\n{format_instructions}

        IF user's question is related to current/latest/recent event, they mean at date and time : {date_time}

        """,
        input_variables = ["query", "history", "yes", "no", "date_time"],
        partial_variables = {"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm
    unparsed_output = chain.invoke({"query": user_query, "history": history,
                'yes': '{"status" : "YES", answer : "Whatever the actual answer is.... "}',
                'no': '{"status" : "NO", answer : "Whatever the new fomatted question is.... "}',
                'date_time': date_time})
    unparsed_output = unparsed_output.content
    json_pattern = r'\{(?:[^{}]*\{[^{}]*\}[^{}]*|[^{}]*)*\}'
    unparsed_output = re.findall(json_pattern, unparsed_output)[0]
    final_status_dict = parser.parse(unparsed_output)
    return final_status_dict

def search_api(query, max_results = 5):
    payload = {
        "query": query,
        "search_depth": "basic",
        "topic": "general",
        "max_results": max_results,
        "include_images": True,
        "include_image_descriptions": False,
        "include_answer": True,
        "include_raw_content": True,
        "include_domains": [],
        "exclude_domains": []
    }
    headers = {
        "Authorization": TAVILY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", tavily_url, json=payload, headers=headers)

    return response.text

def get_chat_response(llm, status_dict, user_input, history, date_time):
    if status_dict['status'] == 'YES':
        return status_dict['answer'], [], [], []
    else:
        prompt_template = ("""
        You a highly intelligent and dedicated **Feminine** AI Assistant created by Aditya Patil.
        Your primary function is to assist users by providing accurate information, answering questions, and engaging in meaningful conversation.
        You are equipped with a vast knowledge base and are capable of understanding complex topics.

        **Chat History:**
        {history}

        **Reference Text**
        {reference_text}

        **User Message:**
        {query}

        Response has to be :
        - Answer has to be in the HINDI Language. Even the numbers have to be in hindi text Eg: 13/१३ has to be written as तेरह.
        - DO NOT REPEAT THE PROMPT
        - CLEAR and INFORMATIVE
        - If user asks a DIRECT and SIMPLE question, then give CONCISE and to the point answer.
        - If user asks a BROAD and OPEN ENDED question, then you can give a longer and COMPREHENSIVE answer.
        - Directly address the user's query or statement.
        - If the output is short, then give PLAIN TEXT OUTPUT.
        - If the output is long and more than 1 paragraph, then give a well ORGANISED OUTPUT with proper headings numerical pointers.
        - Your tone should always be PROFESSIONAL and ARTICULATE, yet FRIENDLY and HUMAN-LIKE.
        - Dont provide a robotic answer. 
        - REMEMBER YOU ARE IN A ONE to ONE CONVERSATION WITH THE PERSON.
        - Today's date and current time is : {date_time}
        """)

        output = search_api(query = status_dict['answer'])
        print(f'------------{output}----------')
        json_data = json.loads(output)

        if isinstance(json_data, dict) and isinstance(json_data.get('results'), list):
            reference_urls = [
                str(result.get('url', 'N/A'))
                for result in json_data['results']
                if result.get('score', 0) > 0.1
            ]
            contents = [
                "Title : " + str(result.get('title', 'N/A')) + "\n" +
                "Content : \n" + str(result.get('content', 'N/A'))
                for result in json_data['results']
                if result.get('score', 0) > 0.1
            ]
            raw_contents = []
            for result in json_data['results']:
                if result.get('score', 0) > 0.1:
                    raw_content = result.get('raw_content') or 'N/A'
                    # Trim raw_content if it exceeds 1000 words
                    if raw_content != 'N/A':
                        words = raw_content.split()
                        raw_content = ' '.join(words[:300]) if len(words) > 300 else raw_content
                    raw_contents.append(raw_content)
            relevancy_scores = [
                str(result.get('score', 'N/A'))
                for result in json_data['results']
                if result.get('score', 0) > 0.1
            ]

        else:
            reference_urls = []
            contents = []
            raw_contents = []
            relevancy_scores = []

        api_answer = json_data['answer']
        image_urls = json_data['images']
        reference_text = "\n\n".join(raw_contents)
        reference_text = api_answer + '\n\n' + reference_text

        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain =  (prompt | llm | StrOutputParser())
        chat_response = chain.invoke({'query': user_input, 'reference_text': reference_text,
                                      'history': history, 'date_time': date_time})
        return chat_response, reference_urls, image_urls, relevancy_scores





















