import re
import requests
import json
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from handyfarm import app, db, bcrypt
from handyfarm.forms import RegistrationForm, LoginForm, UpdateAccountForm
from handyfarm.models import User,Post
# from oauth2client.contrib.flask_util import UserOAuth2
from flask_login import login_user, current_user, logout_user, login_required

import function

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
        return ""
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
IsTuno = "0060" # 기관거래고유번호
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
#print(DrawingTransfer(Tsymd, Iscd, IsTuno, AccessToken, FinAcno, Tram, DractOtlt))

Insymd = "20201211"
Ineymd = "20201212"
#print(InquireTransactionHistory(Tsymd, Iscd, IsTuno, AccessToken, Bncd, Acno, Insymd, Ineymd))

# print(InquireBalance(Tsymd, Iscd, IsTuno, AccessToken, FinAcno))

# oauth2 = UserOAuth2(app)

#농장 더미데이터
# farms=[
#     {
#         'farmer': 'minsung',
#         'title': 'seoul_smart_farm',
#         'content': 'very very good farm',
#         'resist_date': 'Decembrer 8, 2020'
#     }
# ]

@app.route("/")

#첫페이지
@app.route("/home")
def home():
    return render_template('home.html')
#농장
# @app.route("/farm")
# def farm():
#     return render_template('farm.html', title='Farm') #전달해주는 인자

@app.route("/myfarm")
def farm():
    return render_template('myfarm.html', title='myfarm') #전달해주는 인자

@app.route("/item")
def item():
    return render_template('item.html', title='item') #전달해주는 인자

@app.route('/ajax', methods=['POST'])
def ajax():
    data = request.get_json()
    print(data)

    return jsonify(result = "success", result2= data)

@app.route("/delivery")
def delivery():
    return render_template('delivery.html', title='delivery') #전달해주는 인자

@app.route("/subscription")
def subscription():
    return render_template('subscription.html', title='subscription') #전달해주는 인자


@app.route("/paypal")
def paypal():
    return render_template('paypal.html', title='paypal') #전달해주는 인자

@app.route("/farm2")
def farm2():
    return render_template('farm2.html', title='farm2') #전달해주는 인자

#회원가입
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # 로그인 되어있으면
        return redirect(url_for('home')) # 홈페이지로
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # 입력한 비밀번호를 해쉬값으로 치환
        user = User(username = form.username.data, email = form.email.data, password=hashed_password) # 사용자의 다른 정보와 해쉬화된 비밀번호를 저장
        db.session.add(user)
        db.session.commit() # database에 commit
        flash('회원님의 계정이 생성되었습니다! 로그인 할 수 있습니다.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# 구글로그인
# @app.route("/googlelogin", methods=['GET','POST'])
# @oauth2.required
# def googlelogin():
#     if oauth2.has_credentials():
#         return redirect(url_for('home'))
#     else:
#         print('login No')
#     return render_template('googlelogin.html')
#로그인
@app.route("/login", methods=['GET', 'POST'])
# @oauth2.required
def login():
    if current_user.is_authenticated: # 로그인 되어있으면
        return redirect(url_for('home')) # 홈페이지로
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  ### 6, 25:00
        if user and bcrypt.check_password_hash(user.password, form.password.data): ### 6, 25:00
                login_user(user, remember=form.remember.data) ### 6, 25:00
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home')) # 이동하려던 다음페이지가 있으면 다음페이지로 아니면 홈으로
        else:        
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
#로그아웃
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8) # 사진을 해쉬값으로저장
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form =UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('수정이 완료되었습니다.','success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form = form)

count = 2450
@app.route("/final_subscription", methods=['GET', 'POST'])
def final_subscription():
    global count
    str_count = str(count).zfill(4)
    Mes_1 = DrawingTransfer("20201213", "000723", str_count, "4d60bf5b7376fdca75b5a61080c2f5a3e55e21562757c12fad2ee736075f3d28", "00820100007230000000000004841", "29700", "베이직")
    count += 1
    flash(Mes_1)
    msg_1=Mes_1
    str_count = str(count).zfill(4)
    Mes_2 = InquireBalance("20201213", "000723", str_count, "4d60bf5b7376fdca75b5a61080c2f5a3e55e21562757c12fad2ee736075f3d28", "00820100007230000000000004841")
    count += 1
    msg_2="잔액" + Mes_2 + " 원 남았습니다"
    return render_template('final_subscription.html', title='final_subscription', msg_1=msg_1,msg_2=msg_2) #전달해주는 인자