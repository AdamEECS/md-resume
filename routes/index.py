from . import *
from models.document import Document

main = Blueprint('index', __name__)


@main.route('/')
def index():
    u = current_user()
    d = Document.find_one()
    return render_template('index.html', u=u, d=d)
