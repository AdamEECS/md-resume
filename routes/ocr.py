from . import *
import base64
import requests


main = Blueprint('ocr', __name__)


@main.route('/')
def index():
    return render_template('ocr.html')


@main.route('/', methods=['POST'])
def parse():
    img = request.files.get('image')
    img = base64.b64encode(img.read())
    params = {"image": img}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    import config.key as key
    access_token = key.at
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token
    r = requests.post(url, data=params, headers=headers)
    try:
        d = json.loads(r.content.decode())
        words_list = d.get('words_result')
        # pprint.pprint(d)
        ps = [i.get('words') for i in words_list]
        p = ''.join(ps)
    except Exception as e:
        print(e)
        p = '解析失败，请重试。'
        ps = [p]
    return render_template('ocr.html', p=p, ps=ps)
