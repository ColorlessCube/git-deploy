import json
import time
from datetime import datetime
import re

from flask import request
from flaskz.log import flaskz_logger
from flaskz.rest import init_model_rest_blueprint, get_rest_log_msg
from flaskz.models import model_to_dict
from flaskz.utils import create_response

from ..api import api_bp
from ..utils import ssh_session
from ..modules import Project, VM

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
    print(request)
    json_data = request.json
    req_log_data = json.dumps(json_data)
    token = json_data.get('token')
    res_log_data = project_redeploy(json_data, token, True)
    res_status = True
    flaskz_logger.info(get_rest_log_msg('Manual trigger.', req_log_data, res_status, res_log_data))
    return create_response(res_status, res_log_data)


def check_signature(project, token):
    """
    Gitlab check signature do not need to use algorithm.
    :param project:
    :param token:
    :return:
    """
    return project.token == token


def check_project_status(status_info, check_command):
    """
    Check project status need to adapt to all situation.
    :param status_info:
    :param check_command: If check command is empty, then there is no need to check.
    :return:
    """
    result = True
    if check_command == '' or check_command is None:
        return result
    # 1. Empty result
    # lsof -i:8888
    if status_info == '':
        result = False

    # 2. Only ps result
    # ps -ef|grep srte
    # root     10905 10879  0 19:42 pts/0    00:00:00 grep --color=auto srte
    thread_info_ls = status_info.split('\n')
    if len(thread_info_ls) == 1 and 'grep' in thread_info_ls[0]:
        result = False

    # 3. Over given time offset
    # now 19:48 thread_start_time 19:42
    # or thread_start_time Oct15
    time_pattern = re.compile(r'\d{2}:\d{2}')
    month_patterns = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month in months:
        month_patterns.append(re.compile(month + r'\d{2}'))
    for thread_info in thread_info_ls:
        if 'grep' in thread_info:
            continue
        thread_start_time = re.findall(time_pattern, thread_info)[0]
        if thread_start_time != '00:00':
            thread_start_time = int(thread_start_time.replace(':', ''))
            now = int(time.strftime('%H:%M', time.localtime()).replace(':', ''))
            if now - thread_start_time > 2:
                result = False
        for month_pattern in month_patterns:
            thread_start_time = re.findall(month_pattern, thread_info)
            if len(thread_start_time) >= 1:
                result = False
                break
        if result is False:
            break
    return result


def project_redeploy(project_info, token, manual=False):
    """
    1. Find related project.
    2. Find all vms related to this project.
    3. Pull project code from gitlab on each vm.
    4. Exec given commands such as move git code to project directory, restart project.
    5. Check project status.
    :param project_info:
    :param token:
    :param manual:
    :return:
    """
    if not project_info or not token:
        return None
    if not manual:
        project = Project.query_by({
            'name': project_info.get('name'),
            'branch': project_info.get('default_branch')
        }, True)
        if project.repository != project_info.get('git_ssh_url') and project.repository != project_info.get('git_http_url'):
            return None
    else:
        project = Project.query_by({
            'name': project_info.get('name'),
            'repository': project_info.get('repository'),
            'branch': project_info.get('branch')
        }, True)
    if project and check_signature(project, token):
        flaskz_logger.info('Webhook: {}({}) start redeploy.'.format(project.name, project.branch))
        project.last_trig = datetime.now()

        Project.update(model_to_dict(project))
        branch = project.branch
        vm_list = project.vms
        for vm in vm_list:
            redeploy_command_list = vm.deploy_command.split('\n')
            vm_login_info = {
                'hostname': vm.host,
                'username': vm.username,
                'password': vm.password,
                'timeout': 10
            }
            git_info = {
                'git_dir': vm.git_dir,
                'repository': project.repository,
                'username': project.username,
                'password': project.password,
                'branch': branch
            }
            try:
                with ssh_session(**vm_login_info) as ssh:
                    git_pull_res, git_pull_info = ssh.git_pull(**git_info)
                    if git_pull_res is False:
                        return git_pull_res, git_pull_info
                    ssh.run_command_list(redeploy_command_list)
                    flaskz_logger.info('Info: {} -- {} git pull success.'.format(project.name, vm.host))
                    vm.status = check_project_status(ssh.run_command(vm.check_command), vm.check_command)
                    vm.last_trig = datetime.now()
                    restart_res = 'success' if vm.status is True else 'failed'
                    flaskz_logger.info('Info: {} -- {} restart {}.'.format(project.name, vm.host, restart_res))
            except Exception as e:
                flaskz_logger.error('Info: {} -- {} redeploy failed.\nError: {}'.format(project.name, vm.host, str(e)))
            finally:
                VM.update(model_to_dict(vm))
    return model_to_dict(project)
