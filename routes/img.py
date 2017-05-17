from PIL import Image, ImageDraw, ImageFont
import io
import string
import random
from flask import current_app as app
from routes import *

main = Blueprint('img', __name__)


@main.route('/captcha')
def captcha():
    width = 112
    height = 49
    size = (width, height)
    image = Image.new('RGB', size, color=(255, 255, 255))
    font_file = 'static/font/MONACO.TTF'
    font = ImageFont.truetype(font_file, 39)
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 4))
    draw.text((7, 0), rand_str, fill=rand_rgb(), font=font)
    point_chance = 10
    chance = min(50, max(0, int(point_chance)))
    for w in range(width):
        for h in range(height):
            tmp = random.randint(0, 50)
            if tmp > 50 - chance:
                draw.point((w, h), fill=rand_rgb())
    del draw
    session['captcha'] = rand_str.lower()
    buf = io.BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@main.route('/captcha/s')
def captcha_s():
    width = 82
    height = 34
    size = (width, height)
    image = Image.new('RGB', size, color=(255, 255, 255))
    font_file = 'static/font/MONACO.TTF'
    font = ImageFont.truetype(font_file, 29)
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 4))
    draw.text((7, 0), rand_str, fill=rand_rgb(), font=font)
    point_chance = 10
    chance = min(50, max(0, int(point_chance)))
    for w in range(width):
        for h in range(height):
            tmp = random.randint(0, 50)
            if tmp > 50 - chance:
                draw.point((w, h), fill=rand_rgb())
    del draw
    session['captcha'] = rand_str.lower()
    buf = io.BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


def rand_rgb():
    return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))
