from __future__ import unicode_literals
import random
from dialogs import data
import json
from flask import Flask, request
import textTypeAnswer

app = Flask(__name__)
sessionStorage = {}


@app.route("/", methods=['POST'])
def main():
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(request.json, response)
    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Ну начнем",
                "Погнали",
            ],
            'cur_theme': 'default',
            'cur_quest': 0,
            'cur_dif': 0,
            'cur_lose': 0,
            'done': {},
            'count_win_quests': 0,
            'count_lose_quests': 0,
        }
        res['response']['text'] = 'Привет, давай начнем собеседование!'
        res['response']['buttons'] = [
            {'title': startButton, 'hide': True}
            for startButton in sessionStorage[user_id]['suggests']
        ]
        return
    print(req['request']['original_utterance'].lower())
    if req['request']['original_utterance'].lower() in {
        "ну начнем",
        "погнали",
    }:
        start_dialog(user_id, res)
        return
    check_answer(user_id, req, res)
    return


def check_answer(user_id, req, res):
    session = sessionStorage[user_id]
    if (data['themes'][session['cur_theme']]['questions'][session['cur_dif']][
        session['cur_quest']]['type'] == 'text' and textTypeAnswer.equals(req['request']['original_utterance'],
                                                                          data['themes'][session['cur_theme']][
                                                                              'questions'][
                                                                              session['cur_dif']][
                                                                              session['cur_quest']]['answers']) > 0.5):
        win_answer(user_id, res)
    elif data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']][
        'type'] != 'text' and \
            not (req['request']['original_utterance'].lower() in
                 data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']][
                     'answers']):
        res['response']['text'] = data['samples']['quest_repeat'].format("\n".join([
            "{}. {}".format(i + 1, item)
            for i, item in enumerate(
                data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['answers'])
        ]))
        res['response']['buttons'] = get_suggests(user_id)
    elif req['request']['original_utterance'].lower() == \
            data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['answers'][
                0].lower():
        win_answer(user_id, res)
    else:
        lose_answer(user_id, res)


def win_answer(user_id, res):
    session = sessionStorage[user_id]
    session['done'][session['cur_theme']]['count_quest'].add(session['cur_quest'])
    session['cur_dif'] += 1
    session['count_win_quests'] += 1
    if session['cur_dif'] > 2:
        if not switch_theme(user_id):
            send_results(user_id, res)
            sessionStorage[user_id] = session
            return
        else:
            session['cur_dif'] = 0
    sessionStorage[user_id] = session
    next_question(user_id, res)
    write_response(user_id, res, True)


def lose_answer(user_id, res):
    session = sessionStorage[user_id]
    session['done'][session['cur_theme']]['count_quest'].add(session['cur_quest'])
    session['cur_dif'] = 0
    session['cur_lose'] += 1
    session['count_lose_quests'] += 1
    if session['cur_lose'] > 2:
        if not switch_theme(user_id):
            send_results(user_id, res)
            sessionStorage[user_id] = session
            return
        else:
            session['cur_lose'] = 0
    sessionStorage[user_id] = session
    next_question(user_id, res)
    write_response(user_id, res, False)


def start_dialog(user_id, res):
    session = sessionStorage[user_id]
    themes = data['themes'].keys()
    for i in themes:
        session['done'][i] = {'count_quest': set()}
    sessionStorage[user_id] = session
    next_question(user_id, res)
    if data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['type'] != 'text':
        res['response']['text'] = '''
            Первый вопрос.
            {}
            Варианты ответов:
            {}
        '''.format(
            data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body'],
            "\n".join(["{}. {}".format(i + 1, item) for i, item in enumerate(
                data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']][
                    'answers'])])
        )
        res['response']['buttons'] = get_suggests(user_id)
    else:
        res['response']['text'] = '''
            Первый вопрос.
            {}
        '''.format(data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body'])


def write_response(user_id, res, isWin):
    session = sessionStorage[user_id]
    if data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['type'] != 'text':
        res['response']['text'] = \
            data['samples']['win_ans'].format(
                session['cur_theme'],
                data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body'],
                "\n".join(["{}. {}".format(i + 1, item) for i, item in enumerate(
                    data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']][
                        'answers'])])
            ) if isWin else data['samples']['lose_ans'].format(
                data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['resource'],
                data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body'],
                "\n".join(["{}. {}".format(i + 1, item) for i, item in enumerate(
                    data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']][
                        'answers'])])
            )
        res['response']['buttons'] = get_suggests(user_id)
    else:
        res['response']['text'] = \
            data['samples']['win_ans'].format(
                session['cur_theme'],
                data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body']
            ) if isWin else data['samples']['lose_ans'].format(
                data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['resource'],
                data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body']
            )


def next_question(user_id, res):
    session = sessionStorage[user_id]
    if len(data['themes'][session['cur_theme']]['questions'][session['cur_dif']]) == \
            len(session['done'][session['cur_theme']]['count_quest']):
        if not switch_theme(user_id):
            send_results(user_id, res)
            return
    while True:
        num_quest = random.randrange(0, len(data['themes'][session['cur_theme']]['questions'][session['cur_dif']]))
        if not (num_quest in session['done'][session['cur_theme']]['count_quest']):
            break
    session['cur_quest'] = num_quest
    sessionStorage[user_id] = session


def switch_theme(user_id):
    session = sessionStorage[user_id]
    themes = data['themes'].keys()
    random.shuffle(themes)
    for i in themes:
        if len(session['done'][i]['count_quest']) == 0:
            session['cur_theme'] = i
            sessionStorage[user_id] = session
            return True
    sessionStorage[user_id] = session
    return False


def send_results(user_id, res):
    res['response']['text'] = "Молодец, пока!"


def get_suggests(user_id):
    session = sessionStorage[user_id]
    answers = data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['answers']
    random.shuffle(answers)
    suggests = [
        {'title': ans, 'hide': True}
        for ans in answers
    ]
    return suggests
