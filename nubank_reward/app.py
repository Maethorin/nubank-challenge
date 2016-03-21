# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, redirect, request, send_from_directory, Response
from nubank_reward import reward

web_app = Flask(__name__)
app_directory = os.path.join(os.getcwd(), 'nubank_reward')
template_directory = os.path.join(app_directory, 'templates')


@web_app.route('/', methods=['GET'])
def index():
    return send_from_directory(template_directory, 'index.html')


def set_points_response(users_data):
    data_tree = reward.build_tree(users_data)
    reward.set_points(users_data, data_tree)
    return Response(json.dumps(users_data), content_type='application/json')


@web_app.route('/invites/file', methods=['POST'])
def invites_input():
    input_file = request.files.get('invites_file', None)
    if not input_file:
        return redirect("/")
    users_data = reward.build_users_data(input_file.read())
    return set_points_response(users_data)


@web_app.route('/invites/add', methods=['POST'])
def invites_add():
    inviting = request.form.get('inviting', None)
    invited = request.form.get('invited', None)
    users_data = json.loads(request.form.get('users_data', '[]'))
    if not invited or not inviting:
        return redirect("/")
    reward.add_user_data(inviting, invited, users_data)
    return set_points_response(users_data)


def run():
    web_app.run(host='0.0.0.0', port=8081, debug=True)