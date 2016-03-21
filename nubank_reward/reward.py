# -*- coding: utf-8 -*-


def find_invited_by(users_data, user_id):
    for user_data in users_data:
        key = [k for k in user_data.keys()][0]
        if user_id in user_data[key]['invitees']:
            return key
    return None


def create_user_data(user_id, users_data, invited_by=None, invitees=None):
    if not invitees:
        invitees = []
    if invited_by:
        invited_data = find_user_data(invited_by, users_data)
        invited_by = invited_data[invited_by]['invited_by'] + [invited_by]
    else:
        invited_by = []
    return {user_id: {'points': 0, 'invitees': invitees, 'invited_by': invited_by}}


def find_user_data(user, users_data):
    try:
        return [user_data for user_data in users_data if user in user_data][0]
    except IndexError:
        return None


def build_users_data(data_input):
    data_input = data_input.split('\n')
    users_data = []
    for line in data_input:
        if line:
            line = line.split(' ')
            line[1] = line[1].replace('\r', '')
            users_data.extend(add_users_data(line[0], line[1], users_data))
    return users_data


def add_users_data(inviting, invited, users_data):
    can_be_invited = find_invited_by(users_data, invited) is None
    user_data = find_user_data(inviting, users_data)
    return_data = []
    if user_data:
        if can_be_invited:
            user_data[inviting]['invitees'].append(invited)
    else:
        invited_by = find_invited_by(users_data, inviting)
        invitees = [invited] if can_be_invited else []
        return_data.append(create_user_data(inviting, users_data, invited_by=invited_by, invitees=invitees))
    user_data = find_user_data(invited, users_data)
    if not user_data:
        invited_by = find_invited_by(users_data, invited) or inviting
        return_data.append(create_user_data(invited, (users_data + return_data), invited_by=invited_by))
    return return_data


def build_tree(users_data):
    data_tree = {}
    for user_data in users_data:
        key = [k for k in user_data.keys()][0]
        user_data = user_data[key]
        if key not in data_tree and not user_data['invited_by']:
            data_tree[key] = {}
            add_branch(data_tree, key, user_data['invitees'], users_data, data_tree)
    return data_tree


def add_branch(sub_tree, key, invitees, users_data, data_tree):
    for invitee in invitees:
        if user_in_tree(data_tree, invitee):
            continue
        invitee_data = find_user_data(invitee, users_data)
        if invitee_data:
            sub_tree[key][invitee] = {}
            if invitee_data[invitee]['invitees']:
                add_branch(sub_tree[key], invitee, invitee_data[invitee]['invitees'], users_data, data_tree)


def user_in_tree(data_tree, user_id):
    if user_id in data_tree:
        return True
    for node in data_tree:
        if user_in_tree(data_tree[node], user_id):
            return True
    return False


def set_user_points(data_tree, user, level=0):
    if data_tree is None:
        return 0
    points = 0
    for user_id in data_tree[user]:
        if data_tree[user][user_id]:
            points += 0.5 ** level
        points += set_user_points(data_tree[user], user_id, level=level + 1)
    return points


def get_invited_by_tree(data_tree, inviteds_by):
    if not inviteds_by:
        return data_tree
    tree = data_tree
    for invited_by in inviteds_by:
        try:
            tree = tree[invited_by]
        except KeyError:
            return None
    return tree


def set_points(users_data, data_tree):
    users_with_points = list(users_data)
    for user_data in users_with_points:
        user_id = [k for k in user_data.keys()][0]
        tree = get_invited_by_tree(data_tree, user_data[user_id]['invited_by'])
        user_data[user_id]['points'] = set_user_points(tree, user_id)
    return users_with_points
