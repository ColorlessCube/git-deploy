import hmac
from datetime import datetime

from flaskz.log import flaskz_logger, get_log_data
from flaskz.models import model_to_dict

from .ssh import ssh_session
from ..modules import Project, VM


def check_signature(project, token):
    return project.token == token


def check_project_status(command):
    return True


def project_redeploy(project_info, token):
    if not project_info or not token:
        return
    project = Project.query_by({
        'name': project_info.get('name'),
        'repository': project_info.get('git_ssh_url'),
        'branch': project_info.get('default_branch')
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
                'password': vm.password
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
                    vm.status = check_project_status(ssh.run_command(vm.check_command))
                    vm.last_trig = datetime.now()
                    flaskz_logger.info('Info: {} -- {} redeploy success.'.format(project.name, vm.host))
            except Exception as e:
                flaskz_logger.error('Info: {} -- {} redeploy failed.\nError: {}'.format(project.name, vm.host, str(e)))
            finally:
                VM.update(model_to_dict(vm))