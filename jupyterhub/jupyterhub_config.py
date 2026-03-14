import os
from dockerspawner import DockerSpawner
from jupyterhub.spawner import LocalProcessSpawner

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

c.JupyterHub.spawner_class = DockerSpawner

c.DockerSpawner.image = 'jupyter/base-notebook:latest'
c.DockerSpawner.network_name = os.environ.get('DOCKER_NETWORK_NAME')

admin_users = os.environ.get('JUPYTERHUB_ADMIN_USERS', '').split(',')
c.Authenticator.admin_users = set(filter(None, admin_users))

allowed_users = os.environ.get('JUPYTERHUB_ALLOWED_USERS', '').split(',')
c.Authenticator.allowed_users = set(filter(None, allowed_users))

c.DockerSpawner.extra_host_config = {
    'mem_limit': '2g',
    'cpu_quota': 100000,
    'cpu_period': 100000
}

c.DockerSpawner.remove = True

c.JupyterHub.services = [
    {
        'name': 'configurable-http-proxy',
        'command': ['configurable-http-proxy', '--ip', '0.0.0.0', '--port', '8000'],
    }
]
