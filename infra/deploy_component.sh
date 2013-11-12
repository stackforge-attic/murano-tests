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
except "@murano"
send -- "sh setup.sh install > 4.log\n"
expect "@murano"
send -- "service "
send -- [lindex $argv 3]
send -- " restart\n"
expect "@murano"

send -- "exit\n"
