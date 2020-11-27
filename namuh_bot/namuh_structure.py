# -*- coding: utf-8 -*-
from ctypes import *
from ctypes.wintypes import *

from mirage.crypto import Crypto

from alldev.settings.base import SECRET_KEY

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

INPUT_PARM, OUTPUT_PARAM, INPUT_PARM_DEFAULT_ZERO = 1, 2, 4


class StructBase(object):
    def __get_value_str(self, name, fmt='{}'):
        val = getattr(self, name)
        if isinstance(val, Array):
            val = list(val)
        return fmt.format(val)

    def __str__(self):
        result = '{}:\n'.format(self.__class__.__name__)
        maxname = max(len(name) for name, type_ in self._fields_)
        for name, type_ in self._fields_:
            value = getattr(self, name)
            result += ' {name:<{width}}: {value}\n'.format(
                name=name,
                width=maxname,
                value=self.__get_value_str(name),
            )
        return result

    def __repr__(self):
        return '{name}({fields})'.format(
            name=self.__class__.__name__,
            fields=', '.join(
                '{}={}'.format(name, self.__get_value_str(name, '{!r}')) for name, _ in self._fields_)
        )

    @classmethod
    def _typeof(cls, field):
        """Get the type of a field
        Example: A._typeof(A.fld)
        Inspired by stackoverflow.com/a/6061483
        """
        for name, type_ in cls._fields_:
            if getattr(cls, name) is field:
                return type_
        raise KeyError

    @classmethod
    def read_from(cls, f):
        result = cls()
        if f.readinto(result) != sizeof(cls):
            raise EOFError
        return result

    def get_bytes(self):
        """Get raw byte string of this LittleEndianStructure, StructHelper
        ctypes.LittleEndianStructure, StructHelper implements the buffer interface, so it can be used
        directly anywhere the buffer interface is implemented.
        https://stackoverflow.com/q/1825715
        """

        # Works for either Python2 or Python3
        return bytearray(self)

        # Python 3 only! Don't try this in Python2, where bytes() == str()
        # return bytes(self)

    def get_str(self, field_name):
        value = object.__getattribute__(self, field_name)
        return value.decode("cp949")

    def get_dict(self):  # 배열 반환
        return dict((f, self.get_str(f)) for f, _ in self._fields_)


class StructByteBase(StructBase):  # 데이터 구조체가 +1byte 추가된 경우 끝을 짤라서 반환
    _pack_ = 1  # 데이터 반환이 byte 단위로 들어오기 때문에 필드(fields) 순서대로 받아야 함

    def get_str(self, field_name):
        value = object.__getattribute__(self, field_name)
        if len(value) > 0:
            if value[:-1].decode("cp949").isdigit() and value[-1:] != b" ":
                return int(value[:-1].decode("cp949"))
            else:  # if value[-1:] == b" ":  # 끝이 공백 일 경우 문자열 -1 제거 후 반환
                return str(value[:-1].decode("cp949")).strip()
        else:  # 0byte일 경우 공백 반환
            return ""


# class StructProperty:
# def __setattr__(self, attr, value):
#     object.__setattr__(self, attr, str(value[:len(value) - 1]))
# def __getattribute__(self, attr):
#     return str(object.__getattribute__(self, attr).decode("cp949")).strip()


class MsgHeaderStruct(LittleEndianStructure, StructBase):
    _fields_ = [('msg_cd', CHAR * 5),
                ('user_msg', CHAR * 80)
                ]


class ReceivedStruct(LittleEndianStructure, StructBase):
    _fields_ = [('szBlockName', LPSTR),
                ('szData', LPSTR),
                ('nLen', INT)
                ]


class OutdatablockStruct(LittleEndianStructure, StructBase):
    _fields_ = [('TrIndex', INT),
                ('pData', POINTER(ReceivedStruct))
                ]


