###
### Use:
###   expect deploy_component.sh user 10.10.10.10 /refs/for/master/344332 murano-api
###

set timeout 1200

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "@murano"

send -- "sudo su\n"
expect "@murano"

send -- "cd /opt/git/ ; rm -rf "
send -- [lindex $argv 3]
send -- "\n"
expect "@murano"

send -- "git clone https://github.com/stackforge/"
send -- [lindex $argv 3]
send -- "\n"
expect "@murano"

send -- "cd /opt/git/"
send -- [lindex $argv 3]
send -- "\n"
expect "@murano"
send -- "sh setup-centos.sh uninstall > 1.log\n"
expect "@murano"
send -- "sh setup.sh uninstall > 2.log\n"
expect "@murano"
send -- "git fetch https://review.openstack.org/stackforge/"
send -- [lindex $argv 3]
send -- " "
send -- [lindex $argv 2]
send -- " && git checkout FETCH_HEAD\n"
expect "@murano"
send -- "sh setup-centos.sh install > 3.log\n"
expect "@murano"
send -- "sh setup.sh install > 4.log\n"
expect "@murano"
send -- "sed -i \"s/\\\"BootFromVolume\\\": true,//\" /etc/murano-conductor/data/templates/cf/Linux.template\n"
expect "@murano"
send -- "sed -i \"s/\\\"BootFromVolume\\\": true,//\" /etc/murano-conductor/data/templates/cf/Windows.template\n"
expect "@murano"
send -- "service "
send -- [lindex $argv 3]
send -- " restart\n"
expect "@murano"

send -- "cd /tmp/muranorepository-data ; rm -rf *\n"
expect "@murano"
send -- "cd /tmp/muranorepository-cache ; rm -rf *\n"                            
expect "@murano"
send -- "cd /tmp/muranodashboard-cache ; rm -rf *\n"
expect "@murano"
send -- "cd /tmp/muranoconductor-cache ; rm -rf *\n"
expect "@murano"

send -- "python /usr/share/openstack-dashboard/manage.py syncdb --noinput\n"
expect "@murano"

send -- "service murano-repository restart\n"
send -- "service murano-conductor restart\n"
send -- "service apache2 restart\n"

send -- "exit\n"
