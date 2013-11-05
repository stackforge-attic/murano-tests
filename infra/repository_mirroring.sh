###
### Use:
###   expect repository-mirroring.sh root 10.10.10.10 gerrit-user murano-api
###

set timeout 1200

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "*@reposync*"

send -- "git clone --mirror https://github.com/stackforge/"
send -- [lindex $argv 4]
send -- ".git\n"
expect "*@reposync*"

send -- "cd "
send -- [lindex $argv 4]
send -- ".git\n"
expect "*@reposync*"

send -- "git fetch origin +refs/meta/*:refs/meta/*"
expect "*@reposync*"

send -- "git push --mirror ssh://"
send -- [lindex $argv 3]
send -- "@gerrit.mirantis.com:29418/murano/"
send -- [lindex $argv 4]
send -- ".git\n"
expect "*@reposync*"

send -- "exit\n"