class C1101OutBlockStruct(LittleEndianStructure, StructByteBase):
    _fields_ = [("code", CHAR * (6 + 1)),  # 종목코드
                ("hname", CHAR * (13 + 1)),  # 종목명
                ("price", CHAR * (7 + 1)),  # 현재가
                ("sign", CHAR * (1 + 1)),  # 등락부호 0x18 :상한, 0x1E :상승, 0x20 :보함, 0x19 :하한, 0x1F :하락, 등락부호는 시장과 관계없이 동일한 코드체계 사용
                ("change", CHAR * (6 + 1)),  # 등락폭
                ("chrate", CHAR * (5 + 1)),  # 등락률
                ("offer", CHAR * (7 + 1)),  # 매도호가
                ("bid", CHAR * (7 + 1)),  # 매수호가
                ("volume", CHAR * (9 + 1)),  # 거래량
                ("volrate", CHAR * (6 + 1)),  # 거래비율
                ("yurate", CHAR * (5 + 1)),  # 유동주회전율
                ("value", CHAR * (9 + 1)),  # 거래대금
                ("uplmtprice", CHAR * (7 + 1)),  # 상한가
                ("high", CHAR * (7 + 1)),  # 장중고가
                ("open", CHAR * (7 + 1)),  # 시가
                ("opensign", CHAR * (1 + 1)),  # 시가대비부호
                ("openchange", CHAR * (6 + 1)),  # 시가대비등락폭
                ("low", CHAR * (7 + 1)),  # 장중저가
                ("dnlmtprice", CHAR * (7 + 1)),  # 하한가
                ("hotime", CHAR * (8 + 1)),  # 호가시간
                ("offerho", CHAR * (7 + 1)),  # 매도최우선호가
                ("P_offer", CHAR * (7 + 1)),  # 매도차선호가
                ("S_offer", CHAR * (7 + 1)),  # 매도차차선호가
                ("S4_offer", CHAR * (7 + 1)),  # 매도4차선호가
                ("S5_offer", CHAR * (7 + 1)),  # 매도5차선호가
                ("S6_offer", CHAR * (7 + 1)),  # 매도6차선호가
                ("S7_offer", CHAR * (7 + 1)),  # 매도7차선호가
                ("S8_offer", CHAR * (7 + 1)),  # 매도8차선호가
                ("S9_offer", CHAR * (7 + 1)),  # 매도9차선호가
                ("S10_offer", CHAR * (7 + 1)),  # 매도10차선호가
                ("bidho", CHAR * (7 + 1)),  # 매수최우선호가
                ("P_bid", CHAR * (7 + 1)),  # 매수차선호가
                ("S_bid", CHAR * (7 + 1)),  # 매수차차선호가
                ("S4_bid", CHAR * (7 + 1)),  # 매수4차선호가
                ("S5_bid", CHAR * (7 + 1)),  # 매수5차선호가
                ("S6_bid", CHAR * (7 + 1)),  # 매수6차선호가
                ("S7_bid", CHAR * (7 + 1)),  # 매수7차선호가
                ("S8_bid", CHAR * (7 + 1)),  # 매수8차선호가
                ("S9_bid", CHAR * (7 + 1)),  # 매수9차선호가
                ("S10_bid", CHAR * (7 + 1)),  # 매수10차선호가
                ("offerrem", CHAR * (9 + 1)),  # 매도최우선잔량
                ("P_offerrem", CHAR * (9 + 1)),  # 매도차선잔량
                ("S_offerrem", CHAR * (9 + 1)),  # 매도차차선잔량
                ("S4_offerrem", CHAR * (9 + 1)),  # 매도4차선잔량
                ("S5_offerrem", CHAR * (9 + 1)),  # 매도5차선잔량
                ("S6_offerrem", CHAR * (9 + 1)),  # 매도6차선잔량
                ("S7_offerrem", CHAR * (9 + 1)),  # 매도7차선잔량
                ("S8_offerrem", CHAR * (9 + 1)),  # 매도8차선잔량
                ("S9_offerrem", CHAR * (9 + 1)),  # 매도9차선잔량
                ("S10_offerrem", CHAR * (9 + 1)),  # 매도10차선잔량
                ("bidrem", CHAR * (9 + 1)),  # 매수최우선잔량
                ("P_bidrem", CHAR * (9 + 1)),  # 매수차선잔량
                ("S_bidrem", CHAR * (9 + 1)),  # 매수차차선잔량
                ("S4_bidrem", CHAR * (9 + 1)),  # 매수4차선잔량
                ("S5_bidrem", CHAR * (9 + 1)),  # 매수5차선잔량
                ("S6_bidrem", CHAR * (9 + 1)),  # 매수6차선잔량
                ("S7_bidrem", CHAR * (9 + 1)),  # 매수7차선잔량
                ("S8_bidrem", CHAR * (9 + 1)),  # 매수8차선잔량
                ("S9_bidrem", CHAR * (9 + 1)),  # 매수9차선잔량
                ("S10_bidrem", CHAR * (9 + 1)),  # 매수10차선잔량
                ("T_offerrem", CHAR * (9 + 1)),  # 총매도잔량
                ("T_bidrem", CHAR * (9 + 1)),  # 총매수잔량
                ("O_offerrem", CHAR * (9 + 1)),  # 시간외매도잔량
                ("O_bidrem", CHAR * (9 + 1)),  # 시간외매수잔량
                ("pivot2upz7", CHAR * (7 + 1)),  # 피봇2차저항
                ("pivot1upz7", CHAR * (7 + 1)),  # 피봇1차저항
                ("pivotz7", CHAR * (7 + 1)),  # 피봇가
                ("pivot1dnz7", CHAR * (7 + 1)),  # 피봇1차지지
                ("pivot2dnz7", CHAR * (7 + 1)),  # 피봇2차지지
                ("sosokz6", CHAR * (6 + 1)),  # 코스피코스닥구분
                ("jisunamez18", CHAR * (18 + 1)),  # 업종명
                ("capsizez6", CHAR * (6 + 1)),  # 자본금규모
                ("output1z16", CHAR * (16 + 1)),  # 결산월
                ("marcket1z16", CHAR * (16 + 1)),  # 시장조치1
                ("marcket2z16", CHAR * (16 + 1)),  # 시장조치2
                ("marcket3z16", CHAR * (16 + 1)),  # 시장조치3
                ("marcket4z16", CHAR * (16 + 1)),  # 시장조치4
                ("marcket5z16", CHAR * (16 + 1)),  # 시장조치5
                ("marcket6z16", CHAR * (16 + 1)),  # 시장조치6
                ("cbtext", CHAR * (6 + 1)),  # CB구분
                ("parvalue", CHAR * (7 + 1)),  # 액면가
                ("prepricetitlez12", CHAR * (12 + 1)),  # 전일종가타이틀
                ("prepricez7", CHAR * (7 + 1)),  # 전일종가
                ("subprice", CHAR * (7 + 1)),  # 대용가
                ("gongpricez7", CHAR * (7 + 1)),  # 공모가
                ("high5", CHAR * (7 + 1)),  # 5일고가
                ("low5", CHAR * (7 + 1)),  # 5일저가
                ("high20", CHAR * (7 + 1)),  # 20일고가
                ("low20", CHAR * (7 + 1)),  # 20일저가
                ("yhigh", CHAR * (7 + 1)),  # 52주최고가
                ("yhighdate", CHAR * (4 + 1)),  # 52주최고가일
                ("ylow", CHAR * (7 + 1)),  # 52주최저가
                ("ylowdate", CHAR * (4 + 1)),  # 52주최저가일
                ("movlistingz8", CHAR * (8 + 1)),  # 유동주식수
                ("listing", CHAR * (12 + 1)),  # 상장주식수
                ("totpricez9", CHAR * (9 + 1)),  # 시가총액
                ("tratimez5", CHAR * (5 + 1)),  # 시간
                ("off_tra1", CHAR * (6 + 1)),  # 매도거래원1
                ("bid_tra1", CHAR * (6 + 1)),  # 매수거래원1
                ("N_offvolume1", CHAR * (9 + 1)),  # 매도거래량1
                ("N_bidvolume1", CHAR * (9 + 1)),  # 매수거래량1
                ("off_tra2", CHAR * (6 + 1)),  # 매도거래원2
                ("bid_tra2", CHAR * (6 + 1)),  # 매수거래원2
                ("N_offvolume2", CHAR * (9 + 1)),  # 매도거래량2
                ("N_bidvolume2", CHAR * (9 + 1)),  # 매수거래량2
                ("off_tra3", CHAR * (6 + 1)),  # 매도거래원3
                ("bid_tra3", CHAR * (6 + 1)),  # 매수거래원3
                ("N_offvolume3", CHAR * (9 + 1)),  # 매도거래량3
                ("N_bidvolume3", CHAR * (9 + 1)),  # 매수거래량3
                ("off_tra4", CHAR * (6 + 1)),  # 매도거래원4
                ("bid_tra4", CHAR * (6 + 1)),  # 매수거래원4
                ("N_offvolume4", CHAR * (9 + 1)),  # 매도거래량4
                ("N_bidvolume4", CHAR * (9 + 1)),  # 매수거래량4
                ("off_tra5", CHAR * (6 + 1)),  # 매도거래원5
                ("bid_tra5", CHAR * (6 + 1)),  # 매수거래원5
                ("N_offvolume5", CHAR * (9 + 1)),  # 매도거래량5
                ("N_bidvolume5", CHAR * (9 + 1)),  # 매수거래량5
                ("N_offvolall", CHAR * (9 + 1)),  # 매도외국인거래량
                ("N_bidvolall", CHAR * (9 + 1)),  # 매수외국인거래량
                ("fortimez6", CHAR * (6 + 1)),  # 외국인시간
                ("forratez5", CHAR * (5 + 1)),  # 외국인지분율
                ("settdatez4", CHAR * (4 + 1)),  # 결제일
                ("cratez5", CHAR * (5 + 1)),  # 잔고비율(%)
                ("yudatez4", CHAR * (4 + 1)),  # 유상기준일
                ("mudatez4", CHAR * (4 + 1)),  # 무상기준일
                ("yuratez5", CHAR * (5 + 1)),  # 유상배정비율
                ("muratez5", CHAR * (5 + 1)),  # 무상배정비율
                ("formovolz10", CHAR * (10 + 1)),  # 외국인변동주수
                ("jasa", CHAR * (1 + 1)),  # 자사주
                ("listdatez8", CHAR * (8 + 1)),  # 상장일
                ("daeratez5", CHAR * (5 + 1)),  # 대주주지분율
                ("daedatez6", CHAR * (6 + 1)),  # 대주주지분일자
                ("clovergb", CHAR * (1 + 1)),  # 네잎클로버
                ("depositgb", CHAR * (1 + 1)),  # 증거금율
                ("capital", CHAR * (9 + 1)),  # 자본금
                ("N_alloffvol", CHAR * (9 + 1)),  # 전체거래원매도합
                ("N_allbidvol", CHAR * (9 + 1)),  # 전체거래원매수합
                ("hnamez21", CHAR * (21 + 1)),  # 종목명2
                ("detourgb", CHAR * (1 + 1)),  # 우회상장여부
                ("yuratez6", CHAR * (6 + 1)),  # 유동주회전율2
                ("sosokz6_1", CHAR * (6 + 1)),  # 코스피구분
                ("maedatez4", CHAR * (4 + 1)),  # 공여율기준일
                ("lratez5", CHAR * (5 + 1)),  # 공여율(%)
                ("perz5", CHAR * (5 + 1)),  # PER
                ("handogb", CHAR * (1 + 1)),  # 종목별신용한도
                ("avgprice", CHAR * (7 + 1)),  # 가중가
                ("listing2", CHAR * (12 + 1)),  # 상장주식수_주
                ("addlisting", CHAR * (12 + 1)),  # 추가상장주수
                ("gicomment", CHAR * (100 + 1)),  # 종목comment
                ("prevolume", CHAR * (9 + 1)),  # 전일거래량
                ("presign", CHAR * (1 + 1)),  # 전일대비등락부호
                ("prechange", CHAR * (6 + 1)),  # 전일대비등락폭
                ("yhigh2", CHAR * (7 + 1)),  # 연종최고가
                ("yhighdate2", CHAR * (4 + 1)),  # 연중최고가일
                ("ylow2", CHAR * (7 + 1)),  # 연중최저가
                ("ylowdate2", CHAR * (4 + 1)),  # 연중최저가일
                ("forstock", CHAR * (15 + 1)),  # 외국인보유주식수
                ("forlmtz5", CHAR * (5 + 1)),  # 외국인한도율(%)
                ("maeunit", CHAR * (5 + 1)),  # 매매수량단위
                ("mass_opt", CHAR * (1 + 1)),  # 경쟁대량방향구분
                ("largemgb", CHAR * (1 + 1)),  # 대량매매구분
                ("pbrz5", CHAR * (5 + 1)),  # PBR
                ("dmrs_val", CHAR * (7 + 1)),  # 디저항값
                ("dmsp_val", CHAR * (7 + 1)),  # 디지지값
                ("prevalue", CHAR * (9 + 1)),  # 전일거래대금
                ("vi_recprice", CHAR * (7 + 1)),  # VI기준가
                ("vi_hprice", CHAR * (7 + 1)),  # VI상승발동가
                ("vi_lprice", CHAR * (7 + 1)),  # VI하락발동가
                ]


