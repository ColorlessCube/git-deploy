import os
import time
import stat
from contextlib import contextmanager

from flaskz.ext.ssh import SSH

__all__ = ['ssh_session', 'SSHForGit']


@contextmanager
def ssh_session(hostname, username, password=None, port=22, **kwargs):
    """
    with ssh_session(host, username, password) as ssh:
        ssh.run_command("ls -l")
    """
    ssh_client = SSHForGit(hostname=hostname, username=username, password=password, port=port, **kwargs)
    yield ssh_client
    ssh_client.close()


class SSHForGit(SSH):
    def git_pull(self, git_dir, repository, username=None, password=None, branch='main'):
        """
        :param git_dir:
        :param repository:
        :param username:
        :param password:
        :param branch:
        :return:
        """
        self.run_command_list(['mkdir -p ' + git_dir, 'cd ' + git_dir])
        git_init_res = True
        files = self.run_command('ls -a')
        remote_info = self.run_command('git remote -v')
        if '.git' not in files:
            git_init_info = self.run_command('git init')
            if 'fetch' not in git_init_info.lower():
                git_init_res = False
        if 'fetch' not in remote_info:
            self.run_command('git remote add origin "' + repository + '"')
            remote_info = self.run_command('git remote -v')
            if repository not in remote_info:
                git_init_res = False
        if not git_init_res:
            return False, 'Git init failed.'

        self.run_command('git checkout -b ' + branch)
        try:
            if username and password:
                git_pull_info = self.run_command_list(['git pull origin ' + branch, username, password], True)
            else:
                git_pull_info = self.run_command('git pull origin ' + branch)
            if 'fatal' in git_pull_info or 'hint' in git_pull_info:
                git_pull_res, info = False, git_pull_info
            else:
                git_pull_res, info = True, 'Git pull succeeded.'
        except TimeoutError:
            git_pull_res, info = False, 'Git pull timeout.'
        return git_pull_res, info

