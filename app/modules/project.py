from datetime import datetime

from flaskz.models import ModelBase, ModelMixin
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from . import AutoModelMixin, UserBaseModelMixin


class Project(ModelBase, UserBaseModelMixin, ModelMixin, AutoModelMixin):
    __tablename__ = 'deploy_projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('sys_users.id', name='user_id', ondelete='CASCADE'))
    name = Column(String(32), nullable=False)
    repository = Column(String(256), nullable=False)
    branch = Column(String(32), nullable=False)
    token = Column(String(256), nullable=False)
    username = Column(String(64))
    password = Column(String(64))
    last_trig = Column(DateTime())
    created_at = Column(DateTime(), default=datetime.now, info={'auto': True})
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    vms = relationship('VM', cascade='all,delete,delete-orphan', uselist=True, lazy='joined')

    auto_columns = ['id', 'created_at', 'updated_at', 'last_trig']


class VM(ModelBase, UserBaseModelMixin, ModelMixin, AutoModelMixin):
    __tablename__ = 'deploy_vms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('deploy_projects.id', ondelete='CASCADE'), nullable=False)
    host = Column(String(32), nullable=False)
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    git_dir = Column(String(256), nullable=False)
    deploy_command = Column(Text(), nullable=False)
    check_command = Column(String(256), nullable=False)
    status = Column(Boolean)
    trigger_at = Column(DateTime())
    created_at = Column(DateTime(), default=datetime.now, info={'auto': True})
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    auto_columns = ['id', 'created_at', 'updated_at', 'trigger_at']