class C1101OutBlock2Struct(LittleEndianStructure, StructByteBase):
    _fields_ = [("time", CHAR * (8 + 1)),  # 시간
                ("price", CHAR * (7 + 1)),  # 현재가
                ("sign", CHAR * (1 + 1)),  # 등락부호
                ("change", CHAR * (6 + 1)),  # 등락폭
                ("offer", CHAR * (7 + 1)),  # 매도호가
                ("bid", CHAR * (7 + 1)),  # 매수호가
                ("movolume", CHAR * (8 + 1)),  # 변동거래량
                ("volume", CHAR * (9 + 1)),  # 거래량
                ]


class C1101OutBlock3Struct(LittleEndianStructure, StructByteBase):
    _fields_ = [("dongsi", CHAR * (1 + 1)),  # 동시호가구분
                ("jeqprice", CHAR * (7 + 1)),  # 예상체결가
                ("jeqsign", CHAR * (1 + 1)),  # 예상체결부호
                ("jeqchange", CHAR * (6 + 1)),  # 예상체결등락폭
                ("jeqchrate", CHAR * (5 + 1)),  # 예상체결등락률
                ("jeqvol", CHAR * (9 + 1)),  # 예상체결수량
                ("chkdataz1", CHAR * (1 + 1)),  # ECN정보유무구분
                ("ecn_price", CHAR * (9 + 1)),  # ECN전일종가
                ("ecn_sign", CHAR * (1 + 1)),  # ECN부호
                ("ecn_change", CHAR * (9 + 1)),  # ECN등락폭
                ("ecn_chrate", CHAR * (5 + 1)),  # ECN등락률
                ("ecn_volume", CHAR * (10 + 1)),  # ECN체결수량
                ("ecn_jeqsign", CHAR * (1 + 1)),  # ECN대비예상체결부호
                ("ecn_jeqchange", CHAR * (6 + 1)),  # ECN대비예상체결등락폭
                ("ecn_jeqchrate", CHAR * (5 + 1)),  # ECN대비예상체결등락률
                ]


