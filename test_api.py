#!/usr/bin/env python3
import random
import string
import unittest

from api import API

def generate_random_text(l=10):
    """ Helper to generate random text for creating new tasks.
    This is helpful and will ensure that when you run your tests,
    a new text string is created. It is also good for determining
    that two tasks are unique.
    Keyword arguments:
        l (int): How long the generated text should be (default 10)
    Returns:
        A randomly-generated string of length `l`
    """
    chars = string.hexdigits
    return "".join(random.choice(chars) for i in range(l)).lower()


def generate_random_date(year=None, month=None, date=None):
    """ Helper to generate random date for creating new tasks.
    This is helpful as another way of generating random tasks
    Keyword arguments:
        year: Specify a year (default None)
        month: Specify a month (default None)
        date: Specify a date (default None)
    Returns:
        A randomly-generated string representation of a date
    """
    if not year:
        year = str(random.randint(2000, 2025))
    if not month:
        month = str(random.randint(1, 12))
    if not date:
        date = str(random.randint(1, 28))
    return str(year) + "-" + str(month) + "-" + str(date)



class TestAPI(unittest.TestCase):

    # TODO: update these two values with your own.
    base_url = "" #"http://localhost:2000" #http://nodejs-golde3.it210.it.et.byu.edu"
    cookie = ""

    # This will be ran once, when you start your tests.
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.api = API(self.base_url)

    #Tests for correct task requests
    #@unittest.skip("not right now")
    def test_create_task(self):
        """ Tests creating a task is successful.
            - Create the task w/dummy data
            - Verify that the task was created
            - Delete the task we created
        """
        Text = generate_random_text()
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(resp.ok, msg=f"The Create Task failed: {resp.reason}.")
        task = resp.json()

        self.assertEqual(task["Text"], Text, msg="The task's Text did not match the expected Text.")
        self.assertEqual(task["Date"], Date, msg="The task's Date did not match the expected Date.")
        self.assertFalse(task["Done"], msg="The task's Done returned True, expected False.")

        self.api.delete_task(self.cookie, task["_id"])

    #@unittest.skip("not right now")
    def test_read_one_task(self):
        """ Tests reading a task is successful.
            - Create the task w/dummy data
            - Read the task that was created
            - Delete the task we created
        """
        Text = generate_random_text()
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        resp1 = resp.json()

        resp = self.api.read_task(self.cookie, resp1["_id"])
        self.assertTrue(resp.ok, msg=f"The Read One Task failed: {resp.reason}.")
        task = resp.json()

        self.assertEqual(task["Text"], Text, msg="The task's Text did not match the expected Text.")
        self.assertEqual(task["Date"], Date, msg="The task's Date did not match the expected Date.")
        self.assertFalse(task["Done"], msg="The task's Done returned True, expected False.")

        self.api.delete_task(self.cookie, resp1["_id"])

    #@unittest.skip("not right now")
    def test_read_all_tasks(self):
        """ Tests reading all task is successful.
            - Create two tasks w/dummy data
            - Read the tasks that were created
            - Delete the task were created
        """
        Text = generate_random_text()
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        task1 = resp.json()

        Text = generate_random_text()
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        task2 = resp.json()

        resp = self.api.read_all_tasks(self.cookie)
        self.assertTrue(resp.ok, msg=f"The Read All Task failed: {resp.reason}.")
        task = resp.json()

        for t in task:
            self.assertEqual(task[0]["UserId"], t["UserId"], msg="The API should only send tasks belonging to this user")
        
        self.api.delete_task(self.cookie, task1["_id"])
        self.api.delete_task(self.cookie, task2["_id"])

    #@unittest.skip("not right now")
    def test_update_task(self):
        """ Tests updating a task is successful.
            - Create the task w/dummy data
            - Update the Done attribute to true
            - Delete the task we created
        """
        Text = generate_random_text()
        Date = generate_random_date()
        Done = 'true'

        resp = self.api.create_task(self.cookie, Text, Date)
        task = resp.json()

        resp = self.api.update_task(self.cookie, task["_id"], Done)
        self.assertTrue(resp.ok, msg=f"The Update Task failed: {resp.reason}.")
        task = resp.json()
        self.assertTrue(task["Done"], msg="The task's Done returned False, expected True.")

        resp = self.api.read_task(self.cookie, task["_id"])
        task = resp.json()
        self.api.delete_task(self.cookie, task["_id"])
    
    #@unittest.skip("not right now")
    def test_delete_task(self):
        """ Tests deleting a task is successful.
            - Create the task w/dummy data
            - Delete the task we created
            - Read the task to show it was deleted
        """
        Text = generate_random_text()
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(resp.ok, msg=f"The Create Task failed: {resp.reason}.")
        task = resp.json()

        resp = self.api.delete_task(self.cookie, task["_id"])
        self.assertTrue(resp.ok, msg=f"The Delete Task failed: {resp.reason}.")

        resp = self.api.read_task(self.cookie, task["_id"])
        self.assertFalse(resp.ok, msg=f"The Read Task failed after Delete: {resp.reason}.")

    #@unittest.skip("not right now")
    def test_current_user(self):
        """ Tests successful user login.
            - Get user object
            - Check if major attributes are present
        """
        resp = self.api.get_user(self.cookie)
        self.assertTrue(resp.ok, msg=f"The Get User Task failed: {resp.reason}.")
        user = resp.json()

        self.assertIn("Id", user, msg="The user's Id is not present.")
        self.assertIn("UserName", user, msg="The user's Username is not present.")
        self.assertIn("Email", user, msg="The user's Email is not present.")

    #Tests that fail on bad requests
    #@unittest.skip("not right now")
    def test_fail_read_one_nonexistent(self):
        """ Tests read faliure - nonexistent task
            -Try to read nonexistent task
            -Make sure response is 404
        """
        Id = generate_random_text(24)
        resp = self.api.read_task(self.cookie, Id)
        self.assertEqual(resp.status_code, 404, msg=f"The bad Read One test failed: {resp.reason}.")
        resp.text

    #@unittest.skip("not right now")
    def test_fail_delete_nonexistent(self):
        """ Tests delete faliure - nonexistent task
            -Try to delete nonexistent task
            -Make sure response is 404
        """
        Id = generate_random_text(24)
        resp = self.api.delete_task(self.cookie, Id)
        self.assertEqual(resp.status_code, 404, msg=f"The first bad Delete test failed: {resp.reason}.")
        resp.text

    #@unittest.skip("not right now")
    def test_fail_update_nonexistent(self):
        """ Tests update faliure - nonexistent task
            -Try to update nonexistent task
            -Make sure response is 404
        """
        Id = generate_random_text(24)
        resp = self.api.update_task(self.cookie, Id, True)
        self.assertEqual(resp.status_code, 404, msg=f"The bad Update test failed: {resp.reason}.")
        resp.text

    #@unittest.skip("not right now")
    def test_fail_delete_bad_id(self):
        """ Tests delete faliure - bad Mongo id
            -Try to delete nonexistent task with bad id
            -Make sure response is 500
        """
        Id = generate_random_text(20)
        resp = self.api.delete_task(self.cookie, Id)
        self.assertEqual(resp.status_code, 500, msg=f"The second bad Delete test failed: {resp.reason}.")
        resp.text

    #@unittest.skip("not right now")
    def test_fail_read_all_nonexistent(self):
        """ Tests read faliure - no login cookie
            -Try to read tasks when not logged in
            -Make sure response is 401
        """
        resp = self.api.read_all_tasks('')
        self.assertEqual(resp.status_code, 401, msg=f"The bad Read All Task failed: {resp.reason}.")
        resp.text

    #@unittest.skip("not right now")
    def test_fail_create_missingdata(self):
        """ Tests create faliure - missing data
            -Try to create task
            -Make sure response is 500
        """
        Text = ''
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        self.assertEqual(resp.status_code, 500, msg=f"The Create test with missing data failed: {resp.reason}.")
        resp.text

    # Make more methods that begin with 'test` to test all endpoints
    # properly work and fail when you expect them to.

# Inside this `if` statement will only run if we call the program as
# the top-level module, i.e. when we run this file, not when we import
# this file
if __name__ == "__main__":
    unittest.main()