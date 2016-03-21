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
12 13
13 14
14 15
15 16
16 17
17 18
18 19
19 25
18 20
20 26
18 21
21 27
18 22
22 28
18 23
23 29
18 24
24 30
"""


class TestReward(unittest.TestCase):

    users_data = []
    data_tree = {}

    def setUp(self):
        self.maxDiff = None
        super(TestReward, self).setUp()
        self.users_data = [
            {'1': {'points': 0, 'invitees': ['2', '3'], 'invited_by': []}},
            {'2': {'points': 0, 'invitees': [], 'invited_by': ['1']}},
            {'3': {'points': 0, 'invitees': ['4'], 'invited_by': ['1']}},
            {'4': {'points': 0, 'invitees': ['5', '6'], 'invited_by': ['1', '3']}},
            {'5': {'points': 0, 'invitees': [], 'invited_by': ['1', '3', '4']}},
            {'6': {'points': 0, 'invitees': ['7', '8'], 'invited_by': ['1', '3', '4']}},
            {'7': {'points': 0, 'invitees': ['9'], 'invited_by': ['1', '3', '4', '6']}},
            {'8': {'points': 0, 'invitees': [], 'invited_by': ['1', '3', '4', '6']}},
            {'9': {'points': 0, 'invitees': [], 'invited_by': ['1', '3', '4', '6', '7']}},
            {'10': {'points': 0, 'invitees': ['11'], 'invited_by': []}},
            {'11': {'points': 0, 'invitees': ['12', '1'], 'invited_by': ['10']}},
            {'12': {'points': 0, 'invitees': ['13'], 'invited_by': ['10', '11']}},
            {'13': {'points': 0, 'invitees': ['14'], 'invited_by': ['10', '11', '12']}},
            {'14': {'points': 0, 'invitees': ['15'], 'invited_by': ['10', '11', '12', '13']}},
            {'15': {'points': 0, 'invitees': ['16'], 'invited_by': ['10', '11', '12', '13', '14']}},
            {'16': {'points': 0, 'invitees': ['17'], 'invited_by': ['10', '11', '12', '13', '14', '15']}},
            {'17': {'points': 0, 'invitees': ['18'], 'invited_by': ['10', '11', '12', '13', '14', '15', '16']}},
            {'18': {'points': 0, 'invitees': ['19', '20', '21', '22', '23', '24'], 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17']}},
            {'19': {'points': 0, 'invitees': ['25'], 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18']}},
            {'25': {'points': 0, 'invitees': [], 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']}},
            {'20': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['26']}},
            {'26': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '20'], 'invitees': []}},
            {'21': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['27']}},
            {'27': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '21'], 'invitees': []}},
            {'22': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['28']}},
            {'28': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '22'], 'invitees': []}},
            {'23': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['29']}},
            {'29': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '23'], 'invitees': []}},
            {'24': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['30']}},
            {'30': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '24'], 'invitees': []}}
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
                    '12': {
                        '13': {
                            '14': {
                                '15': {
                                    '16': {
                                        '17': {
                                            '18': {
                                                '19': {
                                                    '25': {}
                                                },
                                                '20': {
                                                    '26': {}
                                                },
                                                '21': {
                                                    '27': {}
                                                },
                                                '22': {
                                                    '28': {}
                                                },
                                                '23': {
                                                    '29': {}
                                                },
                                                '24': {
                                                    '30': {}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

    def test_create_user_data_no_invited(self):
        user_data = reward.create_user_data('1', self.users_data, invitees=['2', '3'])
        self.assertEqual(user_data, {'1': {'points': 0, 'invitees': ['2', '3'], 'invited_by': []}})

    def test_create_user_data_invited_level_zero(self):
        user_data = reward.create_user_data('3', self.users_data, invited_by='1', invitees=['4'])
        self.assertEqual(user_data, {'3': {'points': 0, 'invitees': ['4'], 'invited_by': ['1']}})

    def test_create_user_data_invited_level_one(self):
        user_data = reward.create_user_data('4', self.users_data, invited_by='3', invitees=['5', '6'])
        self.assertEqual(user_data, {'4': {'points': 0, 'invitees': ['5', '6'], 'invited_by': ['1', '3']}})

    def test_find_no_inviting(self):
        users_data = [
            {'5': {'points': 0, 'invitees': ['2', '3'], 'invited_by': []}},
            {'1': {'points': 0, 'invitees': ['4', '5'], 'invited_by': []}},
        ]
        self.assertEqual(reward.find_invited_by(users_data, '1'), None)

    def test_find_the_inviting(self):
        users_data = [
            {'5': {'points': 0, 'invitees': ['2', '3'], 'invited_by': []}},
            {'1': {'points': 0, 'invitees': ['4', '5'], 'invited_by': []}},
        ]
        self.assertEqual(reward.find_invited_by(users_data, '5'), '1')

    def test_find_user_data(self):
        user_data = reward.find_user_data('3', self.users_data)
        self.assertEqual(user_data, {'3': {'points': 0, 'invitees': ['4'], 'invited_by': ['1']}})
        user_data = reward.find_user_data('7', self.users_data)
        self.assertEqual(user_data, {'7': {'points': 0, 'invitees': ['9'], 'invited_by': ['1', '3', '4', '6']}})

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

    def test_set_user_one_points(self):
        points = reward.set_user_points(self.data_tree, '1')
        self.assertEqual(points, 1.875)

    def test_set_user_two_points(self):
        points = reward.set_user_points(self.data_tree['1'], '2')
        self.assertEqual(points, 0)

    def test_set_user_three_points(self):
        points = reward.set_user_points(self.data_tree['1'], '3')
        self.assertEqual(points, 1.75)

    def test_set_user_six_points(self):
        points = reward.set_user_points(self.data_tree['1']['3']['4'], '6')
        self.assertEqual(points, 1)

    def test_get_invited_by_tree_level_zero(self):
        tree = reward.get_invited_by_tree(self.data_tree, [])
        self.assertEqual(
            tree,
            self.data_tree
        )

    def test_get_invited_by_tree_level_one(self):
        tree = reward.get_invited_by_tree(self.data_tree, ['1'])
        self.assertEqual(
            tree,
            self.data_tree['1']
        )

    def test_get_invited_by_tree_level_two(self):
        tree = reward.get_invited_by_tree(self.data_tree, ['1', '3'])
        self.assertEqual(
            tree,
            self.data_tree['1']['3']
        )

    def test_get_invited_by_tree_level_tree(self):
        tree = reward.get_invited_by_tree(self.data_tree, ['1', '3', '4'])
        self.assertEqual(
            tree,
            self.data_tree['1']['3']['4']
        )

    def test_get_invited_by_tree_should_return_none_if_no_tree(self):
        tree = reward.get_invited_by_tree(self.data_tree, ['1', '3', '5'])
        self.assertIsNone(tree)

    def test_set_points(self):
        users_data_with_points = reward.set_points(self.users_data, self.data_tree)
        self.assertEqual(
            users_data_with_points,
            [
                {'1': {'points': 1.875, 'invitees': ['2', '3'], 'invited_by': []}},
                {'2': {'points': 0, 'invitees': [], 'invited_by': ['1']}},
                {'3': {'points': 1.75, 'invitees': ['4'], 'invited_by': ['1']}},
                {'4': {'points': 1.5, 'invitees': ['5', '6'], 'invited_by': ['1', '3']}},
                {'5': {'points': 0, 'invitees': [], 'invited_by': ['1', '3', '4']}},
                {'6': {'points': 1, 'invitees': ['7', '8'], 'invited_by': ['1', '3', '4']}},
                {'7': {'points': 0, 'invitees': ['9'], 'invited_by': ['1', '3', '4', '6']}},
                {'8': {'points': 0, 'invitees': [], 'invited_by': ['1', '3', '4', '6']}},
                {'9': {'points': 0, 'invitees': [], 'invited_by': ['1', '3', '4', '6', '7']}},
                {'10': {'points': 2.015625, 'invitees': ['11'], 'invited_by': []}},
                {'11': {'points': 2.03125, 'invitees': ['12', '1'], 'invited_by': ['10']}},
                {'12': {'points': 2.0625, 'invitees': ['13'], 'invited_by': ['10', '11']}},
                {'13': {'points': 2.125, 'invited_by': ['10', '11', '12'], 'invitees': ['14']}},
                {'14': {'points': 2.25, 'invited_by': ['10', '11', '12', '13'], 'invitees': ['15']}},
                {'15': {'points': 2.5, 'invited_by': ['10', '11', '12', '13', '14'], 'invitees': ['16']}},
                {'16': {'points': 3, 'invited_by': ['10', '11', '12', '13', '14', '15'], 'invitees': ['17']}},
                {'17': {'points': 4, 'invited_by': ['10', '11', '12', '13', '14', '15', '16'], 'invitees': ['18']}},
                {'18': {'points': 6, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17'], 'invitees': ['19', '20', '21', '22', '23', '24']}},
                {'19': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['25']}},
                {'25': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19'], 'invitees': []}},
                {'20': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['26']}},
                {'26': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '20'], 'invitees': []}},
                {'21': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['27']}},
                {'27': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '21'], 'invitees': []}},
                {'22': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['28']}},
                {'28': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '22'], 'invitees': []}},
                {'23': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['29']}},
                {'29': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '23'], 'invitees': []}},
                {'24': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18'], 'invitees': ['30']}},
                {'30': {'points': 0, 'invited_by': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '24'], 'invitees': []}}
            ]
        )
