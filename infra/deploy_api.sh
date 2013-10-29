set timeout 1200

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "password"
send -- [lindex $argv 2]
send -- "\n"
expect "*root@A1box*"

send -- "cd /opt/git/murano-api\n"
expect "*root@A1box*"
send -- "sh setup-centos.sh uninstall\n"
expect "*root@A1box*"
send -- "git fetch https://review.openstack.org/stackforge/murano-api "
send -- [lindex $argv 3]
send -- " && git checkout FETCH_HEAD\n"
expect "*root@A1box*"
send -- "sh setup-centos.sh install\n"
expect "*root@A1box*"

send -- "exit\n"
