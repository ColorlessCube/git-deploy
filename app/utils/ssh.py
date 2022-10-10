import errno
import os
import re
import stat
import time
from contextlib import contextmanager

import paramiko

__all__ = ['ssh_session', 'SSH']


@contextmanager
def ssh_session(hostname, username, password=None, port=22, **kwargs):
    """
    with ssh_session(host, username, password) as ssh:
        ssh.run_command("ls -l")
    """
    ssh_client = SSHForGit(hostname=hostname, username=username, password=password, port=port, **kwargs)
    yield ssh_client
    ssh_client.close()


class SSH(object):
    def __init__(self, hostname, username, password=None, port=22, **kwargs):
        """
        ssh = SSH(host, username, password)
        """
        self._username = username
        self._password = password

        self.transport = paramiko.Transport((hostname, port))
        self.transport.connect(username=username, password=password, **kwargs)

        self.ssh = paramiko.SSHClient()
        self.ssh._transport = self.transport
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @property
    def sftp(self):
        if not hasattr(self, '_sftp'):
            self._sftp = paramiko.SFTPClient.from_transport(self.transport)
        return self._sftp

    @property
    def channel(self):
        if not hasattr(self, '_channel'):
            self._channel = self.ssh.invoke_shell(height=100000)
            # self._channel.settimeout(1)
        return self._channel

    def run_command(self, command):
        """
        Run the command
        ssh.run_command("ls -l")
        """
        command = command.strip()
        self.channel.send(command + '\n')
        output = self._get_output(command)

        if self._password and command.lower().startswith('sudo') and 'assword' in output:  # input password
            pwd_ouput = self.run_command(self._password)
            if 'assword' in pwd_ouput:
                return output
            return self.run_command(command)

        return output

    def run_command_list(self, command_list, last_result=False):
        """
        Run a command list
        By default, returns the list of results , if last_result==True returns the result of the last command
        ssh.run_command_list(['cd /usr/projects/git/srte',
                      'pwd',
                      'git pull origin master',
                      'wiui@hotmail.com',
                      '11111111'
                      ], True)
        """
        re_list = []
        for command in command_list:
            re_list.append(self.run_command(command))
        if last_result is True:
            return re_list[-1]
        return re_list

    def sftp_get_dir(self, remote_dir, local_dir):
        """
        Download remote direction to local
        Return the local files list
        ssh.sftp_get_dir("/usr/projects/git/srte/src/", "/Users/taozh/Work/Codes/ssh_test/sftp")
        """
        if not self._path_exists(remote_dir):
            return False
        remote_dir = _remove_end_slash(remote_dir)
        local_dir = _remove_end_slash(local_dir)
        if not os.path.exists(local_dir):
            os.mkdir(local_dir)
        all_files = self.listdir(remote_dir, True)
        local_files = []
        for f in all_files:
            local_filename = f.replace(remote_dir, local_dir)
            local_filepath = os.path.dirname(local_filename)
            local_files.append(local_filepath)
            if not os.path.exists(local_filepath):
                os.makedirs(local_filepath)
            self.sftp.get(f, local_filename)
        return local_files

    def listdir(self, path, recursion=False):
        """
        List all files in the given path
        ssh.listdir("/usr/projects/git/srte/src/")
        """
        all_files = []
        path = _remove_end_slash(path)
        if path[-1] == '/':
            path = path[0:-1]
        files = self.sftp.listdir_attr(path)
        for f in files:
            filename = path + '/' + f.filename
            if stat.S_ISDIR(f.st_mode):  # 如果是文件夹的话递归处理
                if recursion is True:
                    all_files.extend(self.listdir(filename, recursion))
            else:
                all_files.append(filename)
        return all_files

    def close(self):
        """Close the connect"""
        self.channel.close()
        self.ssh.close()

    def _path_exists(self, path):
        """Return whether the path exists"""
        try:
            self.sftp.stat(path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True

    def _get_output(self, command):
        output = self._recv_data()
        output = _clear_redundant(output, command)
        return output

    def _recv_data(self):
        """Receive the command output"""
        while not self.channel.recv_ready():
            time.sleep(0.01)
        res_list = []
        time.sleep(0.2)  # Solve the problem of incomplete data
        # cmd_pattern = re.compile('.*[#$] ' + command) # Does not work with password entry
        while True:
            data = self.channel.recv(1024)
            info = data.decode()
            res = info.replace(' \r', '')
            res_list.append(res)
            if len(info) < 1024:  # read speed > write speed
                if info.endswith(('# ', '$ ', ': ')):
                    break

        return ''.join(res_list)


def _clear_redundant(txt, command):
    """
    Clear the redundant information
    - Welcome info      ex)Welcome to Ubuntu...
    - Last login info   ex)Last login...
    - Path info         ex)[root@localhost ~]...
    - Command info      ex)ls -l
    """
    if txt.startswith(command):
        txt = txt[len(command):]
    cmd_pattern = re.compile('.*([#$])?( )*' + re.escape(command))  # 处理转义字符
    search_result = cmd_pattern.search(txt)
    if search_result:
        txt = txt[search_result.end():]
    path_pattern = re.compile('.*[#$] ')
    txt = path_pattern.sub('', txt)  # remove the path info
    txt = txt.replace(command + '\r\n', '')  # remove the command
    return txt.strip()


def _remove_end_slash(path):
    """Remove ending slash """
    if path[-1] == '/':
        return path[0:-1]
    return path


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
        git_pull_info = self.run_command('git pull origin ' + branch)
        if 'username' in git_pull_info.lower():
            if username:
                self.run_command(username)
                git_pull_info = self.run_command(password)
            else:
                return False, 'Git pull operation needs account info.'
        if 'fatal' in git_pull_info or 'hint' in git_pull_info:
            git_pull_res = False
            info = git_pull_info
        else:
            git_pull_res = True
            info = 'Git pull succeeded.'

        return git_pull_res, info

    def list_dir(self, dir_path):
        """
        Return all files in the given directory.
        :param dir_path:
        :return: list
        """
        return self.sftp.listdir(dir_path)

    def zip(self, dir_path, zip_name):
        if dir_path.endswith('/'):
            dir_path = dir_path[:-1]
        dir_list = dir_path.split('/')
        parent_dir_path = '/'.join(dir_list[:-1])
        if not zip_name.endswith('.zip'):
            zip_name += '.zip'
        self.run_command('cd ' + parent_dir_path)
        self.run_command('zip -r ' + zip_name + ' ' + dir_list[-1])
        if zip_name in self.list_dir(parent_dir_path):
            return True
        else:
            return False

    def rm_all(self, dir_path):
        """
        Remove all files in the directory, but it will not remove .file_name, which means file like .git could be saved.
        :param dir_path:
        :return:
        """
        if dir_path.endswith('/'):
            dir_path = dir_path[:-1]
        self.run_command('rm -rf ' + dir_path + '/*')
        files = self.list_dir(dir_path)
        for file in files:
            if not file.startswith('.'):
                return False
        return True

    def cp_file(self, ori_file, dst_dir):
        self.run_command('\\cp -rf ' + ori_file + ' ' + dst_dir)
        return True

    def stop_service(self, name):
        res = self.run_command('supervisorctl stop ' + name)
        if 'error' in res.lower():
            if 'not running' in res.lower():
                return True, 'Service stopped.'
            else:
                return False, 'Service stop failed.'
        else:
            return True, 'Service stopped.'

    def start_service(self, name):
        # To prevent any config changed, reread config file before start service
        self.run_command('supervisorctl reread')
        self.run_command('supervisorctl update')
        res = self.run_command('supervisorctl start ' + name)
        if 'error' in res.lower():
            if 'already started' in res.lower():
                return True, 'Service started.'
            else:
                return False, 'Service stop failed.'
        else:
            return True, 'Service started.'

    def scp(self, local_path, host, username, password, dir_path):
        """
        Copy all files in local path to remote host directory path.
        :param local_path:
        :param host:
        :param username:
        :param password:
        :param dir_path:
        :return:
        """
        self.run_command('\\scp -r ' + local_path + '/* ' + username + '@' + host + ':' + dir_path)
        res = self.run_command(password)
        if '100%' in res:
            return True
        else:
            return False

    def _get_all_files_in_remote_dir(self, sftp, remote_dir):
        """
        递归遍历远程服务器指定目录下的所有文件
        :param sftp:
        :param remote_dir:
        :return:
        """
        all_files = []
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]
        files = sftp.listdir_attr(remote_dir)
        for file in files:
            filename = remote_dir + '/' + file.filename
            if stat.S_ISDIR(file.st_mode):  # 如果是文件夹的话递归处理
                all_files.extend(self._get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)
        return all_files

    def sftp_get_dir(self, remote_dir, local_dir):
        try:
            all_files = self._get_all_files_in_remote_dir(self.sftp, remote_dir)
            # root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
            # local_dir = os.path.abspath(os.path.join(root, local_dir))
            # subprocess.run('rm -rf ' + local_dir + '/*', shell=True)
            for file in all_files:
                if '.git' in file:
                    continue
                local_filename = file.replace(remote_dir, local_dir)
                local_filepath = os.path.dirname(local_filename)
                if not os.path.exists(local_filepath):
                    os.makedirs(local_filepath)
                self.sftp.get(file, local_filename)
        except Exception as e:
            return False, e
        return True, 'SFTP succeeded.'
