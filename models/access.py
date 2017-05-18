from . import MongoModel
from . import timestamp
from datetime import datetime
import time
from flask import current_app as app


class Access(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('token', str, ''),
            ('user_uuid', str, ''),
            ('doc_uuid', str, ''),
            ('platform', str, ''),
            ('browser', str, ''),
            ('version', str, ''),
            ('user_agent', str, ''),
            ('access_route', list, []),
            ('success', bool, False),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form):
        m = super().new(form)
        # m.set_uuid(field='token')
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
