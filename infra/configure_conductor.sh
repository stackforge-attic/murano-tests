set timeout 30

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "@murano
send -- "sudo su\n"
expect "@murano"
send -- "sed -i \"s/init_scripts_dir = \/etc\/murano\/init-scripts/init_scripts_dir = \/opt\/git\/murano-conductor\/etc\/init-scripts/\" /etc/murano-conductor/conductor.conf\n"
expect "@murano"
send -- "sed -i \"s/agent_config_dir = \/etc\/murano\/agent-config/agent_config_dir = \/etc\/murano-conductor\/data\/templates\/agent-config\" /etc/murano-conductor/conductor.conf\n"
expect "@murano"
