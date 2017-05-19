from . import *
from models.document import Document

main = Blueprint('index', __name__)


@main.route('/')
def index():
    return redirect(url_for('demo.index'))

