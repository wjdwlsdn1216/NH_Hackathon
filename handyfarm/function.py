import requests
import json
import re


def OpenFinAccountDirect(Tsymd, Iscd, IsTuno, AccessToken, BrdtBrno, Bncd, Acno):  # 핀-어카운트직접발급
    datas = {
    "Header": {
    "ApiNm": "OpenFinAccountDirect",
    "Tsymd": Tsymd, # 오늘 날짜
    "Trtm": "112428",
    "Iscd": Iscd,  # 기관 코드
    "FintechApsno": "001",
    "ApiSvcCd": "DrawingTransferA",
    "IsTuno": IsTuno,  # 로그 기록을 위한 index값
    "AccessToken": AccessToken}, # 인증키

    "DrtrRgyn": "Y",
    "BrdtBrno": BrdtBrno,  # 생년월일
    "Bncd": Bncd,  # 은행코드
    "Acno": Acno  # 계좌번호
    }

    url = "https://developers.nonghyup.com/OpenFinAccountDirect.nh"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    params_json = json.dumps(datas)
    response = requests.post(url, data=params_json, headers=headers).text

    z = re.compile('[0-9a-zA-Zㄱ-힗]+').findall(response)
    x = {"d":"d"}
    for i in range(0,len(z)-1):
        x.setdefault(z[i],z[i+1])
    return x['Rgno']

def CheckOpenFinAccountDirect(Tsymd, Iscd, IsTuno, AccessToken, Rgno, BrdtBrno):  # 핀-어카운트발급확인
    datas = {
    "Header": {
        "ApiNm": "CheckOpenFinAccountDirect",
        "Tsymd": Tsymd,  # 오늘 날짜
        "Trtm": "112428",  
        "Iscd": Iscd,  # 기관코드 
        "FintechApsno": "001",
        "ApiSvcCd": "DrawingTransferA",
        "IsTuno": IsTuno,  # 로그 기록을 위한 index값
        "AccessToken": AccessToken  # 인증키
    },
    "Rgno": Rgno, # 등록 번호
    "BrdtBrno": BrdtBrno # 생년월일
    }

    url = "https://developers.nonghyup.com/CheckOpenFinAccountDirect.nh"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    params_json = json.dumps(datas)
    response = requests.post(url, data=params_json, headers=headers).text

    z = re.compile('[0-9a-zA-Zㄱ-힗]+').findall(response)
    x = {"d":"d"}

    for i in range(0,len(z)-1):
        x.setdefault(z[i],z[i+1])

    return x["FinAcno"]

def InquireDepositorAccountNumber(Tsymd, Iscd, IsTuno, AccessToken, Bncd, Acno):  # 예금주조회
    datas = {
    "Header": {
        "ApiNm": "InquireDepositorAccountNumber",
        "Tsymd": Tsymd,
        "Trtm": "112428",
        "Iscd": Iscd,
        "FintechApsno": "001",
        "ApiSvcCd": "DrawingTransferA",
        "IsTuno": IsTuno,
        "AccessToken": AccessToken
    },
    "Bncd": Bncd,
    "Acno": Acno
    }

    url = "https://developers.nonghyup.com/InquireDepositorAccountNumber.nh"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    params_json = json.dumps(datas)
    response = requests.post(url, data=params_json, headers=headers).text

    z = re.compile('[0-9a-zA-Zㄱ-힗]+').findall(response)
    x = {"d":"d"}

    for i in range(0,len(z)-1):
        x.setdefault(z[i],z[i+1])

    return [x["Dpnm"], x["Acno"]]

def DrawingTransfer(Tsymd, Iscd, IsTuno, AccessToken, FinAcno, Tram, DractOtlt):  # 출금이체
    datas = {
    "Header": {
        "ApiNm": "DrawingTransfer",
        "Tsymd": Tsymd,
        "Trtm": "112428",
        "Iscd": Iscd,
        "FintechApsno": "001",
        "ApiSvcCd": "DrawingTransferA",
        "IsTuno": IsTuno,
        "AccessToken": AccessToken
    },
    "FinAcno": FinAcno, # 핀어카운트
    "Tram": Tram, # 거래 금액
    "DractOtlt": DractOtlt # 출금계좌인자내용, 메모
    }

    url = "https://developers.nonghyup.com/DrawingTransfer.nh"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    params_json = json.dumps(datas)
    response = requests.post(url, data=params_json, headers=headers).text

    z = re.compile('[0-9a-zA-Zㄱ-힗]+').findall(response)
    x = {"d":"d"}

    for i in range(0,len(z)-1):
        x.setdefault(z[i],z[i+1])

    if x["Rsms"] == "정상처리":
        return "정상처리 되었습니다"
    else:
        return "오류 발생"

