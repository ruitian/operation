# coding=utf-8
from fabric.api import local, env, run, cd

env.hosts = [
    'work@192.168.60.59'
]

remote_project_dir = '/home/work/zhangrui/CMS-OPERATION'
remote_service_dir = '/home/work/dongbingwei'
def update():
    with cd(remote_project_dir):
        print '正在更新代码..'
        run('git pull origin zhangrui')

def stop(server_name):
    with cd(remote_service_dir):
        print '正在停止%s' % server_name
        run('supervisorctl -c supervisor.conf stop %s' % server_name)
        print '%s已停止' % server_name

def start(server_name):
    with cd(remote_service_dir):
        print '正在开启%s' % server_name
        run('supervisorctl -c supervisor.conf start %s' % server_name)
        print '%s已开启' % server_name


def restart(server_name):
    with cd(remote_service_dir):
        print '正在重启%s' % server_name
        run('supervisorctl -c supervisor.conf restart %s' % server_name)
        print '%s已重启' % server_name
