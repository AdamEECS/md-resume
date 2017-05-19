from routes import *
from models.document import Document
from models.user import User
from models.auth import Auth
from models.access import Access
from flask import current_app as app

import qiniu
from config import key

q = qiniu.Auth(key.qiniu_access_key, key.qiniu_secret_key)

main = Blueprint('admin', __name__)


@main.route('/document/<user_uuid>')
@admin_required
def document(user_uuid):
    cu = current_user()
    u = User.find_one(uuid=user_uuid)
    u.pics_url = [app.config['BASE_URL'] + app.config['USER_PIC_DIR'] + pic for pic in u.pics]
    u.pics_url.reverse()
    d = Document.find_one(user_uuid=u.uuid)
    d.doc_url_full_path = app.config['DOC_URL'] + d.doc_url
    return render_template('user/document.html', p=d, u=cu)


@main.route('/document/new', methods=['POST'])
@admin_required
def document_new():
    u = current_user()
    form = request.form
    status, msgs = Document.valid(form)
    if status is True:
        p = Document.new(form)
        return redirect(url_for('admin.document', uuid=p.uuid))
    else:
        return render_template('admin/document_new.html', msgs=msgs, u=u)


@main.route('/documents')
@admin_required
def documents():
    u = current_user()
    ms = Document.all()
    ms.reverse()
    for m in ms:
        m.user = User.find_one(uuid=m.user_uuid)
    return render_template('admin/documents.html', ms=ms, u=u)


@main.route('/document/<uuid>', methods=['POST'])
@admin_required
def document_update(uuid):
    p = Document.find_one(uuid=uuid)
    form = request.form
    p.update(form)
    return redirect(url_for('admin.document', uuid=p.uuid))


@main.route('/auths')
@admin_required
def auths():
    u = current_user()
    ms = Auth.all()
    ms.reverse()
    for m in ms:
        m.user = User.find_one(uuid=m.user_uuid)
        m.verified = m.verify()
    return render_template('admin/auths.html', ms=ms, u=u)


# ------------------------- 用户管理 --------------------------
@main.route('/users')
@admin_required
def users():
    u = current_user()
    ms = User.all()
    return render_template('admin/users.html', ms=ms, u=u)


@main.route('/users', methods=['POST'])
@admin_required
def users_search():
    u = current_user()
    form = request.form
    ms = User.search_or(form)
    return render_template('admin/users.html', u=u, ms=ms)


@main.route('/user/<int:id>')
@admin_required
def user(id):
    u = current_user()
    m = User.get(id)
    return render_template('admin/user.html', m=m, u=u)


@main.route('/user/delete/<int:id>')
@admin_required
def user_delete(id):
    # m = User.get(id)
    # m.delete()
    # TODO 先不让删
    return redirect(url_for('admin.users'))


@main.route('/user/update/<int:id>', methods=['POST'])
@admin_required
def user_update(id):
    m = User.get(id)
    form = request.form
    m.update_user(form)
    return redirect(url_for('admin.user', id=m.id))

# @main.route('/root')
# @login_required
# def root_set():
#     root = User.find_one(username='root')
#     root.role = 'admin'
#     root.save()
#     return redirect(url_for('admin.document_new'))