class C4113OutKospi200Struct(LittleEndianStructure, StructBase):
    _fields_ = [("fuitem", CHAR * (8 + 1)),  # 종목코드
                ("fucurr", CHAR * (5 + 1)),  # 현물지수
                ("fusign", CHAR * (1 + 1)),  # 전일비부호
                ("fuchange", CHAR * (5 + 1)),  # 전일비
                ("fuopen", CHAR * (5 + 1)),  # 시가
                ("fuhigh", CHAR * (5 + 1)),  # 고가
                ("fulow", CHAR * (5 + 1)),  # 저가
                ("fuvolall", CHAR * (7 + 1)),  # 거래량
                ]


class P1005OutBlockStruct(LittleEndianStructure, StructByteBase):
    _fields_ = [
        ("code", CHAR * (6 + 1)),  # 단축코드
        ("expcode", CHAR * (12 + 1)),  # KRX코드
        ("hnamez40", CHAR * (40 + 1)),  # 종목명
    ]


class J8OutBlockStruct(LittleEndianStructure, StructBase):
    _fields_ = [
        ("code", (CHAR * 6)),  # 종목코드
        ("time", (CHAR * 8)),  # 시간
        ("sign", (CHAR * 1)),  # 등락부호
        ("change", (CHAR * 6)),  # 등락폭
        ("price", (CHAR * 7)),  # 현재가
        ("chrate", (CHAR * 5)),  # 등락률
        ("high", (CHAR * 7)),  # 고가
        ("low", (CHAR * 7)),  # 저가
        ("offer", (CHAR * 7)),  # 매도호가
        ("bid", (CHAR * 7)),  # 매수호가
        ("volume", (CHAR * 9)),  # 거래량
        ("volrate", (CHAR * 6)),  # 거래량전일비
        ("movolume", (CHAR * 8)),  # 변동거래량
        ("value", (CHAR * 9)),  # 거래대금
        ("open", (CHAR * 7)),  # 시가
        ("avgprice", (CHAR * 7)),  # 가중평균가
        ("janggubun", (CHAR * 1)),  # 장구분
    ]


