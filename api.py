# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

import random

from dialogs import data

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {
    'user_id': {
        
    }
}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Ну начнем",
                "Погнали",
            ],
            'cur_theme': 'default',
            'cur_quest': 0,
            'done': {
                'default': {
                    'quest_num': []
                }
            },
            'count_win_quests': 0,
            'count_lose_quests': 0,
        }

        res['response']['text'] = 'Привет, давай начнем собеседование!'
        res['response']['buttons'] = [
            {'title': startButton, 'hide': True}
            for startButton in sessionStorage[user_id]['suggests']
        ]
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        "Ну начнем",
        "погнали",
    ]:
        start_dialog(user_id, res)
        res['response']['text'] = 'test'
        return
    res['response']['text'] = 'Выберете предложенный ответ'
    return
    
    
def start_dialog(user_id, res):
    session = sessionStorage[user_id]
    next_question(user_id)
    res['response']['text'] = data[session['cur_theme']]['questions'][session['cur_quest']]
    res['response']['buttons'] = get_suggests(user_id)

def next_question(user_id):
    session = sessionStorage[user_id]
    if (session['done'][session['cur_theme']]['quest_num'].__len__() > 3):
        switch_theme(user_id)
        return
    num_quest = -1
    while (True):
        num_quest = random.randrange(0, data['themes'][session['cur_theme']]['questions'].__len__() - 1)
        if (not num_quest in session['done'][session['cur_theme']]['quest_num']):
            break
    session['cur_quest'] = num_quest


def switch_theme(user_id):
    return

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests = [
        {'title': ans, 'hide': True}
        for ans in data['themes'][session['cur_theme']]['questions'][session['cur_quest']]['answers']
    ]
    return suggests