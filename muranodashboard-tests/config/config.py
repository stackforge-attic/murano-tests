import os
from oslo.config import cfg

common_group = cfg.OptGroup(name='common', title="common configs")

CommonGroup = [
    cfg.StrOpt('base_url',
               default='http://127.0.0.1:8080',
               help="savanna url"),
    cfg.StrOpt('user',
               default='admin',
               help="keystone user"),
    cfg.StrOpt('password',
               default='pass',
               help="password for keystone user"),
    cfg.StrOpt('tenant',
               default='admin',
               help='keystone tenant')
]

def register_config(config, config_group, config_opts):

    config.register_group(config_group)
    config.register_opts(config_opts, config_group)

path = os.path.join("%s/config/config.conf"
                    % os.getcwd())

if os.path.exists(path):
    cfg.CONF([], project='muranodashboard', default_config_files=[path])

register_config(cfg.CONF, common_group, CommonGroup)

common = cfg.CONF.common