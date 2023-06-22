from fastapi import APIRouter
from langchain.llms import OpenAI
import requests
import json
import time

router = APIRouter()

@router.get("/")
async def root():
    return {"it": "works"}

@router.get("/example")
async def example():
    llm = OpenAI(temperature=0.9)
    text = "What would be a good company name for a company that makes colorful socks?"
    return {text: llm(text).strip()}

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
                    all_boards.extend(data['data']['boards'])
                    page += 1
                else:
                    print("Error:", response.status_code)
                    break
        new_dict = {
            "data": {
                "boards": all_boards
            }
        }
        with open(filename, "w") as file:
            json.dump(new_dict, file, indent=4)

        print("Data saved successfully.")

    apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI2MzM5MTgzNCwiYWFpIjoxMSwidWlkIjo0NDY5Mjg5MiwiaWFkIjoiMjAyMy0wNi0xOVQwNzo1MDo1Ni45MjdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTc0NDUzNjAsInJnbiI6ImV1YzEifQ.rbK-c0pO_kOgECFGcuOfEcnMJ0ce55w9vlbVV-EW4S0"
    query = query_template.format(page=1)
    filename = "tasksAndValues.json"
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
    filename = "users.json"

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
    filename = "boards.json"

    download_and_save_data(apiKey, query, filename)

    return {"it": "works"}
