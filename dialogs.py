data = {
    'themes': {
        'default': {
            'questions': [
                {
                    'body': 'is it possible?',
                    'answers': ['yes', 'no'],
                    'resources': [
                        'https://ru.wikipedia.org/wiki/Yes_(%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0)',
                    ],
                    'next_quest': [
                        -1, 
                    ]
                },
                {
                    'body': 'Its TEst2?',
                    'answers': ['TEst', 'NOTESTno'],
                    'resources': [
                        'https://ru.wikipedia.org/wiki/Yes_(%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0)',
                    ],
                    'next_quest': [
                        -1,
                    ]
                }
            ]
        }
    },
    'sample_answer': {
        'win_ans': '''
            Это правильный ответ!
            Следующий вопрос...
        ''',
        'lose_ans': '''
            Это неправильный ответ!
            Ты можешь почитать про это поподробнее: {}
            Следующий вопрос...
        ''',
        'quest_ans': '''
            Тема: {}
            Вопрос: {}
        '''
    }
}