from flaskz.rest import register_model_route

from ..api import api_bp
from ..modules.project import Project

register_model_route(api_bp, Project, '/project', module='deploy', to_json_option={'cascade': 1})
