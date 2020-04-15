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
    base_url = "http://localhost:2000" #http://nodejs-golde3.it210.it.et.byu.edu"
    cookie = "s%3AzE1KjRbtMeY9D13TOFO01anUPgfHSEKl.w6%2B43%2F06jt0zOy%2Ff%2BLWrX2pg7ejJvsZOqfeLL71rUds"

    # This will be ran once, when you start your tests.
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.api = API(self.base_url)

    #Tests for correct task requests
    def test_create_task(self):
        """ Tests creating a task is successful.
        This is an example test:
            - Create the task w/dummy data
            - Verify that the task was created
            - Delete the task we created
        You will be required to implement the other tests
        that are defined in BaseTestCase. They will be marked
        with @abc.abstractmethod.
        """
        Text = generate_random_text()
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(resp.ok, msg=f"The Create Task failed: {resp.reason}.")
        task = resp.json()

        self.assertEqual(task["Text"], Text, msg="The task's Text did not match the expected Text.")
        self.assertEqual(task["Date"], Date, msg="The task's Date did not match the expected Date.")
        self.assertFalse(task["Done"], msg="The task's Done returned True, expected False.")

        # cleanup - we don't want to conflict with other tests
        # or have a test task in our database.
        self.api.delete_task(self.cookie, task["_id"])

    def test_read_one_task(self):
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

    def test_read_all_tasks(self):
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
            self.assertEqual(task[0]["UserId"], t["UserId"])
        # self.assertEqual(task[0]["_id"], task1["_id"], msg="The first task's ID did not match the expected ID.")
        # self.assertEqual(task[1]["_id"], task2["_id"], msg="The second task's ID did not match the expected ID.")
        
        self.api.delete_task(self.cookie, task1["_id"])
        self.api.delete_task(self.cookie, task2["_id"])

    def test_update_task(self):
        Text = generate_random_text()
        Date = generate_random_date()
        Done = 'true'

        resp = self.api.create_task(self.cookie, Text, Date)
        
        task = resp.json()

        resp = self.api.update_task(self.cookie, task["_id"], Done)
        self.assertTrue(resp.ok, msg=f"The Update Task failed: {resp.reason}.")
        self.assertTrue(task["Done"], msg="The task's Done returned False, expected True.")

        self.api.delete_task(self.cookie, task["_id"])
    
    def test_delete_task(self):
        Text = generate_random_text()
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(resp.ok, msg=f"The Create Task failed: {resp.reason}.")
        task = resp.json()

        resp = self.api.delete_task(self.cookie, task["_id"])
        self.assertTrue(resp.ok, msg=f"The Delete Task failed: {resp.reason}.")

        resp = self.api.read_task(self.cookie, task["_id"])
        self.assertFalse(resp.ok, msg=f"The Read Task failed after Delete: {resp.reason}.")

    def test_current_user(self):
        resp = self.api.get_user(self.cookie)
        self.assertTrue(resp.ok, msg=f"The Get User Task failed: {resp.reason}.")
        user = resp.json()

        self.assertIn("Id", user, msg="The user's Id is not present.")
        self.assertIn("UserName", user, msg="The user's Username is not present.")
        self.assertIn("Email", user, msg="The user's Email is not present.")

    #Tests that fail on bad requests
    def test_fail_read_one_nonexistent(self):
        Id = generate_random_text(24)
        resp = self.api.read_task(self.cookie, Id)
        self.assertEqual(resp.status_code(404), 404, msg=f"The bad Read One test failed: {resp.reason}.")
        resp.text

    def test_fail_delete_nonexistent(self):
        Id = generate_random_text(24)
        resp = self.api.delete_task(self.cookie, Id)
        self.assertEqual(resp.status_code(404), 404, msg=f"The first bad Delete test failed: {resp.reason}.")
        resp.text

    def test_fail_update_nonexistent(self):
        Id = generate_random_text(24)
        resp = self.api.update_task(self.cookie, Id, True)
        self.assertEqual(resp.status_code(404), 404, msg=f"The bad Update test failed: {resp.reason}.")
        resp.text

    def test_fail_delete_bad_id(self):
        Id = generate_random_text(12)
        resp = self.api.delete_task(self.cookie, Id)
        self.assertEqual(resp.status_code(500), 500, msg=f"The second bad Delete test failed: {resp.reason}.")
        resp.text

    def test_fail_read_all_nonexistent(self):
        resp = self.api.read_all_tasks('')
        self.assertEqual(resp.status_code(401), 401, msg=f"The bad Read All Task failed: {resp.reason}.")
        resp.text

    def test_fail_create_missingdata(self):
        Text = ''
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        self.assertEqual(resp.status_code(500), 500, msg=f"The Create test with missing data failed: {resp.reason}.")
        resp.text

    # Make more methods that begin with 'test` to test all endpoints
    # properly work and fail when you expect them to.

# Inside this `if` statement will only run if we call the program as
# the top-level module, i.e. when we run this file, not when we import
# this file
if __name__ == "__main__":
    unittest.main()