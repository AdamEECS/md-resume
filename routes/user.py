from routes import *
from models.user import User
from models.document import Document
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


@main.route('/password/forget')
def forget_password():
    return render_template('user/forget_password.html')


@main.route('/password/forget', methods=['POST'])
def forget_password_send():
    form = request.form
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        flash('验证码错误', 'warning')
        return redirect(url_for('user.forget_password'))
    r = User.forget_password(form)
    if r:
        flash('密码重置邮件已经发送，请查收邮箱', 'success')
    else:
        flash('用户名或邮箱不匹配', 'warning')
    return redirect(url_for('user.forget_password'))


@main.route('/email/verify/<tb64>')
def email_verify(tb64):
    if User.email_verify(tb64):
        flash('邮箱验证通过', 'success')
    else:
        flash('邮箱验证失败', 'danger')
    return redirect(url_for('user.profile'))


@main.route('/password/forget/verify/<tb64>')
def forget_password_verify(tb64):
    if User.forget_password_verify(tb64):
        flash('重置邮件验证通过', 'success')
        return render_template('user/reset_password.html', tb64=tb64)
    else:
        flash('重置邮件验证失败', 'danger')
        return redirect(url_for('user.index'))


@main.route('/password/reset/<tb64>', methods=['POST'])
def reset_password(tb64):
    password = request.form.get('password', '')
    if User.forget_password_verify(tb64):
        u = User.get_user_by_tb64(tb64)
        u.reset_password(password)
        session['uid'] = u.id
        flash('密码已重置', 'success')
        return redirect(url_for('index.index'))
    else:
        flash('重置邮件验证失败', 'warning')
        return redirect(url_for('user.index'))


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


@main.route('/profile')
@login_required
def profile():
    u = current_user()
    d = Document.find_one(user_uuid=u.uuid)
    return render_template('user/profile.html', u=u, d=d)


@main.route('/profile', methods=['POST'])
@login_required
def profile_update():
    cu = current_user()
    form = request.form
    cu.safe_update_user(form)
    flash('信息已更新', 'success')
    return redirect(url_for('user.profile'))


@main.route('/email/update', methods=['POST'])
@login_required
def update_email():
    u = current_user()
    form = request.form
    new_email = form.get('email', '')
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        return json.dumps({'status': 'warning', 'msg': '验证码错误'})
    if User.has(email=new_email) and User.find_one(email=new_email).uuid != u.uuid:
        return json.dumps({'status': 'warning', 'msg': '该邮箱已被占用'})
    if u.validate_login(form):
        u.send_email_verify(new_email)
        return json.dumps({'status': 'info', 'msg': '已发送验证邮件，请查收'})
    else:
        return json.dumps({'status': 'warning', 'msg': '密码错误'})


@main.route('/document')
@login_required
def document():
    u = current_user()
    p = Document.find_one(user_uuid=u.uuid)
    return render_template('user/document.html', p=p, u=u)


@main.route('/document', methods=['POST'])
@login_required
def document_update():
    u = current_user()
    p = Document.find_one(user_uuid=u.uuid)
    form = request.form
    p.update(form)
    return redirect(url_for('user.document'))


@main.route('/document/setting', methods=['POST'])
@login_required
def document_setting():
    u = current_user()
    p = Document.find_one(user_uuid=u.uuid)
    form = request.form
    p.update_setting(form)
    flash('简历设置已更新', 'success')
    return redirect(url_for('user.profile'))


@main.route('/auth')
@login_required
def auth():
    cu = current_user()
    return render_template('user/profile.html', u=cu)
