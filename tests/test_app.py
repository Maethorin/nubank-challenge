# -*- coding: utf-8 -*-
import json

import unittest
from StringIO import StringIO
from flask import Request
from nubank_reward import app

INPUT = """
1 2
1 3
3 4
2 4
4 5
4 6
6 7
6 8
7 9
10 11
11 12
11 1
"""


class FileTest(StringIO):
    def read(self, n=-1):
        return INPUT


class RequestMock(Request):
    def _get_file_stream(*args, **kwargs):
        return FileTest()


class AppTestCase(unittest.TestCase):
    expected_response = [
        {"1": {"points": 1.875, "invited_by": [], "invitees": ["2", "3"]}},
        {"2": {"points": 0, "invited_by": ["1"], "invitees": []}},
        {"3": {"points": 1.75, "invited_by": ["1"], "invitees": ["4"]}},
        {"4": {"points": 1.5, "invited_by": ["1", "3"], "invitees": ["5", "6"]}},
        {"5": {"points": 0, "invited_by": ["1", "3", "4"], "invitees": []}},
        {"6": {"points": 1.0, "invited_by": ["1", "3", "4"], "invitees": ["7", "8"]}},
        {"7": {"points": 0, "invited_by": ["1", "3", "4", "6"], "invitees": ["9"]}},
        {"8": {"points": 0, "invited_by": ["1", "3", "4", "6"], "invitees": []}},
        {"9": {"points": 0, "invited_by": ["1", "3", "4", "6", "7"], "invitees": []}},
        {"10": {"points": 1.0, "invited_by": [], "invitees": ["11"]}},
        {"11": {"points": 0, "invited_by": ["10"], "invitees": ["12", "1"]}},
        {"12": {"points": 0, "invited_by": ["10", "11"], "invitees": []}}
    ]

    def setUp(self):
        self.app = app.web_app.test_client()
        app.web_app.request_class = RequestMock

    def test_get_in_invited_files_should_return_405(self):
        invited_files = self.app.get('/invites/file')
        self.assertEqual(invited_files.status_code, 405)

    def test_pots_in_invited_files_redirects_if_not_input_file(self):
        invited_files = self.app.post('/invites/file')
        self.assertEqual(invited_files.status_code, 302)

    def test_get_in_invited_add_should_return_405(self):
        invited_add = self.app.get('/invites/add')
        self.assertEqual(invited_add.status_code, 405)

    def test_post_in_invited_add_should_redirect_if_no_inviting(self):
        invited_add = self.app.post('/invites/add', data={'inviting': None, 'invited': '101'})
        self.assertEqual(invited_add.status_code, 302)

    def test_post_in_invited_add_should_redirect_if_no_invited(self):
        invited_add = self.app.post('/invites/add', data={'inviting': '100', 'invited': None})
        self.assertEqual(invited_add.status_code, 302)

    def test_post_in_invited_files_should_return_json(self):
        invited_files = self.app.post('/invites/file', data={'invites_file': (StringIO(INPUT), 'input.txt')})
        self.assertEqual(json.loads(invited_files.data), self.expected_response)

    def test_post_in_invited_add_should_return_json_without_preloaded_data(self):
        invited_add = self.app.post('/invites/add', data={'inviting': '100', 'invited': '101'})
        self.assertEqual(
            json.loads(invited_add.data),
            [
                {'100': {'invited_by': [], 'invitees': ['101'], 'points': 0}},
                {'101': {'invited_by': ['100'], 'invitees': [], 'points': 0}}
            ]
        )

    def test_post_in_invited_add_should_return_json_with_preloaded_data(self):
        invited_add = self.app.post('/invites/add', data={'inviting': '100', 'invited': '101', 'users_data': json.dumps(self.expected_response)})
        self.assertEqual(
            json.loads(invited_add.data),
            self.expected_response +
            [
                {'100': {'invited_by': [], 'invitees': ['101'], 'points': 0}},
                {'101': {'invited_by': ['100'], 'invitees': [], 'points': 0}}
            ]
        )
