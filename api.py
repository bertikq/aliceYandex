from __future__ import unicode_literals
import random
from dialogs import data
import json
from flask import Flask, request

app = Flask(__name__)
sessionStorage = {}


@app.route("/", methods=['POST'])
def main():
    print("HELLO!")
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
            'cur_theme': 'общая',
            'cur_quest': 0,
            'cur_dif': 0,
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
    if not (req['request']['original_utterance'].lower() in
            data['themes'][session['cur_theme']]['questions'][session['cur_quest']]['answers']):
        res['response']['text'] = data['samples']['quest_repeat'].format("\n".join([
            "{}. {}".format(i + 1, item)
            for i, item in enumerate(data['themes'][session['cur_theme']]['questions'][session['cur_quest']]['answers'])
        ]))
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() == data['themes'][session['cur_theme']]['questions'][session['cur_quest']]['answers'][0]:
        win_answer(user_id, res)
        return
    lose_answer(user_id, res)


def win_answer(user_id, res):
    session = sessionStorage[user_id]
    session['done']['общая']['count_quest'].add(session['cur_quest'])
    session['cur_dif'] += 1
    session['count_win_quests'] += 1
    sessionStorage[user_id] = session
    next_question(user_id)
    write_response(user_id, res, True)


def lose_answer(user_id, res):
    session = sessionStorage[user_id]
    session['done']['общая']['count_quest'].add(session['cur_quest'])
    session['cur_dif'] = 0
    session['count_lose_quests'] += 1
    sessionStorage[user_id] = session
    next_question(user_id)
    write_response(user_id, res, False)


def start_dialog(user_id, res):
    session = sessionStorage[user_id]
    session['done']['общая'] = {'count_quest': set()}
    sessionStorage[user_id] = session
    next_question(user_id)
    res['response']['text'] = '''
        Первый вопрос.
        {}
        Варианты ответов:
        {}
    '''.format(
        data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body'],
        "\n".join(["{}. {}".format(i + 1, item) for i, item in enumerate(data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['answers'])])
    )
    res['response']['buttons'] = get_suggests(user_id)


def write_response(user_id, res, isWin):
    session = sessionStorage[user_id]
    res['response']['text'] = \
        data['samples']['win_ans'].format(
            session['cur_theme'],
            data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body'],
            "\n".join(["{}. {}".format(i + 1, item) for i, item in enumerate(data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['answers'])])
        ) if isWin else \
        data['samples']['lose_ans'].format(
            data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['resource'],
            session['cur_theme'],
            data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['body'],
            "\n".join(["{}. {}".format(i + 1, item) for i, item in enumerate(data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['answers'])])
        )
    res['response']['buttons'] = get_suggests(user_id)


def next_question(user_id):
    session = sessionStorage[user_id]
    if len(session['done'][session['cur_theme']]['count_quest']) > 3:
        if not switch_theme(user_id):
            send_results(user_id)
        return
    while True:
        num_quest = random.randrange(0, len(data['themes'][session['cur_theme']]['questions'][session['cur_dif']]) - 1)
        if not (num_quest in session['done'][session['cur_theme']]['count_quest']):
            break
    session['cur_quest'] = num_quest
    sessionStorage[user_id] = session


def switch_theme(user_id):
    session = sessionStorage[user_id]
    themes = data['themes'].keys()
    random.shuffle(themes)
    for i in themes:
        session['done'][i] = session['done'].get(i, default={'count_quest': []})
        if len(session['done'][i]['count_quest']) == 0:
            session['cur_theme'] = i
            session['cur_dif'] = 0
            sessionStorage[user_id] = session
            return True
    sessionStorage[user_id] = session
    return False


def send_results(user_id):
    pass


def get_suggests(user_id):
    session = sessionStorage[user_id]
    answers = data['themes'][session['cur_theme']]['questions'][session['cur_dif']][session['cur_quest']]['answers']
    random.shuffle(answers)
    suggests = [
        {'title': ans, 'hide': True}
        for ans in answers
    ]
    return suggests
