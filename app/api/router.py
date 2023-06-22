from fastapi import APIRouter
from langchain.llms import OpenAI
import requests
import json
import time

router = APIRouter()

@router.get("/")
async def example():
    return {"it": "works"}

@router.get("/format")
async def example():
    with open('data/tasksAndValues.json') as json_file:
        data = json.load(json_file)

    times_formatted = []

    tasks_formatted = []
    for board in data['data']['boards']:
        for item in board['items']:
            tasks_formatted.append({'task_id': item['id'],
                                    'task_name': item['name'],
                                    'created_at': item['created_at'],
                                    'board_id': board['id']})

            for column in item['column_values']:
                if column['type'] == 'duration':
                    if column['value']:
                        values = json.loads(column['value'])

                        for time_val in values['additional_value']:
                            tmp_val = time_val
                            tmp_val['board_id'] = board['id']
                            tmp_val['task_id'] = item['id']
                            times_formatted.append(tmp_val)

    with open("data/tasks_formatted.json", "w") as new_file:
        new_file.write('\n'.join([json.dumps(task) for task in tasks_formatted]))

    with open("data/times_formatted.json", "w") as new_file:
        new_file.write('\n'.join([json.dumps(time) for time in times_formatted]))

    with open('data/users.json') as json_file:
        data = json.load(json_file)

    with open("data/users_formatted.json", "w") as new_file:
        new_file.write('\n'.join([json.dumps(user) for user in data['data']['users']]))

    with open('data/boardsV.json') as json_file:
        data = json.load(json_file)

    with open("data/boards_formatted.json", "w") as new_file:
        new_file.write('\n'.join([json.dumps(board) for board in data['data']['boards'] if board['type'] == 'board']))

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
