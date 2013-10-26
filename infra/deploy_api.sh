set timeout 1200

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "password"
send -- [lindex $argv 2]
send -- "\n"
expect "*root@A1box*"

send -- "yum makecache -y\n"
expect "*root@A1box*"
send -- "yum update -y\n"
expect "*root@A1box*"
send -- "yum install python-memcached -y\n"
expect "*root@A1box*"

send -- "echo 'RABBITMQ_HOST = \'172.18.124.201\'' >> /etc/murano-deployment/lab-binding.rc\n"
expect "*root@A1box*"
send -- "rm -rf /opt/git\n"
expect "*root@A1box*"
send -- "mkdir -p /opt/git\n"
expect "*root@A1box*"
send -- "cd /opt/git\n"
expect "*root@A1box*"
send -- "git clone https://github.com/stackforge/murano-deployment -b release-0.2\n"
expect "*root@A1box*"

send -- "cd murano-deployment/devbox-scripts/\n"
expect "*root@A1box*"
send -- "./murano-git-install.sh prerequisites\n"
expect "*root@A1box*"
send -- "./murano-git-install.sh install\n"
expect "*root@A1box*"

send -- "cd /opt/git/murano-api\n"
expect "*root@A1box*"
send -- "git fetch https://review.openstack.org/stackforge/murano-api "
send -- [lindex $argv 3]
send -- " && git checkout FETCH_HEAD\n"
expect "*root@A1box*"
send -- "sh setup-centos.sh install\n"
expect "*root@A1box*"

send -- "exit\n"
