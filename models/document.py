from . import MongoModel
from . import bool_dict
from flask import current_app as app


class Document(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('user_uuid', str, ''),
            ('doc_url', str, ''),
            ('title', str, ''),
            ('public', bool, False),
            ('detail', str, ''),
            ('css', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form):
        m = super().new(form)
        from uuid import uuid4
        m.set_uuid(field='doc_url', seed=uuid4)
        m.save()
        return m

    def update_pic(self, pic):
        allowed_type = ['jpg', 'jpeg', 'gif', 'png']
        upload_name = pic.filename
        if upload_name != '' and upload_name.split('.')[-1] in allowed_type:
            path = app.config['USER_PIC_DIR']
            ext = app.config['PRODUCT_PIC_EXT']
            fullname = '{}{}.{}'.format(path, str(self.id), ext)
            pic.save(fullname)
            self.pic = '/' + fullname
            self.save()
        return self

    def set_pic_url(self, url):
        if len(url) > 0:
            self.pic = url
            self.save()

    def update_setting(self, form):
        form = form.to_dict()
        public = form.pop('public', 'false')
        form['public'] = bool_dict.get(public, False)
        if self.has(doc_url=form.get('doc_url')):
            form.pop('doc_url')
        self.update(form)
        return self
