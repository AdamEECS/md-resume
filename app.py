import logging

from flask import Flask
from flask_script import Manager

app = Flask(__name__)

manager = Manager(app)


def register_routes(app):
    from routes.user import main as routes_user
    from routes.index import main as routes_index
    from routes.admin import main as routes_admin
    from routes.img import main as routes_img
    from routes.document import main as routes_document
    from routes.demo import main as routes_demo

    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_index, url_prefix='/')
    app.register_blueprint(routes_admin, url_prefix='/admin')
    app.register_blueprint(routes_img, url_prefix='/img')
    app.register_blueprint(routes_document, url_prefix='/doc')
    app.register_blueprint(routes_demo, url_prefix='/demo')


def register_filters(app):
    from usr_util.filters import filters
    app.jinja_env.filters.update(filters)


def register_errorhandler(app):
    from flask import render_template

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('error/401.html'), 401

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404


def configure_app():
    from config import key
    app.secret_key = key.secret_key
    from config.config import config_dict
    app.config.update(config_dict)
    register_routes(app)
    register_filters(app)
    register_errorhandler(app)
    # 设置 log, 否则输出会被 gunicorn 吃掉
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


def configured_app():
    configure_app()
    return app


@manager.command
def server():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=8003,
    )
    app.run(**config)


if __name__ == '__main__':
    configure_app()
    manager.run()

# (gunicorn wsgi --worker-class=gevent -t 4 -b 0.0.0.0:8000 &)