class K8OutBlockStruct(LittleEndianStructure, StructBase):
    _fields_ = [
        ("code", (CHAR * 6)),  # 종목코드
        ("time", (CHAR * 8)),  # 시간
        ("sign", (CHAR * 1)),  # 등락부호
        ("change", (CHAR * 6)),  # 등락폭
        ("price", (CHAR * 7)),  # 현재가
        ("chrate", (CHAR * 5)),  # 등락률
        ("high", (CHAR * 7)),  # 고가
        ("low", (CHAR * 7)),  # 저가
        ("offer", (CHAR * 7)),  # 매도호가
        ("bid", (CHAR * 7)),  # 매수호가
        ("volume", (CHAR * 9)),  # 거래량
        ("volrate", (CHAR * 6)),  # 거래량전일비
        ("movolume", (CHAR * 8)),  # 변동거래량
        ("value", (CHAR * 9)),  # 거래대금
        ("open", (CHAR * 7)),  # 시가
        ("avgprice", (CHAR * 7)),  # 가중평균가
        ("janggubun", (CHAR * 1)),  # 장구분
    ]


class D2OutBlockStruct(LittleEndianStructure, StructBase):
    _fields_ = [
        ("userid", (CHAR * 8)),  # 사용자ID
        ("itemgb", (CHAR * 1)),  # ITEM구분
        ("accountno", (CHAR * 11)),  # 계좌번호
        ("orderno", (CHAR * 10)),  # 주문번호
        ("issuecd", (CHAR * 15)),  # 종목코드
        ("slbygb", (CHAR * 1)),  # 매도수구분
        ("concgty", (CHAR * 10)),  # 체결수량
        ("concprc", (CHAR * 11)),  # 체결가격
        ("conctime", (CHAR * 6)),  # 체결시간
        ("ucgb", (CHAR * 1)),  # 정정취소구분
        ("rejgb", (CHAR * 1)),  # 거부구분
        ("fundcode", (CHAR * 3)),  # 펀드코드
        ("sin_gb", (CHAR * 2)),  # 신용구분
        ("loan_date", (CHAR * 8)),  # 대출일자
        ("ato_ord_tpe_chg", (CHAR * 1)),  # 선물옵션주문유형변경여부
        ("filler", (CHAR * 34)),  # filler
    ]


