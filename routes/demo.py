from . import *
from models.document import Document

main = Blueprint('demo', __name__)


@main.route('/')
def index():
    u = current_user()
    print('demo')
    d = Document.find_one(doc_url='demo')
    return render_template('document.html', u=u, d=d)


@main.route('/trick')
def fake_update():
    return render_template('demo/fake_update.html')
