from fastapi import APIRouter
from langchain.llms import OpenAI
import requests
import json
import time
import os
from app.db import db

router = APIRouter()

@router.get("/")
async def example():
    return {"it": "works"}

@router.get("/init")
async def init():
    await download_board_task()
    await download_user()
    await download_boards()
    await format_data()
    await import_data()

    return {"status": "ok"}

@router.get("/format")
async def format_data():
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

    with open('data/boards.json') as json_file:
        data = json.load(json_file)

    with open("data/boards_formatted.json", "w") as new_file:
        new_file.write('\n'.join([json.dumps(board) for board in data['data']['boards'] if board['type'] == 'board']))

@router.get("/import")
async def import_data():
    f = open("database.sql", "r")
    query = f.read()
    f.close()

    sqlCommands = query.split(';')
    for command in sqlCommands:
        await db.execute(command)

    return {"status": "ok"}

@router.get("/download-board-task")
async def download_board_task():
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
    query = query_template.format(page=1)
    filename = "data/tasksAndValues.json"
    download_and_save_data(os.environ.get('MONDAY_API_KEY'), query, filename)

    return {"it": "works"}

@router.get("/download-user")
async def download_user():
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

    download_and_save_data(os.environ.get('MONDAY_API_KEY'), query, filename)

    return {"it": "works"}

@router.get("/download-boards")
async def download_boards():
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

    download_and_save_data(os.environ.get('MONDAY_API_KEY'), query, filename)

    return {"it": "works"}
@router.get("/wrong/3")
async def mistake():
    query = """
        SELECT tt.task_id, tt.board_id, tt.started_at, tt.ended_at,
               started_user.username AS started_username, started_user.email AS started_user_email,started_user.id AS started_user_id,
               ended_user.username AS ended_username,ended_user.id AS ended_id, ended_user.email AS ended_user_email, tasks_data.task_name,
               boards_data.board_name
        FROM monday_src.time_tracking tt
        LEFT JOIN monday_src.users started_user ON tt.started_user_id = started_user.id
        LEFT JOIN monday_src.users ended_user ON tt.ended_user_id = ended_user.id
        LEFT JOIN monday_src.tasks tasks_data ON tt.task_id = tasks_data.id
        LEFT JOIN monday_src.boards boards_data ON tt.board_id = boards_data.id
        WHERE tt.started_user_id != tt.ended_user_id;
    """

    rows = await db.fetch_all(query=query)

    return rows
