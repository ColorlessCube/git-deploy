"""
用于提供业务API
"""
from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import deploy
from . import project
