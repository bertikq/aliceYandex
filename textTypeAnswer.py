def equals(answer, info):
    masAnswer = set(answer.split(' '))
    masInfo = set(info.split(' '))
    infoCountWord = len(masAnswer)
    countEqualWords = 0.0
    for word in masAnswer:
        if word in masInfo:
            countEqualWords += 1
    return countEqualWords / infoCountWord


