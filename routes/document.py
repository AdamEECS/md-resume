from . import *
from models.document import Document
from models.auth import Auth

main = Blueprint('document', __name__)


@main.route('/<doc_url>')
def index(doc_url):
    u = current_user()
    d = Document.find_one(doc_url=doc_url)
    if d.public is True or (u is not None and d.user_uuid == u.uuid):
        return render_template('document.html', d=d, u=u)
    else:
        abort(401)


@main.route('/<doc_url>/token/<token>')
def protected(doc_url, token):
    u = current_user()
    d = Document.find_one(doc_url=doc_url)
    a = Auth.find_one(token=token, doc_uuid=d.uuid)
    if a is None:
        abort(401)
    if a.verify():
        a.used(request, success=True)
        text = '面试者对您的访问授权剩余{}次，授权过期时间：{}'.format(a.token_times, time_str(a.token_exp))
        flash(text, 'success')
        return render_template('document.html', d=d, u=u, token=token)
    else:
        a.used(request, success=False)
        abort(401)


@main.route('/<doc_url>/mail', methods=['POST'])
def send_mail(doc_url):
    u = current_user()
    form = request.form
    captcha = form.get('captcha', '').lower()
    email = form.get('email')
    token = form.get('token', '')
    if captcha != session.get('captcha', 'no captcha!'):
        return json.dumps({'status': 'warning', 'msg': '验证码错误!'})
    d = Document.find_one(doc_url=doc_url)
    a = Auth.find_one(token=token, doc_uuid=d.uuid)
    public_valid = d.public is True
    owner_valid = u is not None and d.user_uuid == u.uuid
    token_valid = a is not None and a.verify()
    if public_valid or owner_valid:
        d.send_email(email)
        return json.dumps({'status': 'success', 'msg': '邮件已发送，未收到请检查垃圾箱。'})

    elif token_valid:
        d.send_email(email)
        a.used(request, success=True, mode='Send Email')
        return json.dumps({'status': 'success', 'msg': '邮件已发送，未收到请检查垃圾箱。本次请求已消耗您的授权1次。'})
    else:
        return json.dumps({'status': 'warning', 'msg': '您的请求未获得授权。'})
