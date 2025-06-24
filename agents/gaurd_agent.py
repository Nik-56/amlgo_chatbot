import os
import dotenv
import json
import re
from copy import deepcopy
from .utils import get_chatbot_response

import google.generativeai as genai


dotenv.load_dotenv()



class GaurdAgent():

    def get_response(self, messages):
        messages = deepcopy(messages)

        system_instruction="""
            You are a helpful AI assistant for a ebay.
            Your task is to determine whether a customer is asking something relevant to ebay or not.
            The user is allowed to:
            1. Ask questions about ebay, it's documentation, it's policies related questions.
            2. The user can greet

            The user is not allowed to:
            1. Ask questions anythings else than the ebay related questions
            2. Ask questions about the staff or prices of the products
            3. Ask questions about the competitors of ebay
            4. Ask questions about the personal information of the staff or customers

            Your output should be in JSON format with the following structure, each key is a string and each value is a string,
            make sure to follow the format correctly:
            {
                "chain of thought": "go over each of the points above and see if the message lies under this point or not. Then you write some thought about as what point is the input relevant to."
                "decision": "allowed" or "not allowed", pick one of these choice and only write the word
                "message": leave the message empty "" if allowed otherwise write "sorry I am not allowed to help you with that, is there something else i can help you with?"
            }

            """

        chatbot_output = get_chatbot_response(str(messages[-5:]), system_instruction)

        cleaned = chatbot_output.strip().removeprefix("```json").removesuffix("```").strip()
        output  = self.postproces(cleaned)
        # print("updated output: ", output)
        return output

    def postproces(self, chatbot_output):
        output = json.loads(chatbot_output)

        dict_output = {
            "role": "Assistant",
            "content": output["message"],
            "memory": {
                "agent": "gaurd_agent",
                "gaurd_decision": output["decision"],
            }
        }
        return dict_output
