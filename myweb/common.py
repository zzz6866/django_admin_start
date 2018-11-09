import time


# 활동로그를 기록하는 함수
def printLog(logText, type):
    # 현재 시간 셋팅
    now = time.localtime()
    nowTime = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    nowDay = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

    # 로그를 기록 저장
    logText = "[" + nowTime + "] " + str(logText) + "\n"
    if type == "W":
        log = open(nowDay + "_log.txt", "a", encoding="utf-8")
        log.write(logText)
        log.close()
    elif type == "P":
        print(logText)
    else:
        print("Not Match Type")
