data = {
    'themes': {
        'общая': {
            'questions': [
                [
                    {
                        'type': 'simple',
                        'body': 'Ты тут?',
                        'answers': ['да', 'нет'],
                        'resource': 'https://ru.wikipedia.org/wiki/Yes_(%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0)',
                    },
                    {
                        'type': 'simple',
                        'body': 'Ты меня слышишь?',
                        'answers': ['да', 'нет', 'наверное'],
                        'resource': 'https://ru.wikipedia.org/wiki/Yes_(%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0)',
                    },
                    {
                        'type': 'text',
                        'body': 'Как ты понимаешь что такое гит?',
                        'answers': "распределённая система управления версиями Системы контроля версий (СКВ, VCS, "
                                   "Version Control Systems) позволяют разработчикам сохранять все изменения, "
                                   "внесённые в код. Поэтому в случае, описанном выше, они могут просто откатить код "
                                   "до рабочего состояния вместо того, чтобы тратить часы на поиски маленькой ошибки "
                                   "или ошибок, ломающих весь код.СКВ также дают возможность нескольким разработчикам "
                                   "работать над одним проектом и сохранять внесённые изменения, чтобы убедиться, "
                                   "что все могут следить за тем, над чем они работают.Существует три типа СКВ: "
                                   "локальная, централизованная и распределённая.",
                        'resource': 'https://ru.wikipedia.org/wiki/Yes_(%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0)',
                    }
                ],
                [],
                [
                    {
                        'type': 'simple',
                        'body': 'Сколько шариков для гольфа поместится в школьный автобус?',
                        'answers': ['около 500 тысяч', "около 2-х миллионов", "около 5-ти миллионов"],
                        'resource': "https://tproger.ru/problems/golf-balls-is-school-bus/"
                    }
                ]
            ]
        },
        'git': {},
        'алгоритмы': {}
    },
    'samples': {
        'win_ans': '''
            Это правильный ответ!
            Следующий вопрос...
            {}
            Варианты ответов:
            {}
        ''',
        'lose_ans': '''
            Это неправильный ответ!
            Ты можешь почитать про это поподробнее: {}
            Следующий вопрос...
            {}
            Варианты ответов:
            {}
        ''',
        'quest_repeat': '''
            Используй только предложенные варианты ответов. Возможно, я не расслышала твой ответ.
            Повторю варианты ответов:
            {}
        ''',
    }
}