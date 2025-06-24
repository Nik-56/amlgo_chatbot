import os
import dotenv
import json
import re
from copy import deepcopy
from .utils import get_chatbot_response, get_embeddings
import google.generativeai as genai
from pinecone import Pinecone

dotenv.load_dotenv()

source_knowledge = ''

class DetailsAgent():
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        self.index_name = os.getenv('PINECONE_INDEX_NAME')

    def get_closest_response(self, index_name, input_embeddings, top_k = 2 ):
        index = self.pc.Index(index_name)

        results = index.query(
            namespace= 'ns1',
            vector = input_embeddings,
            top_k = top_k,
            include_values = False,
            include_metadata = True
        )
        return results

    
    def get_response(self, messages):
        messages = deepcopy(messages)

        user_messages = str(messages[-3:])
        # print("details agent started\n\n")
        embeddings = get_embeddings(user_messages)
        # print("got embeddings\n\n")
        result = self.get_closest_response(self.index_name, embeddings)
        source_knowledge = "\n".join([x['metadata']['text'].strip()+'\n' for x in result['matches']])

        prompt = f"""
            Using the context below try to answer the query
            
            Context:
            {source_knowledge}

            Query:
            {user_messages}
        
        """

        system_instruction="""
            You are a customer support agent for a ebay, you should answer latest question as a support agent,
            focus on the latest query
            and provide the necessary information to the user regarding the latest query
            """
        messages[-1] = prompt

        chatbot_output = get_chatbot_response(str(messages[-2:]), system_instruction)

        output  = self.postproces(chatbot_output)
        # print("source: \n",source_knowledge)
        return output, source_knowledge
    
    def postproces(self, output):
        dict_output = {
            "role": "Assistant",
            "content": output,
            "memory": {
                "agent": "details_agent",
            }
        }
        return dict_output
