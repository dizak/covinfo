#pylint: disable=import-outside-toplevel,too-few-public-methods
"""
Unit-tests for covinfo module
"""

import unittest


class Request:
    """
    Dummy request class mocking attributes holding by flask.Flask.request
    """
    args = {}

class CovinfoTests(unittest.TestCase):
    """
    Tests of covinfo module
    """
    def setUp(self):
        """
        Data and environment set-up for the tests
        """
        from covinfo import main
        self.main = main

        self.request_empty = Request()
        self.request = Request()
        self.request.args = {
            'country': 'poland',
            'recoveryrate': ''
        }

    def test_get_daily_data(self):
        """
        Test if get_daily_data returns proper data
        """
        output = self.main.get_daily_data(self.request, country='France')
        print(output)
