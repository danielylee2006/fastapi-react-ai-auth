import os
import json
from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

#initialize OpenAI Client with the open ai api key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:

    system_prompt = """You are an expert coding challenge creator. 
    Your task is to generate a coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Return the challenge in the following JSON structure:
    {
        "title": "The question title",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_answer_id": 0, // Index of the correct answer (0-3)
        "explanation": "Detailed explanation of why the correct answer is right"
    }

    Make sure the options are plausible but with only one clearly correct answer. """

    try: 
        
        #OpenAI Python SDK -> accessing the chat completion api to continue conversation
        #We are telling the LLM -> "This is the conversation so far, now complete it.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",

            #Messages represent a conversation history. 
            messages = [
                {"role": "system", "content": system_prompt}, #message to system (training)
                {"role": "user", "content" : f"Generate a {difficulty} difficulty coding challenge"} #message as a user to LLM
            ], 
            response_format = {"type" : "json_object"},
            temperature=0.7 #randomness/creativty of response (0-2.0)
        )

        #response contains list of possible completions, so get the first one and access its content
        content = response.choices[0].message.content

        #convert json string into python dictionary.
        challenge_data = json.loads(content)

        required_fields = ["title", "options", "correct_answer_id", "explanation"]

        #make sure all required_fields are in the generated challenge_data 
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}") #when error raised -> immediately jumps to exception block.
            
        return challenge_data

    except Exception as e:
        print(e)
        return {
            "title" : "Basic Python List Operation", 
            "options" : ["my_list.append(5)", 
                         "my_list_add(5)",
                         "my_list_push(5)",
                         "my_list.insert(5)"],
            "correct_answer_id" : 0,
            "explanaion" : "In Python, append() is the correct method to add an element to the end of a list." 
        }
