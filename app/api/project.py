from flask_login import current_user
from flaskz.log import flaskz_logger
from flaskz.models import model_to_dict
from flaskz.rest import get_rest_log_msg, rest_permission_required
from flaskz.utils import create_response

from ..api import api_bp
from ..modules.project import Project


@api_bp.route('/project/', methods=['GET'])
@rest_permission_required('project')
def query_project():
    result = Project.query_by({
        'user_id': current_user.id
    })
    status = True
    if current_user.role.name == 'Manager':
        status, result = Project.query_all()
    res_data = model_to_dict(result, {'cascade': 1})
    flaskz_logger.debug(get_rest_log_msg('Query Project data by {}'.format(current_user.name), None, status, res_data))
    return create_response(status, res_data)
