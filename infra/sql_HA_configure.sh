set timeout 30

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "@murano"

send -- "sudo su\n"
expect "@murano"
send -- "sed -i \"s/connection = mysql:\\/\\/murano:swordfish@localhost:3306\\/murano/connection = mysql:\\/\\/murano:swordfish@"
send -- [lindex $argv 2]
send -- ":3306\\/murano/\" /etc/murano-api/murano-api.conf\n"
expect "@murano"
send -- "service murano-api restart\n"
expect "@murano"
send -- "exit\n"
