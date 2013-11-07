###
### Use:
###   expect repository-mirroring.sh root 10.10.10.10 gerrit-user murano-api
###

### Manual way is the following:
###   1. git clone --mirror https://github.com/stackforge/murano-api.git
###   2. cd murano-api.git/
###   3. git fetch origin +refs/meta/*:refs/meta/*
###   4. git push --mirror ssh://tnurlygayanov@gerrit.mirantis.com:29418/murano/murano-api.git
###
###  after that you should not perform Step #3 again.

set timeout 1200

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "password"
send -- [lindex $argv 2]
send -- "\n"
expect "*@reposync*"

send -- "sudo su\n"
expect "*#*"

send -- "git clone --mirror https://github.com/stackforge/"
send -- [lindex $argv 4]
send -- ".git\n"
expect "*#*"

send -- "cd "
send -- [lindex $argv 4]
send -- ".git\n"
expect "*#*"

send -- "git fetch\n"
expect "*#*"

send -- "git push --mirror ssh://"
send -- [lindex $argv 3]
send -- "@gerrit.mirantis.com:29418/openstack/"
send -- [lindex $argv 4]
send -- ".git\n"
expect "*#*"

send -- "exit\n"
