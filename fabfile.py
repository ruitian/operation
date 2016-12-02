# coding=utf-8
from fabric.api import local, env, run, cd

env.hosts = [
    'work@192.168.60.59'
]

remote_service_dir = '/home/work/dongbingwei'
def update(branch, route):
    with cd('/home/work/%s/CMS-OPERATION' % route):
        print '正在从%s分支更新%s路径下的代码...' % (branch, route)
        run('git pull origin %s' % branch)

def stop(service):
    with cd(remote_service_dir):
        print '正在停止%s' % service
        run('supervisorctl -c supervisor.conf stop %s' % service)
        print '%s已停止' % service

def start(service):
    with cd(remote_service_dir):
        print '正在开启%s' % service
        run('supervisorctl -c supervisor.conf start %s' % service)
        print '%s已开启' % service


def restart(service):
    with cd(remote_service_dir):
        print '正在重启%s' % service
        run('supervisorctl -c supervisor.conf restart %s' % service)
        print '%s已重启' % service
