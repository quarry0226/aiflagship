import json
import logging

import sys
import os
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))

from teamup_service import TeamUpService


logger = logging.getLogger("teamup-bot")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

file_name = os.path.join(os.path.dirname(__file__), 'configuration.json')
with open(file_name) as data_file:
    configuration = json.load(data_file)

service = TeamUpService(configuration)

service.login()


def toss_Chat_Data(team_index, room_index, chat):
	service.post_chat(team_index, room_index, chat, extras=None)
	out = 'true'
	return str(out)



#post_chat(12357, 514334, "Hello")