class D3OutBlockStruct(LittleEndianStructure, StructBase):
    _fields_ = [
        ("userid", (CHAR * 8)),  # USERID
        ("itemgb", (CHAR * 1)),  # ITEM구분
        ("accountno", (CHAR * 11)),  # 계좌번호
        ("orderno", (CHAR * 10)),  # 주문번호
        ("orgordno", (CHAR * 10)),  # 원주문번호
        ("ordercd", (CHAR * 2)),  # 주문구분
        ("issuecd", (CHAR * 15)),  # 종목코드
        ("issuename", (CHAR * 20)),  # 종목명
        ("slbygb", (CHAR * 1)),  # 매매구분
        ("order_type", (CHAR * 2)),  # 주문유형
        ("ordergty", (CHAR * 10)),  # 주문수량
        ("orderprc", (CHAR * 11)),  # 주문단가
        ("procnm", (CHAR * 2)),  # 처리구분
        ("commcd", (CHAR * 2)),  # 매체구분
        ("order_cond", (CHAR * 1)),  # 주문조건1
        ("fundcode", (CHAR * 3)),  # 펀드코드
        ("sin_gb", (CHAR * 2)),  # 신용구분
        ("order_time", (CHAR * 6)),  # 주문시간
        ("loan_date", (CHAR * 8)),  # 대출일자
    ]


