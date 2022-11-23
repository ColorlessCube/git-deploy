"""
业务模型类目录，请参考 -http://zhangyiheng.com/blog/articles/py_flaskz_model_mixin.html
template为实例，需删除
"""
# app/modules/__init__.py
from flask_login import current_user
from flaskz.models import ModelBase
# 避免IDE自动删除未引用导入
from flaskz.utils import filter_list

from ..utils import get_current_user_id

if ModelBase:
    pass


def is_admin():
    user = current_user
    if user and user.username == 'admin':
        return True
    return False


# custom modules, include model and logic
class AutoModelMixin:
    auto_columns = ['id', 'created_at', 'updated_at']


class UserBaseModelMixin:
    """
    User-based data access control
    Users can only access their own data

        class Customer(ModelBase, UserBaseModelMixin, ModelMixin, AutoModelMixin):
            ...
    """

    @classmethod
    def get_user_id_field(cls):
        """
        Get the user id field
        :return:
        """
        return 'user_id'

    @classmethod
    def _append_user_id(cls, data):
        user_id_field = cls.get_user_id_field()
        if user_id_field:
            data[cls.get_user_id_field()] = get_current_user_id()
        return data

    @classmethod
    def get_add_data(cls, data):
        return super().get_add_data(cls._append_user_id(data))

    @classmethod
    def get_update_data(cls, data):
        user_id_field = cls.get_user_id_field()
        if user_id_field:
            # After the data is modified by other users, whether to modify user_id, 1 or 2
            # 1. not modify user_id
            data.pop(user_id_field, None)
            # 2. modify user_id
            # cls._append_user_id(data)
        return super().get_update_data(data)

    @classmethod
    def query_all(cls):
        success, result = super().query_all()
        if success is True and not is_admin():
            current_user_id = get_current_user_id()
            user_id_field = cls.get_user_id_field()
            if user_id_field:
                return success, filter_list(result, lambda item: getattr(item, user_id_field) == current_user_id)
        return success, result

    @classmethod
    def query_pss(cls, pss_option):
        user_id_field = cls.get_user_id_field()
        if user_id_field and not is_admin():
            filter_ands = pss_option.get('filter_ands', [])
            filter_ands.append(user_id_field + "='" + get_current_user_id() + "'")
            pss_option['filter_ands'] = filter_ands
        return super().query_pss(pss_option)


from .project import *
