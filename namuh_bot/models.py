from ctypes import *
from ctypes.wintypes import *

"""
AGENT MODEL START
"""
# 윈도우 메시지 상수 선언
DT_SINGLELINE = 32
DT_CENTER = 1
DT_VCENTER = 4

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

# windows tray
MENU_EXIT = 1025

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


class c1101OutBlockStruct(Structure):
    _pack_ = 1
    _fields_ = [("code", CHAR * 6),  # 종목코드
                ("hname", CHAR * 13),  # 종목명
                ("price", CHAR * 7),  # 현재가
                ("sign", CHAR * 1),  # 등락부호 0x18 :상한, 0x1E :상승, 0x20 :보함, 0x19 :하한, 0x1F :하락, 등락부호는 시장과 관계없이 동일한 코드체계 사용
                ("change", CHAR * 6),  # 등락폭
                ("chrate", CHAR * 5),  # 등락률
                ("offer", CHAR * 7),  # 매도호가
                ("bid", CHAR * 7),  # 매수호가
                ("volume", CHAR * 9),  # 거래량
                ("volrate", CHAR * 6),  # 거래비율
                ("yurate", CHAR * 5),  # 유동주회전율
                ("value", CHAR * 9),  # 거래대금
                ("uplmtprice", CHAR * 7),  # 상한가
                ("high", CHAR * 7),  # 장중고가
                ("open", CHAR * 7),  # 시가
                ("opensign", CHAR * 1),  # 시가대비부호
                ("openchange", CHAR * 6),  # 시가대비등락폭
                ("low", CHAR * 7),  # 장중저가
                ("dnlmtprice", CHAR * 7),  # 하한가
                ("hotime", CHAR * 8),  # 호가시간
                ("offerho", CHAR * 7),  # 매도최우선호가
                ("P_offer", CHAR * 7),  # 매도차선호가
                ("S_offer", CHAR * 7),  # 매도차차선호가
                ("S4_offer", CHAR * 7),  # 매도4차선호가
                ("S5_offer", CHAR * 7),  # 매도5차선호가
                ("S6_offer", CHAR * 7),  # 매도6차선호가
                ("S7_offer", CHAR * 7),  # 매도7차선호가
                ("S8_offer", CHAR * 7),  # 매도8차선호가
                ("S9_offer", CHAR * 7),  # 매도9차선호가
                ("S10_offer", CHAR * 7),  # 매도10차선호가
                ("bidho", CHAR * 7),  # 매수최우선호가
                ("P_bid", CHAR * 7),  # 매수차선호가
                ("S_bid", CHAR * 7),  # 매수차차선호가
                ("S4_bid", CHAR * 7),  # 매수4차선호가
                ("S5_bid", CHAR * 7),  # 매수5차선호가
                ("S6_bid", CHAR * 7),  # 매수6차선호가
                ("S7_bid", CHAR * 7),  # 매수7차선호가
                ("S8_bid", CHAR * 7),  # 매수8차선호가
                ("S9_bid", CHAR * 7),  # 매수9차선호가
                ("S10_bid", CHAR * 7),  # 매수10차선호가
                ("offerrem", CHAR * 9),  # 매도최우선잔량
                ("P_offerrem", CHAR * 9),  # 매도차선잔량
                ("S_offerrem", CHAR * 9),  # 매도차차선잔량
                ("S4_offerrem", CHAR * 9),  # 매도4차선잔량
                ("S5_offerrem", CHAR * 9),  # 매도5차선잔량
                ("S6_offerrem", CHAR * 9),  # 매도6차선잔량
                ("S7_offerrem", CHAR * 9),  # 매도7차선잔량
                ("S8_offerrem", CHAR * 9),  # 매도8차선잔량
                ("S9_offerrem", CHAR * 9),  # 매도9차선잔량
                ("S10_offerrem", CHAR * 9),  # 매도10차선잔량
                ("bidrem", CHAR * 9),  # 매수최우선잔량
                ("P_bidrem", CHAR * 9),  # 매수차선잔량
                ("S_bidrem", CHAR * 9),  # 매수차차선잔량
                ("S4_bidrem", CHAR * 9),  # 매수4차선잔량
                ("S5_bidrem", CHAR * 9),  # 매수5차선잔량
                ("S6_bidrem", CHAR * 9),  # 매수6차선잔량
                ("S7_bidrem", CHAR * 9),  # 매수7차선잔량
                ("S8_bidrem", CHAR * 9),  # 매수8차선잔량
                ("S9_bidrem", CHAR * 9),  # 매수9차선잔량
                ("S10_bidrem", CHAR * 9),  # 매수10차선잔량
                ("T_offerrem", CHAR * 9),  # 총매도잔량
                ("T_bidrem", CHAR * 9),  # 총매수잔량
                ("O_offerrem", CHAR * 9),  # 시간외매도잔량
                ("O_bidrem", CHAR * 9),  # 시간외매수잔량
                ("pivot2upz7", CHAR * 7),  # 피봇2차저항
                ("pivot1upz7", CHAR * 7),  # 피봇1차저항
                ("pivotz7", CHAR * 7),  # 피봇가
                ("pivot1dnz7", CHAR * 7),  # 피봇1차지지
                ("pivot2dnz7", CHAR * 7),  # 피봇2차지지
                ("sosokz6", CHAR * 6),  # 코스피코스닥구분
                ("jisunamez18", CHAR * 18),  # 업종명
                ("capsizez6", CHAR * 6),  # 자본금규모
                ("output1z16", CHAR * 16),  # 결산월
                ("marcket1z16", CHAR * 16),  # 시장조치1
                ("marcket2z16", CHAR * 16),  # 시장조치2
                ("marcket3z16", CHAR * 16),  # 시장조치3
                ("marcket4z16", CHAR * 16),  # 시장조치4
                ("marcket5z16", CHAR * 16),  # 시장조치5
                ("marcket6z16", CHAR * 16),  # 시장조치6
                ("cbtext", CHAR * 6),  # CB구분
                ("parvalue", CHAR * 7),  # 액면가
                ("prepricetitlez12", CHAR * 12),  # 전일종가타이틀
                ("prepricez7", CHAR * 7),  # 전일종가
                ("subprice", CHAR * 7),  # 대용가
                ("gongpricez7", CHAR * 7),  # 공모가
                ("high5", CHAR * 7),  # 5일고가
                ("low5", CHAR * 7),  # 5일저가
                ("high20", CHAR * 7),  # 20일고가
                ("low20", CHAR * 7),  # 20일저가
                ("yhigh", CHAR * 7),  # 52주최고가
                ("yhighdate", CHAR * 4),  # 52주최고가일
                ("ylow", CHAR * 7),  # 52주최저가
                ("ylowdate", CHAR * 4),  # 52주최저가일
                ("movlistingz8", CHAR * 8),  # 유동주식수
                ("listing", CHAR * 12),  # 상장주식수
                ("totpricez9", CHAR * 9),  # 시가총액
                ("tratimez5", CHAR * 5),  # 시간
                ("off_tra1", CHAR * 6),  # 매도거래원1
                ("bid_tra1", CHAR * 6),  # 매수거래원1
                ("N_offvolume1", CHAR * 9),  # 매도거래량1
                ("N_bidvolume1", CHAR * 9),  # 매수거래량1
                ("off_tra2", CHAR * 6),  # 매도거래원2
                ("bid_tra2", CHAR * 6),  # 매수거래원2
                ("N_offvolume2", CHAR * 9),  # 매도거래량2
                ("N_bidvolume2", CHAR * 9),  # 매수거래량2
                ("off_tra3", CHAR * 6),  # 매도거래원3
                ("bid_tra3", CHAR * 6),  # 매수거래원3
                ("N_offvolume3", CHAR * 9),  # 매도거래량3
                ("N_bidvolume3", CHAR * 9),  # 매수거래량3
                ("off_tra4", CHAR * 6),  # 매도거래원4
                ("bid_tra4", CHAR * 6),  # 매수거래원4
                ("N_offvolume4", CHAR * 9),  # 매도거래량4
                ("N_bidvolume4", CHAR * 9),  # 매수거래량4
                ("off_tra5", CHAR * 6),  # 매도거래원5
                ("bid_tra5", CHAR * 6),  # 매수거래원5
                ("N_offvolume5", CHAR * 9),  # 매도거래량5
                ("N_bidvolume5", CHAR * 9),  # 매수거래량5
                ("N_offvolall", CHAR * 9),  # 매도외국인거래량
                ("N_bidvolall", CHAR * 9),  # 매수외국인거래량
                ("fortimez6", CHAR * 6),  # 외국인시간
                ("forratez5", CHAR * 5),  # 외국인지분율
                ("settdatez4", CHAR * 4),  # 결제일
                ("cratez5", CHAR * 5),  # 잔고비율(%)
                ("yudatez4", CHAR * 4),  # 유상기준일
                ("mudatez4", CHAR * 4),  # 무상기준일
                ("yuratez5", CHAR * 5),  # 유상배정비율
                ("muratez5", CHAR * 5),  # 무상배정비율
                ("formovolz10", CHAR * 10),  # 외국인변동주수
                ("jasa", CHAR * 1),  # 자사주
                ("listdatez8", CHAR * 8),  # 상장일
                ("daeratez5", CHAR * 5),  # 대주주지분율
                ("daedatez6", CHAR * 6),  # 대주주지분일자
                ("clovergb", CHAR * 1),  # 네잎클로버
                ("depositgb", CHAR * 1),  # 증거금율
                ("capital", CHAR * 9),  # 자본금
                ("N_alloffvol", CHAR * 9),  # 전체거래원매도합
                ("N_allbidvol", CHAR * 9),  # 전체거래원매수합
                ("hnamez21", CHAR * 21),  # 종목명2
                ("detourgb", CHAR * 1),  # 우회상장여부
                ("yuratez6", CHAR * 6),  # 유동주회전율2
                ("sosokz6_1", CHAR * 6),  # 코스피구분
                ("maedatez4", CHAR * 4),  # 공여율기준일
                ("lratez5", CHAR * 5),  # 공여율(%)
                ("perz5", CHAR * 5),  # PER
                ("handogb", CHAR * 1),  # 종목별신용한도
                ("avgprice", CHAR * 7),  # 가중가
                ("listing2", CHAR * 12),  # 상장주식수_주
                ("addlisting", CHAR * 12),  # 추가상장주수
                ("gicomment", CHAR * 100),  # 종목comment
                ("prevolume", CHAR * 9),  # 전일거래량
                ("presign", CHAR * 1),  # 전일대비등락부호
                ("prechange", CHAR * 6),  # 전일대비등락폭
                ("yhigh2", CHAR * 7),  # 연종최고가
                ("yhighdate2", CHAR * 4),  # 연중최고가일
                ("ylow2", CHAR * 7),  # 연중최저가
                ("ylowdate2", CHAR * 4),  # 연중최저가일
                ("forstock", CHAR * 15),  # 외국인보유주식수
                ("forlmtz5", CHAR * 5),  # 외국인한도율(%)
                ("maeunit", CHAR * 5),  # 매매수량단위
                ("mass_opt", CHAR * 1),  # 경쟁대량방향구분
                ("largemgb", CHAR * 1),  # 대량매매구분
                ("pbrz5", CHAR * 5),  # PBR
                ("dmrs_val", CHAR * 7),  # 디저항값
                ("dmsp_val", CHAR * 7),  # 디지지값
                ("prevalue", CHAR * 9),  # 전일거래대금
                ("vi_recprice", CHAR * 7),  # VI기준가
                ("vi_hprice", CHAR * 7),  # VI상승발동가
                ("vi_lprice", CHAR * 7),  # VI하락발동가
                ]

    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__,
                                   ", \n".join(["{}: {}".format(field[0],
                                                                getattr(self,
                                                                        field[0]))
                                                for field in self._fields_]))


