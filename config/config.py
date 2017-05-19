from pymongo import *

config_dict = dict(
    USER_AVATAR_DIR='static/user_avatar/',
    PRODUCT_PIC_DIR='static/product_pic/',
    USER_PIC_DIR='static/user_pic/',
    PRODUCT_PIC_EXT='png',
    SEND_EMAIL_URL='https://api.mailgun.net/v3/mg.suzumiya.cc/messages',
    SEND_EMAIL_FROM='Suzumiya <no-replay@mg.suzumiya.cc>',
    BASE_URL='http://localhost:8003',
    MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    ALLOWED_UPLOAD_TYPE=['jpg', 'jpeg', 'gif', 'png', 'ico'],
)

# mongodb config
db_name = 'mongo_md_resume'
client = MongoClient("mongodb://localhost:27017")
db = client[db_name]
