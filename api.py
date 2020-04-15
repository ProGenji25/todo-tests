#!/usr/bin/env python3

from urllib.parse import urljoin

import requests

class API(object):

    def __init__(self, base_url):
        """ Creates the API client.
        Paramaters:
            base_url (str): The base url for the API.
        Returns:
            New API class for testing an API.
        """
        self.base_url = base_url

    def create_task(self, cookie, Text, Date):
        """ Create a new task
        Parameters:
            cookie (str): Pre-authorized cookie
            Text (str): Text/description of the task.
            Date (str): Due date of the task
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/items")
        data = '{ "Text": "%s", "Date": "%s" }' % (Text, Date)
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("POST", url, headers=headers, data=data)
        return response

    def read_all_tasks(self, cookie):
        """ Reads all collection tasks
        Parameters:
            cookie (str): Pre-authorized cookie
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/items")
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("GET", url, headers=headers)
        return response

    def read_task(self, cookie, task_id):
        """ Create a new task
        Parameters:
            cookie (str): Pre-authorized cookie
            task_id (str): ID of the task.
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/items/" + task_id)
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("GET", url, headers=headers)
        return response

    def update_task(self, cookie, task_id, Done):
        """ Update Done attribute of task with given id
        Parameters:
            cookie (str): Pre-authorized cookie
            task_id (str): ID of the task.
            Done (str): Completion status of the task
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/items/" + task_id)
        data = '{ "Done": %s }' % (str(Done).lower())
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("PUT", url, headers=headers, data=data)
        return response

    def delete_task(self, cookie, task_id):
        """ Delete the task with chosen id
        Parameters:
            cookie (str): Pre-authorized cookie
            task_id (str): ID of the task.
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/items/" + task_id)
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("DELETE", url, headers=headers)
        return response

    def get_user(self, cookie):
        """ Returns current logged-in user
        Parameters:
            cookie (str): Pre-authorized cookie
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/user")
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("GET", url, headers=headers)
        return response

if __name__ == "__main__":
    base_url = "http://localhost:2000" #http://nodejs-golde3.it210.it.et.byu.edu"
    cookie = "s%3AzE1KjRbtMeY9D13TOFO01anUPgfHSEKl.w6%2B43%2F06jt0zOy%2Ff%2BLWrX2pg7ejJvsZOqfeLL71rUds"
    test_id = ""
    api = API(base_url)
    """
    response = api.create_task(cookie, "Test the API", "2020-04-20")
    print(response.ok)
    print(response.status_code)
    print(response.text)
    print(response.json())
    
    response = api.read_all_tasks(cookie)
    print(response.ok)
    print(response.status_code)
    print(response.text)
    print(response.json())
    
    response = api.read_task(cookie, test_id)
    print(response.ok)
    print(response.status_code)
    print(response.text)
    print(response.json())
    
    response = api.update_task(cookie, test_id,"true")
    print(response.ok)
    print(response.status_code)
    print(response.text)
    print(response.json())
    
    response = api.delete_task(cookie, test_id)
    print(response.ok)
    print(response.status_code)
    print(response.text)
    print(response.json())
    
    response = api.get_user(cookie)
    print(response.ok)
    print(response.status_code)
    print(response.text)
    print(response.json())
    """