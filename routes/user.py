from routes import *
from models.user import User
from decimal import Decimal
from flask import current_app as app

main = Blueprint('user', __name__)

Model = User


@main.route('/login')
def index():
    return render_template('user/login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    username = form.get('username', '')
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        flash('验证码错误', 'warning')
        return redirect(url_for('user.index'))
    u = User.find_one(username=username)
    if u is not None and u.validate_login(form):
        session['uid'] = u.id
        return redirect(url_for('index.index'))
    else:
        flash('用户名密码错误', 'warning')
        return redirect(url_for('user.index'))


@main.route('/register')
def register_page():
    return render_template('user/register.html')


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        flash('验证码错误', 'warning')
        return redirect(url_for('user.register'))
    status, msgs = User.valid(form)
    if status is True:
        u = User.new(form)
        u.send_email_verify(u.email)
        session['uid'] = u.id
        flash('验证邮件已发送，请查收', 'info')
        return redirect(url_for('index.index'))
    else:
        for msg in msgs:
            flash(msg, 'warning')
        return redirect(url_for('user.register'))


@main.route('/email/verify/<tb64>')
def email_verify(tb64):
    if User.email_verify(tb64):
        flash('邮箱验证通过', 'success')
    else:
        flash('邮箱验证失败', 'danger')
    return redirect(url_for('user.profile'))


@main.route('/avatar/upload', methods=['POST'])
@login_required
def avatar():
    u = current_user()
    avatar = request.files['avatar']
    u.update_avatar(avatar)
    return redirect(url_for('.profile'))


@main.route('/logout')
@login_required
def logout():
    p = session.pop('uid')
    print('logout: pop uid', p)
    flash('账号已安全退出', 'success')
    return redirect(url_for('index.index'))


