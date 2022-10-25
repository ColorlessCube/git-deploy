import json

from flaskz.log import flaskz_logger
from flaskz.rest import init_model_rest_blueprint, get_rest_log_msg
from flask import request
from flaskz.utils import create_response

from ..api import api_bp
from ..modules.project import Project, VM
from ..utils import project_redeploy

init_model_rest_blueprint(Project, api_bp, '/project', routers=['add', 'update', 'upsert', 'delete'], module='project',
                          to_json_option={'cascade': 1})

init_model_rest_blueprint(VM, api_bp, '/vm', module='vm', multiple_option={
    'vms': VM,
    'projects': {
        'model_cls': Project,
        'option': {
            'include': ['id', 'name']
        }
    }
})


@api_bp.route('/deploy', methods=['POST'])
def deploy():
    json_data = request.json
    req_log_data = json.dumps(json_data)
    token = request.headers.get('X-Gitlab-Token', '')
    if token:
        project_redeploy(json_data.get('project'), token)
    res_log_data = 'Webhook Succeed.'
    res_status = True
    flaskz_logger.info(get_rest_log_msg('Webhook trigger.', req_log_data, res_status, res_log_data))
    return create_response(res_status, res_log_data)


@api_bp.route('/deploy/manual', methods=['POST'])
def manual_deploy():
    json_data = request.json
    req_log_data = json.dumps(json_data)
    token = json_data.get('token')
    project_redeploy(json_data, token)
    res_log_data = 'Manual redeploy succeed.'
    res_status = True
    flaskz_logger.info(get_rest_log_msg('Manual trigger.', req_log_data, res_status, res_log_data))
    return create_response(res_status, res_log_data)
