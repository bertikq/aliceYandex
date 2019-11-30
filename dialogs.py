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
                        'answers': "распределённая система управления версиями. Проект был создан Линусом Торвальдсом для управления разработкой ядра Linux, первая версия выпущена 7 апреля 2005 года. На сегодняшний день его поддерживает Джунио Хамано.",
                        'resource': 'https://ru.wikipedia.org/wiki/Yes_(%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0)',
                    }
                ]
            ]
        }
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