def InquireTransactionHistory(Tsymd, Iscd, IsTuno, AccessToken, Bncd, Acno, Insymd, Ineymd):  # 거래내역 조회
    datas = {
    "Header": {
        "ApiNm": "InquireTransactionHistory",
        "Tsymd": Tsymd,
        "Trtm": "112428",
        "Iscd": Iscd,
        "FintechApsno": "001",
        "ApiSvcCd": "ReceivedTransferA",
        "IsTuno": IsTuno,
        "AccessToken": AccessToken
    },
    "Bncd": Bncd,
    "Acno": Acno,
    "Insymd": Insymd,  # 시작 날짜
    "Ineymd": Ineymd,  # 끝 날짜
    "TrnsDsnc": "A",
    "Lnsq": "DESC",
    "PageNo": "1",
    "Dmcnt": "100"
    }

    url = "https://developers.nonghyup.com/InquireTransactionHistory.nh"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    params_json = json.dumps(datas)
    response = requests.post(url, data=params_json, headers=headers).text

    z = re.compile('[0-9a-zA-Zㄱ-힗]+').findall(response)
    x = {"d":"d"}

    for i in range(0,len(z)-1):
        x.setdefault(z[i],z[i+1])

    return x["TotCnt"] + "건" 

def InquireBalance(Tsymd, Iscd, IsTuno, AccessToken, FinAcno):  # 잔액조회
    datas = {
    "Header": {
        "ApiNm": "InquireBalance",
        "Tsymd": Tsymd,
        "Trtm": "112428",
        "Iscd": Iscd,
        "FintechApsno": "001",
        "ApiSvcCd": "ReceivedTransferA",
        "IsTuno": IsTuno,
        "AccessToken": AccessToken
    },
    "FinAcno": FinAcno
    }

    url = "https://developers.nonghyup.com/InquireBalance.nh"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    params_json = json.dumps(datas)
    response = requests.post(url, data=params_json, headers=headers).text

    z = re.compile('[0-9a-zA-Zㄱ-힗]+').findall(response)
    x = {"d":"d"}

    for i in range(0,len(z)-1):
        x.setdefault(z[i],z[i+1])

    return x["Ldbl"] 


Tsymd = "20201213" # 오늘날짜
Iscd = "000723"  # 기관코드
IsTuno = "0056" # 기관거래고유번호
AccessToken = "4d60bf5b7376fdca75b5a61080c2f5a3e55e21562757c12fad2ee736075f3d28" # 인증키
BrdtBrno = "19501212"  # 생년월일
Bncd = "011" # 은행코드
Acno = "3020000003092"  # 계좌번호

# Rgno = (OpenFinAccountDirect(Tsymd, Iscd, IsTuno, AccessToken, BrdtBrno, Bncd, Acno))
Rgno = "20201212000001031"

# FinAcno = CheckOpenFinAccountDirect(Tsymd, Iscd, IsTuno, AccessToken, Rgno, BrdtBrno)
FinAcno = "00820100007230000000000004841"

#print(InquireDepositorAccountNumber(Tsymd, Iscd, IsTuno, AccessToken, Bncd, Acno))

Tram = 10000 # 만원
DractOtlt = "하.."
print(DrawingTransfer(Tsymd, Iscd, IsTuno, AccessToken, FinAcno, Tram, DractOtlt))

Insymd = "20201211"
Ineymd = "20201212"
#print(InquireTransactionHistory(Tsymd, Iscd, IsTuno, AccessToken, Bncd, Acno, Insymd, Ineymd))

#print(InquireBalance(Tsymd, Iscd, IsTuno, AccessToken, FinAcno))