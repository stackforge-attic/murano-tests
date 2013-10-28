set timeout 1200

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "password"
send -- [lindex $argv 2]
send -- "\n"
expect "*root@A2box*"

send -- "yum makecache -y\n"
expect "*root@A2box*"
send -- "yum update -y\n"
expect "*root@A2box*"
send -- "yum install python-memcached -y\n"
expect "*root@A2box*"

send -- "sed -i \"s/LAB_HOST=''/LAB_HOST='"
send -- [lindex $argv 4]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "*root@A2box*"
send -- "sed -i \"s/BRANCH_NAME=''/BRANCH_NAME='"
send -- [lindex $argv 5]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "*root@A2box*"
send -- "rm -rf /opt/git\n"
expect "*root@A2box*"
send -- "mkdir -p /opt/git\n"
expect "*root@A2box*"
send -- "cd /opt/git\n"
expect "*root@A2box*"
send -- "git clone https://github.com/stackforge/murano-deployment -b "
send -- [lindex $argv 5]
send -- "\n"
expect "*root@A2box*"

send -- "cd murano-deployment/devbox-scripts/\n"
expect "*root@A2box*"
send -- "./murano-git-install.sh prerequisites\n"
expect "*root@A2box*"
send -- "./murano-git-install.sh install\n"
expect "*root@A2box*"

send -- "sed -i \"s/connection = sqlite:///murano.sqlite/connection = mysql://murano:swordfish@localhost:3306/murano/\" /etc/murano-api/murano-api.conf\n"
expect "*root@A2box*"
send -- "/etc/init.d/murano-api restart\n"
expect "*root@A2box*"

send -- "cd /opt/git/murano-dashboard\n"
expect "*root@A2box*"
send -- "git fetch https://review.openstack.org/stackforge/murano-dashboard "
send -- [lindex $argv 3] 
send -- " && git checkout FETCH_HEAD\n"
expect "*root@A2box*"
send -- "sh setup-centos.sh install\n"
expect "*root@A2box*"

send -- "exit\n"
