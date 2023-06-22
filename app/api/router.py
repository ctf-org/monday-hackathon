from fastapi import APIRouter
from langchain.llms import OpenAI
import requests
import json
import time
import os
import openai
openai.api_key = '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'


router = APIRouter()

@router.get("/")
async def example():
    return {"it": "works"}

@router.get("/downloadBoardTask")
async def download_data():
    # Base of your GraphQL query
    query_template = """
    query {{
        boards(limit: 1, page: {page}) {{
            id
            items {{
                name
                id
                state
                created_at
                updated_at
                group {{
                    id
                }}
                column_values {{
                    text
                    description
                    type
                    id
                    value
                }}
            }}
        }}
    }}
    """

    def download_and_save_data(api_key, query, filename):
        url = "https://api.monday.com/v2"
        headers = {
            "Content-Type": "application/json",
            "Authorization": api_key
        }

        page = 1
        has_more_items = True
        all_boards = []

        while has_more_items:
            query = query_template.format(page=page)
            page_query = f'{query}'
            response = requests.post(url, headers=headers, json={"query": page_query})
            # Parse the response
            data = json.loads(response.text)

            if 'status_code' in data and data['status_code'] == 429:
                print("Throttling limit reached. Waiting for a minute...")
                time.sleep(60)
            else:
                if response.status_code == 200:
                    print(response.text)
                    boards = data['data']['boards']
                    if not boards:
                        # If it's empty, break the loop
                        break
                    all_boards.extend(boards)
                    page += 1
                else:
                    print("Error:", response.status_code)
                    break

        with open(filename, "w") as file:
            json.dump(all_boards, file, indent=4)

        print("Data saved successfully.")

    apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI2MzM5MTgzNCwiYWFpIjoxMSwidWlkIjo0NDY5Mjg5MiwiaWFkIjoiMjAyMy0wNi0xOVQwNzo1MDo1Ni45MjdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTc0NDUzNjAsInJnbiI6ImV1YzEifQ.rbK-c0pO_kOgECFGcuOfEcnMJ0ce55w9vlbVV-EW4S0"
    query = query_template.format(page=1)
    filename = "data/tasksAndValues.json"
    download_and_save_data(apiKey, query, filename)

    return {"it": "works"}

@router.get("/downloadUser")
async def download_data():
    def download_and_save_data(api_key, query, filename):
        url = "https://api.monday.com/v2"
        headers = {
            "Content-Type": "application/json",
            "Authorization": api_key
        }

        response = requests.post(url, headers=headers, json={"query": query})

        if response.status_code == 200:
            data = response.json()
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print("Data saved successfully.")
        else:
            print("Error:", response.status_code)

    apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI2MzM5MTgzNCwiYWFpIjoxMSwidWlkIjo0NDY5Mjg5MiwiaWFkIjoiMjAyMy0wNi0xOVQwNzo1MDo1Ni45MjdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTc0NDUzNjAsInJnbiI6ImV1YzEifQ.rbK-c0pO_kOgECFGcuOfEcnMJ0ce55w9vlbVV-EW4S0"
    query = '''
    {
        users {
            name
            email
            id
            birthday
            is_admin
            is_guest
            is_pending
            is_verified
            time_zone_identifier
        }
    }
    '''
    filename = "data/users.json"

    download_and_save_data(apiKey, query, filename)

    return {"it": "works"}

@router.get("/downloadBoards")
async def download_data():
    def download_and_save_data(api_key, query, filename):
        url = "https://api.monday.com/v2"
        headers = {
            "Content-Type": "application/json",
            "Authorization": api_key
        }

        response = requests.post(url, headers=headers, json={"query": query})

        if response.status_code == 200:
            data = response.json()
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print("Data saved successfully.")
        else:
            print("Error:", response.status_code)

    apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI2MzM5MTgzNCwiYWFpIjoxMSwidWlkIjo0NDY5Mjg5MiwiaWFkIjoiMjAyMy0wNi0xOVQwNzo1MDo1Ni45MjdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTc0NDUzNjAsInJnbiI6ImV1YzEifQ.rbK-c0pO_kOgECFGcuOfEcnMJ0ce55w9vlbVV-EW4S0"
    query = '''
    query {
      boards {
        name
        id
        type
        creator {
          id
        }
      }
    }
    '''
    filename = "data/boards.json"

    download_and_save_data(apiKey, query, filename)

    return {"it": "works"}

@router.get("/talkWithAI")
async def talk_with_AI():
    return {"Answer": "Now I am become Death, the destroyer of worlds "}
@router.get("/kowalskiAnalysis")
async def talk_with_AI2(monday_location: str = "Hakaton"):

    def get_problems(monday_location, location_type="Board"):
        #
        # get data from DB 
        # get users wit
        #
        
        forecast=[]
        if(True):
            forecast.append( "Users count time multiple timers at the same time")
        if(True):
            forecast.append("List of users who count time in multiple timers")
        if(True):
            forecast.append("User stop time couter of another user.")

        # end of DB quering

        """Get the current weather in a given location"""
        issues_info = {
            "clickup_location": monday_location,
            "problems_detected": len(forecast),
            "location_type": location_type,
            "forecast": forecast,
        }
        return json.dumps(issues_info)
    def run_conversation():
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": "What is wrong in my data on board "+monday_location+"?"}],
            functions=[
                {
                    "name": "get_problems",
                    "description": "Identify problems in users data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "monday_location": {
                                "type": "string",
                                "description": "Monday item location name",
                            },
                            "board_type": {"type": "string", "enum": ["board", "document", "List"]},
                        },
                        "required": ["monday_location"],
                    },
                }
            ],
            function_call="auto",
        )
        message = response["choices"][0]["message"]
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
        function_response = get_problems(
                monday_location=message.get("monday_location"),
                location_type=message.get("location_type"),
            )
        second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[
                    {"role": "user", "content": "What is wrong in my data on Board "+monday_location+" ?" },
                    message,
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    },
                ],
            )
        return second_response
    answer = run_conversation()
 
    return {"Kowalski": answer["choices"][0]["message"]["content"]}