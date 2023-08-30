import argparse
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    api_key = input("Please provide your API key: ")

api = TodoistAPI(api_key)

def add_task(name, project_id):
    try:
        task = api.add_task(content=name, project_id=project_id)
        print(task)
    except Exception as error:
        print(error)

def get_tasks():
    try:
        tasks = api.get_tasks()
        for task in tasks:
            print(task.content)
    except Exception as error:
        print(error)

def get_tasks_for_next_days(days):
    try:
        tasks = api.get_tasks()
        for task in tasks:
            if datetime.now() <= datetime.strptime(task.due_date, '%Y-%m-%dT%H:%M:%S') <= datetime.now() + timedelta(days=days):
                print(task.content)
    except Exception as error:
        print(error)

def complete_task(task_content):
    try:
        tasks = api.get_tasks()
        for task in tasks:
            if task.content == task_content:
                is_success = api.close_task(task_id=task.id)
                if not is_success:
                    raise Exception("400 Client Error: Bad Request for url: https://api.todoist.com/rest/v2/tasks/test/close")
                print(is_success)
                break
    except Exception as error:
        print(error)

parser = argparse.ArgumentParser(description='Manage Todoist tasks.')
subparsers = parser.add_subparsers(dest='command')

add_task_parser = subparsers.add_parser('add', help='Add a new task.')
add_task_parser.add_argument('name', help='Name of the task.')
add_task_parser.add_argument('project_id', help='ID of the project.')

get_tasks_parser = subparsers.add_parser('get', help='Get all tasks.')

get_tasks_for_next_days_parser = subparsers.add_parser('get_next_days', help='Get tasks for the next days.')
get_tasks_for_next_days_parser.add_argument('days', type=int, help='Number of days to get tasks for.')

complete_task_parser = subparsers.add_parser('complete', help='Complete a task.')
complete_task_parser.add_argument('task_content', help='Content of the task to complete.')

args = parser.parse_args()

if args.command == 'add':
    add_task(args.name, args.project_id)
elif args.command == 'get':
    get_tasks()
elif args.command == 'get_next_days':
    get_tasks_for_next_days(args.days)
elif args.command == 'complete':
    complete_task(args.task_content)

