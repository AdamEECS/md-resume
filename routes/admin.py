from routes import *
from models.document import Document
from models.user import User
from flask import current_app as app

import qiniu
from config import key

q = qiniu.Auth(key.qiniu_access_key, key.qiniu_secret_key)

main = Blueprint('admin', __name__)


@main.route('/document/new')
@admin_required
def document_new_page():
    u = current_user()
    return render_template('admin/document_new.html', u=u)


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


@main.route('/document')
@admin_required
def document():
    u = current_user()
    p = Document.find_one()
    return render_template('admin/document.html', p=p, u=u)


@main.route('/document/<uuid>', methods=['POST'])
@admin_required
def document_update(uuid):
    p = Document.find_one(uuid=uuid)
    form = request.form
    p.update(form)
    return redirect(url_for('admin.document', uuid=p.uuid))


@main.route('/root')
@login_required
def root_set():
    root = User.find_one(username='root')
    root.role = 'admin'
    root.save()
    return redirect(url_for('admin.document_new'))
