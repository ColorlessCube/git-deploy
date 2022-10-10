from flaskz.models import ModelBase

if ModelBase:
    pass


class AutoModelMixin:
    auto_columns = ['id', 'created_user', 'created_at', 'updated_at']


from .git import *
