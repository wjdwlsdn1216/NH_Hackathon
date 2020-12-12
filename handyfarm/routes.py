import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from handyfarm import app, db, bcrypt
from handyfarm.forms import RegistrationForm, LoginForm, UpdateAccountForm
from handyfarm.models import User,Post
# from oauth2client.contrib.flask_util import UserOAuth2
from flask_login import login_user, current_user, logout_user, login_required

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


@app.route("/delivery")
def delivery():
    return render_template('delivery.html', title='delivery') #전달해주는 인자

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
