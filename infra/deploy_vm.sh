# Use:
#   expect infra/deploy_vm.sh ubuntu 10.100.0.6 172.18.11.4 master 5672 True A002box
#

set timeout 30

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "@murano"

send -- "sudo su\n"
expect "@murano"

send -- "sed -i \"s/LAB_HOST=''/LAB_HOST='"
send -- [lindex $argv 2]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "@murano"

send -- "sed -i \"s/RABBITMQ_VHOST='A001box'/RABBITMQ_VHOST='"
send -- [lindex $argv 6]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "@murano"

send -- "sed -i \"s/RABBITMQ_LOGIN='A001box'/RABBITMQ_LOGIN='"
send -- [lindex $argv 6]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "@murano"

send -- "sed -i \"s/RABBITMQ_PORT=''/RABBITMQ_PORT='"
send -- [lindex $argv 4]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "@murano"

send -- "sed -i \"s/BRANCH_NAME=''/BRANCH_NAME='"
send -- [lindex $argv 3]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "@murano"
send -- "rm -rf /opt/git\n"
expect "@murano"
send -- "mkdir -p /opt/git\n"
expect "@murano"
send -- "cd /opt/git\n"
expect "@murano"
send -- "git clone https://github.com/stackforge/murano-deployment -b "
send -- [lindex $argv 3]
send -- "\n"
expect "@murano"

set timeout 600
send -- "cd murano-deployment/devbox-scripts/\n"
expect "@murano"
send -- "./murano-git-install.sh prerequisites\n"
expect "@murano"
send -- "./murano-git-install.sh install\n"
expect "@murano"

set timeout 30
send -- "sed -i \"s/connection = sqlite:\\/\\/\\/murano.sqlite/connection = mysql:\\/\\/murano:swordfish@localhost:3306\\/murano/\" /etc/murano/murano-api.conf\n"
expect "@murano"

send -- "sed -i \"s/ssl = False/ssl = "
send -- [lindex $argv 5]
send -- "/\" /etc/murano/murano-api.conf\n"
expect "@murano"

send -- "sed -i \"s/ssl = False/ssl = "
send -- [lindex $argv 5]
send -- "/\" /etc/murano/murano-conductor.conf\n"
expect "@murano"

send -- "sed -i \"s/\\\"BootFromVolume\\\": true,//\" /etc/murano-conductor/data/templates/cf/Linux.template\n"
expect "@murano"
send -- "sed -i \"s/\\\"BootFromVolume\\\": true,//\" /etc/murano-conductor/data/templates/cf/Windows.template\n"
expect "@murano"

send -- "sed -i \"s/murano_metadata_url = http:\\/\\/localhost:8084\\/v1/murano_metadata_url = http:\\/\\/"
send -- [lindex $argv 1]
send -- ":8084\\/v1/\" /etc/murano/murano-conductor.conf\n"
expect "@murano"

send -- "service murano-api restart\n"
expect "@murano"
send -- "service murano-conductor restart\n"
expect "@murano"

send -- "echo \"LANGUAGE_CODE='en'\" >> /etc/openstack-dashboard/local_settings.py\n"
expect "@murano"
send -- "service apache2 restart\n"
expect "@murano"
send -- "rm -rf /tmp/muranoconductor-cache/* /tmp/muranorepository-cache/*\n"
expect "@murano"

send -- "exit\n"
