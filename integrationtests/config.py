import os
from oslo.config import cfg


murano_group = cfg.OptGroup(name='murano', title="murano")

MuranoGroup = [
    cfg.StrOpt('auth_url',
               default='http://127.0.0.1:5000/v2.0/',
               help="keystone url"),
    cfg.StrOpt('murano_url',
               default='http://127.0.0.1:8082',
               help="murano url"),
    cfg.StrOpt('metadata_url',
               default='http://127.0.0.1:8084/v1',
               help="metadata url"),
    cfg.StrOpt('user',
               default='admin',
               help="keystone user"),
    cfg.StrOpt('password',
               default='pass',
               help="password for keystone user"),
    cfg.StrOpt('tenant',
               default='admin',
               help='keystone tenant'),
    cfg.BoolOpt('deploy',
                default=False,
                help='Run deploy tests or no')
]


def register_config(config, config_group, config_opts):

    config.register_group(config_group)
    config.register_opts(config_opts, config_group)

path = os.path.join("%s/config.conf" % os.getcwd())

if os.path.exists(path):
    cfg.CONF([], project='muranointegration', default_config_files=[path])

register_config(cfg.CONF, murano_group, MuranoGroup)

murano = cfg.CONF.murano
