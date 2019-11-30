def equals(answer, info):
    masAnswer = set(answer.split(' '))
    masInfo = set(info.split(' '))
    infoCountWord = len(masInfo) / 2
    countEqualWords = 0.0
    for word in masInfo:
        if masAnswer.__contains__(word):
            countEqualWords += 1
    return countEqualWords / infoCountWord


