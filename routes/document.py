from . import *
from models.document import Document

main = Blueprint('document', __name__)


@main.route('/<doc_url>')
def index(doc_url):
    u = current_user()
    d = Document.find_one(doc_url=doc_url)
    return render_template('document.html', d=d, u=u)
