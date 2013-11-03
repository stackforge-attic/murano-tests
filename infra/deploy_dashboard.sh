set timeout 1200

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "*@murano-devbox*"

send -- "sudo su\n"
expect "*@murano-devbox*"

send -- "cd /opt/git/murano-dashboard\n"
expect "*@murano-devbox*"
send -- "git fetch https://review.openstack.org/stackforge/murano-dashboard "
send -- [lindex $argv 2]
send -- " && git checkout FETCH_HEAD\n"
expect "*@murano-devbox*"
send -- "sh setup-centos.sh install\n"
expect "*@murano-devbox*"
send -- "sh setup.sh install\n"
expect "*@murano-devbox*"

send -- "exit\n"