class c1101OutBlock2Struct(Structure):
    _pack_ = 1
    _fields_ = [("time", CHAR * 8),  # 시간
                ("price", CHAR * 7),  # 현재가
                ("sign", CHAR * 1),  # 등락부호
                ("change", CHAR * 6),  # 등락폭
                ("offer", CHAR * 7),  # 매도호가
                ("bid", CHAR * 7),  # 매수호가
                ("movolume", CHAR * 8),  # 변동거래량
                ("volume", CHAR * 9),  # 거래량
                ]
    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__,
                                   ", \n".join(["{}: {}".format(field[0],
                                                                getattr(self,
                                                                        field[0]))
                                                for field in self._fields_]))

class c1101OutBlock3Struct(Structure):
    _pack_ = 1
    _fields_ = [("dongsi", CHAR * 1),  # 동시호가구분
                ("jeqprice", CHAR * 7),  # 예상체결가
                ("jeqsign", CHAR * 1),  # 예상체결부호
                ("jeqchange", CHAR * 6),  # 예상체결등락폭
                ("jeqchrate", CHAR * 5),  # 예상체결등락률
                ("jeqvol", CHAR * 9),  # 예상체결수량
                ("chkdataz1", CHAR * 1),  # ECN정보유무구분
                ("ecn_price", CHAR * 9),  # ECN전일종가
                ("ecn_sign", CHAR * 1),  # ECN부호
                ("ecn_change", CHAR * 9),  # ECN등락폭
                ("ecn_chrate", CHAR * 5),  # ECN등락률
                ("ecn_volume", CHAR * 10),  # ECN체결수량
                ("ecn_jeqsign", CHAR * 1),  # ECN대비예상체결부호
                ("ecn_jeqchange", CHAR * 6),  # ECN대비예상체결등락폭
                ("ecn_jeqchrate", CHAR * 5),  # ECN대비예상체결등락률
                ]
    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__,
                                   ", \n".join(["{}: {}".format(field[0],
                                                                getattr(self,
                                                                        field[0]))
                                                for field in self._fields_]))

class c1101OutBlock_Struct(Structure):
    _fields_ = []


"""
AGENT MODEL END
"""

"""
WEB MODEL START
"""

# 종목코드 모델
# class StockCd(models.Model):
#     # http://kind.krx.co.kr/corpgeneral/corpList.do?method=download (한국 거래소에서 종목 코드 리스트 수집)
#     #     opening_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
#     cd = models.CharField(max_length=6, primary_key=True)
#     nm = models.CharField(max_length=100)


"""
WEB MODEL END 
"""
