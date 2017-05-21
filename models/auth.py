from . import MongoModel
from . import timestamp
from models.access import Access
from datetime import datetime
import time
from flask import current_app as app


class Auth(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('user_uuid', str, ''),
            ('doc_uuid', str, ''),
            ('comment', str, ''),
            ('token', str, ''),
            ('token_exp', int, 0),
            ('token_times', int, 0),
            ('visited_times', int, 0),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form):
        m = super().new(form)
        m.set_uuid(field='token')
        m.save()
        return m

    def update_setting(self, form):
        form = form.to_dict()
        form.pop('token')
        token_exp = form.pop('token_exp')
        token_exp = datetime.strptime(token_exp, '%Y-%m-%dT%H:%M')
        token_times = form.pop('token_times')
        form['token_times'] = int(token_times)
        form['token_exp'] = int(token_exp.timestamp())
        self.update(form)
        return self

    def verify(self):
        now = timestamp()
        if self.token_times > 0 and self.token_exp > now:
            return True
        else:
            return False

    def used(self, request, success=True, mode='Web'):
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        form = dict(
            token=self.token,
            user_uuid=self.user_uuid,
            mode=mode,
            doc_uuid=self.doc_uuid,
            platform=request.user_agent.platform,
            browser=request.user_agent.browser,
            version=request.user_agent.version,
            user_agent=request.user_agent.string,
            access_route=[i for i in request.access_route],
            ip=ip,
            success=success,
        )
        Access.new(form)
        if success:
            self.token_times -= 1
            self.visited_times += 1
            self.save()
