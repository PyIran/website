#-*- coding: utf-8 -*-

import trello

from flask import request as r, g
# 1 - GET token from: trello.get_token_url('My App', expires='30days', write_access=True)
# 2- members: https://trello.com/1/members/efazati
# 3- http://pythonhosted.org/trello/trello.html
# 4- https://trello.com/docs/api/

# get new token:
#	1) import trello
#	2) t = trello.TrelloApi(API_KEY)
#	3) url = t.get_token_url('AppName', expires='never')
#	4) go to "url", login and allow and get id
#	5) API_TOKEN = step 4 result id!
#	*) after 30Days GoTo step 1 :D

API_KEY = 'd759595bc133670e01b6b306305fb72d'
API_TOKEN = '3101742aaf29de81eac3338dfb4d287dcc2d258d8b1f47140070bcdbc9533a2e'

# t.get_list('RFHiA3ku') ---> list_id
CARD_LIST_ID = '53ca8c8ece6b84afdd5015fb'
MEMBERS = ['leal3', 'RaminNietzsche']


def import_cart_to_list(error):
    try:
        code = error.code
    except:
        code = 500
    title = "%s - %s" % (code, error.message)
    body = """url: %s
	referrer: %s
	user: %s - %s
	request data: %s - %s
	response: %s

	request data:
	header: %s
	args: %s
	""" % (r.url, r.referrer, g.user.username, g.user.username, r.method, r.module, error.args, r.headers, r.values)
    t = trello.Cards(API_KEY, API_TOKEN)

    if uniq_title(title) == 0:
        data = t.new(title, CARD_LIST_ID, desc=body)
        t.new_label(data['id'], 'red')
    else:
        t.new_action_comment(uniq_title(title), body)


def uniq_title(title):
    lists = trello.Lists(API_KEY, API_TOKEN)
    for item in lists.get_card(CARD_LIST_ID):
        if item['name'] == title:
            return item['id']
    return 0
