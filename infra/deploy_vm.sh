set timeout 30

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "*@murano-devbox*"

send -- "sudo su\n"
expect "*@murano-devbox*"

send -- "sed -i \"s/LAB_HOST=''/LAB_HOST='"
send -- [lindex $argv 2]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "*@murano-devbox*"
send -- "sed -i \"s/BRANCH_NAME=''/BRANCH_NAME='"
send -- [lindex $argv 3]
send -- "'/\" /etc/murano-deployment/lab-binding.rc\n"
expect "*@murano-devbox*"
send -- "rm -rf /opt/git; mkdir -p /opt/git; cd /opt/git\n"
expect "*@murano-devbox*"
send -- "git clone https://github.com/stackforge/murano-deployment -b "
send -- [lindex $argv 3]
send -- "\n"
expect "*@murano-devbox*"

set timeout 600
send -- "cd murano-deployment/devbox-scripts/\n"
expect "*@murano-devbox*"
send -- "./murano-git-install.sh prerequisites\n"
expect "*@murano-devbox*"
send -- "./murano-git-install.sh install\n"
expect "*@murano-devbox*"

set timeout 30
send -- "sed -i \"s/connection = sqlite:\\/\\/\\/murano.sqlite/connection = mysql:\\/\\/murano:swordfish@localhost:3306\\/murano/\" /etc/murano-api/murano-api.conf\n"
expect "*@murano-devbox*"
send -- "sed -i \"s/port = 5672/port = "
send -- [lindex $argv 4]
send -- "/\" /etc/murano-api/murano-api.conf\n"
expect "*@murano-devbox*"
send -- "sed -i \"s/port = 5672/port = "
send -- [lindex $argv 4]
send -- "/\" /etc/murano-conductor/conductor.conf\n"
expect "*@murano-devbox*"
send -- "sed -i \"s/\\\"BootFromVolume\\\": true,//\" /etc/murano-conductor/data/templates/cf/Linux.template\n"
expect "*@murano-devbox*"
send -- "sed -i \"s/\\\"BootFromVolume\\\": true,//\" /etc/murano-conductor/data/templates/cf/Windows.template\n"
expect "*@murano-devbox*"

send -- "restart murano-api\n"
expect "*@murano-devbox*"
send -- "restart murano-conductor\n"
expect "*@murano-devbox*"

send -- "exit\n"
