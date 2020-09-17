from ctypes.wintypes import *
from ctypes import *

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
# 단타 도우미 models
from django.utils import timezone

# 윈도우 메시지 상수 선언
DT_SINGLELINE = 32
DT_CENTER = 1
DT_VCENTER = 4

CW_USEDEFAULT = -2147483648
IDI_APPLICATION = 32512
WS_OVERLAPPEDWINDOW = 13565952

CS_HREDRAW = 2
CS_VREDRAW = 1

IDC_ARROW = 32512
WHITE_BRUSH = 0

SW_SHOWNORMAL = 1

WM_USER = 1024
CA_WMCAEVENT = WM_USER + 8400  # wmca.dll에서 수신한 윈도우 메시지를 핸들러로 각 이벤트 분기 처리
CA_CONNECTED = WM_USER + 110  # 로그인 성공
CA_DISCONNECTED = WM_USER + 120  # 접속 끊김
CA_SOCKETERROR = WM_USER + 130  # 통신 오류 발생
CA_RECEIVEDATA = WM_USER + 210  # 서비스 응답 수신(TR)
CA_RECEIVESISE = WM_USER + 220  # 실시간 데이터 수신(BC)
CA_RECEIVEMESSAGE = WM_USER + 230  # 상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨)
CA_RECEIVECOMPLETE = WM_USER + 240  # 서비스 처리 완료
CA_RECEIVEERROR = WM_USER + 250  # 서비스 처리중 오류 발생 (입력값 오류등)
ON_TASKBAR_NOTIFY = WM_USER + 20

# class FlipperHelper(models.Model):
#     investmentable_amount = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)  # 투자 가능 금액(증권사 입금 금액)
#     investment_amount = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)  # 투자 시점 금액
#     min_limit_percent = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')])  # 총 손절 마지노선 (%)
#     max_limit_percent = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')])  # 총 익절 마지노선 (%)
#     investment_now_amount = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)  # 투자 후 현재 금액(변동)
#     min_limit_now_percent = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')])  # 투자 후 현재 금액(변동)의 손절 마지노선 (%)
#     max_limit_now_percent = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')])  # 투자 후 현재 금액(변동)의 익절 마지노선 (%)


INPUT_PARM, OUTPUT_PARAM, INPUT_PARM_DEFAULT_ZERO = 1, 2, 4


class MsgHeaderStruct(Structure):
    _fields_ = [('msg_cd', CHAR * 5),
                ('user_msg', CHAR * 80)]


class ReceivedStruct(Structure):
    _fields_ = [('szBlockName', LPSTR),
                ('szData', LPSTR),
                ('nLen', INT)]


class OutdatablockStruct(Structure):
    _fields_ = [('TrIndex', INT),
                ('pData', POINTER(ReceivedStruct))]
