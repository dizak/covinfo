#pylint: disable=import-outside-toplevel,too-few-public-methods,bad-continuation
"""
Unit-tests for covinfo module
"""

import unittest
import json


class Request:
    """
    Dummy request class mocking attributes holding by flask.Flask.request
    """
    args = {}

    def get(
        self,
        key,
    ):
        """
        Return args
        """
        return self.args[key]

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
        self.request_portugal_days_10 = Request()
        self.request_portugal_days_10.args = {
                'country': 'portugal',
                'days': 10,
        }
        self.request.args = {
            'country': 'poland',
            'recoveryrate': ''
        }

    def test_get_daily_data_req_empty(self):
        """
        Test if get_daily_data returns proper data if request args dict is
        empty
        """
        output = self.main.get_daily_data(self.request_empty)
        self.assertIsInstance(
            json.loads(output)[0],
            dict,
        )

    def test_get_daily_data_req_args(self):
        """
        Test if get_daily_data returns proper data
        """
        output = self.main.get_daily_data(self.request)
        self.assertIsInstance(
            float(output),
            float,
        )

    def test_get_changerate(self):
        """
        Test if get_daily_data return proper data for change rate
        """
        output = self.main.get_changerate(self.request_portugal_days_10)
        #self.assertIsInstance(
        #    output,
        #    float,
        #)
        print(output)
