# -*- coding: utf-8 -*-

import unittest

from nubank_reward import reward

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


class TestReward(unittest.TestCase):

    users_data = []
    data_tree = {}

    def setUp(self):
        self.maxDiff = None
        super(TestReward, self).setUp()
        self.users_data = [
            {'1': {'points': 0, 'invitees': ['2', '3'], 'invited_by': None}},
            {'2': {'points': 0, 'invitees': [], 'invited_by': '1'}},
            {'3': {'points': 0, 'invitees': ['4'], 'invited_by': '1'}},
            {'4': {'points': 0, 'invitees': ['5', '6'], 'invited_by': '3'}},
            {'5': {'points': 0, 'invitees': [], 'invited_by': '4'}},
            {'6': {'points': 0, 'invitees': ['7', '8'], 'invited_by': '4'}},
            {'7': {'points': 0, 'invitees': ['9'], 'invited_by': '6'}},
            {'8': {'points': 0, 'invitees': [], 'invited_by': '6'}},
            {'9': {'points': 0, 'invitees': [], 'invited_by': '7'}},
            {'10': {'points': 0, 'invitees': ['11'], 'invited_by': None}},
            {'11': {'points': 0, 'invitees': ['12', '1'], 'invited_by': '10'}},
            {'12': {'points': 0, 'invitees': [], 'invited_by': '11'}}
        ]
        self.data_tree = {
            '1': {
                '2': {},
                '3': {
                    '4': {
                        '5': {},
                        '6': {
                            '7': {
                                '9': {}
                            },
                            '8': {}
                        }
                    }
                }
            },
            '10': {
                '11': {
                    '12': {}
                }
            }
        }

    def test_create_user_data_no_invited(self):
        user_data = reward.create_user_data('1', invitees=[2, 3])
        self.assertEqual(user_data, {'1': {'points': 0, 'invitees': [2, 3], 'invited_by': None}})

    def test_create_user_data_invited(self):
        user_data = reward.create_user_data('1', invited_by=2, invitees=[5, 6])
        self.assertEqual(user_data, {'1': {'points': 0, 'invitees': [5, 6], 'invited_by': 2}})

    def test_find_no_invitor(self):
        users_data = [
            {'5': {'points': 0, 'invitees': ['2', '3'], 'invited_by': None}},
            {'1': {'points': 0, 'invitees': ['4', '5'], 'invited_by': None}},
        ]
        self.assertEqual(reward.find_invited_by(users_data, '1'), None)

    def test_find_the_invitor(self):
        users_data = [
            {'5': {'points': 0, 'invitees': ['2', '3'], 'invited_by': None}},
            {'1': {'points': 0, 'invitees': ['4', '5'], 'invited_by': None}},
        ]
        self.assertEqual(reward.find_invited_by(users_data, '5'), '1')

    def test_find_user_data(self):
        user_data = reward.find_user_data('3', self.users_data)
        self.assertEqual(user_data, {'3': {'points': 0, 'invitees': ['4'], 'invited_by': '1'}})
        user_data = reward.find_user_data('7', self.users_data)
        self.assertEqual(user_data, {'7': {'points': 0, 'invitees': ['9'], 'invited_by': '6'}})

    def test_find_user_data_return_none_if_no_user(self):
        user_data = reward.find_user_data('100', self.users_data)
        self.assertEqual(user_data, None)

    def test_user_construct_users_data(self):
        users_data = reward.build_users_data(INPUT)
        self.assertEqual(
            users_data,
            self.users_data
        )

    def test_check_id_user_is_in_tree_first_level(self):
        self.assertTrue(reward.user_in_tree(self.data_tree, '1'))

    def test_check_id_user_is_in_tree_deep_level(self):
        self.assertTrue(reward.user_in_tree(self.data_tree, '6'))

    def test_build_tree(self):
        data_tree = reward.build_tree(self.users_data)
        self.assertEqual(
            data_tree,
            self.data_tree
        )
    #
    # def test_set_points(self):
    #     users_data = reward.set_points(self.users_data, self.data_tree)
    #     self.assertEqual(
    #         users_data,
    #         [
    #             {'1': {'points': 1.875, 'invitees': ['2', '3'], 'invited_by': None}},
    #             {'2': {'points': 0, 'invitees': [], 'invited_by': '1'}},
    #             {'3': {'points': 1.75, 'invitees': ['4'], 'invited_by': '1'}},
    #             {'4': {'points': 1.5, 'invitees': ['5', '6'], 'invited_by': '3'}},
    #             {'5': {'points': 0, 'invitees': [], 'invited_by': '4'}},
    #             {'6': {'points': 1, 'invitees': ['7', '8'], 'invited_by': '4'}},
    #             {'7': {'points': 0, 'invitees': ['9'], 'invited_by': '6'}},
    #             {'8': {'points': 0, 'invitees': [], 'invited_by': '6'}},
    #             {'9': {'points': 0, 'invitees': [], 'invited_by': '7'}},
    #             {'10': {'points': 1, 'invitees': ['11'], 'invited_by': None}},
    #             {'11': {'points': 0, 'invitees': ['12', '1'], 'invited_by': '10'}},
    #             {'12': {'points': 0, 'invitees': [], 'invited_by': '11'}}
    #         ]
    #     )