class C8101InBlockStruct(LittleEndianStructure, StructByteBase):  # 주식매도 주문 input
    _fields_ = [
        ("pswd_noz8", CHAR * 44),  # 계좌비밀번호
        ("issue_codez6", CHAR * 6),  # 종목번호
        ("order_qtyz12", CHAR * 12),  # 주문수량
        ("order_unit_pricez10", CHAR * 10),  # 주문단가
        ("trade_typez2", CHAR * 2),  # 매매유형 : 00 보통가, 03 시장가, 05 조건부지정가, 12 최유리지정가, 13 최우선지정가, 31 시간외단일가, 61 장전시간외, 71 장후시간외, C0 IOC보통가 (즉시체결.잔량취소), F0 FOK보통가 (전량체결.전량취소), C3 IOC시장가 (즉시체결.잔량취소), F3 FOK시장가 (전량체결.전량취소), C2 IOC최유리 (즉시체결.잔량취소), F2 FOK최유리 (전량체결.전량취소)
        ("shsll_pos_flagz1", CHAR * 1),  # 공매도가능여부
        ("trad_pswd_no_1z8", CHAR * 44),  # 거래비밀번호1
        ("trad_pswd_no_2z8", CHAR * 44),  # 거래비밀번호2
    ]


class C8101OutBlockStruct(LittleEndianStructure, StructByteBase):  # 주식매도 주문 output
    _fields_ = [
        ("order_noz10", CHAR * 10),  # 주문번호
        ("order_qtyz12", CHAR * 12),  # 주문수량
        ("order_unit_pricez10", CHAR * 10),  # 주문단가
    ]


class C8102InBlockStruct(LittleEndianStructure, StructByteBase):  # 주식매수 주문 input
    _fields_ = [
        ("pswd_noz8", CHAR * 44),  # 계좌비밀번호
        ("issue_codez6", CHAR * 6),  # 종목번호
        ("order_qtyz12", CHAR * 12),  # 주문수량
        ("order_unit_pricez10", CHAR * 10),  # 주문단가
        ("trade_typez2", CHAR * 2),  # 매매유형 : 00 보통가, 03 시장가, 05 조건부지정가, 12 최유리지정가, 13 최우선지정가, 31 시간외단일가, 61 장전시간외, 71 장후시간외, C0 IOC보통가 (즉시체결.잔량취소), F0 FOK보통가 (전량체결.전량취소), C3 IOC시장가 (즉시체결.잔량취소), F3 FOK시장가 (전량체결.전량취소), C2 IOC최유리 (즉시체결.잔량취소), F2 FOK최유리 (전량체결.전량취소)
        ("trad_pswd_no_1z8", CHAR * 44),  # 거래비밀번호1
        ("trad_pswd_no_2z8", CHAR * 44),  # 거래비밀번호2
    ]

    def __init__(self, dict_data=None):
        # print(dict_data)
        super().__init__()
        if dict_data:
            super().__init__(dict_data.account_pw.encode('utf-8'), dict_data.buy_cd_id.encode('utf-8'), str(dict_data.buy_qty).encode('utf-8'), str(dict_data.buy_price).encode('utf-8'), b'00', b'', b'')


class C8102OutBlockStruct(LittleEndianStructure, StructByteBase):  # 주식매수 주문 output
    _fields_ = [
        ("order_noz10", CHAR * 10),  # 주문번호
        ("order_qtyz12", CHAR * 12),  # 주문수량
        ("order_unit_pricez10", CHAR * 10),  # 주문단가
    ]


"""
AGENT MODEL END
"""
