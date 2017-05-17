from . import MongoModel
from flask import current_app as app


class Document(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('name', str, ''),
            ('price', str, ''),
            ('pic', str, ''),
            ('detail', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def valid(cls, form):
        name = form.get('name', '')
        valid_name = cls.find_one(name=name) is None
        msgs = []
        if not valid_name:
            message = '商品已经存在'
            msgs.append(message)
        status = valid_name
        return status, msgs

    @classmethod
    def new(cls, form):
        m = super().new(form)
        m.qiniu_pic()
        return m

    def update_pic(self, pic):
        allowed_type = ['jpg', 'jpeg', 'gif', 'png']
        upload_name = pic.filename
        if upload_name != '' and upload_name.split('.')[-1] in allowed_type:
            path = app.config['PRODUCT_PIC_DIR']
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
