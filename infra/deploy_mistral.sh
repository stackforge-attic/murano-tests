set timeout 200

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "@mistral"

send -- "sudo su\n"
expect "@mistral"

send -- "git clone https://github.com/stackforge/mistral -b "
send -- [lindex $argv 3]
send -- "\n"
expect "@mistral"

send -- "cp mistral/etc/mistral.conf.example mistral/etc/mistral.conf\n"
expect "@mistral"


send -- "sed -i \"s/auth_enable = True/auth_enable = False/\" mistral/etc/mistral.conf\n"
expect "@mistral"
send -- "sed -i \"s/rabbit_host = localhost/rabbit_host = "
send -- [lindex $argv 2]
send -- "/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/rabbit_port = 5672/rabbit_port = "
send -- [lindex $argv 4]
send -- "/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/rabbit_virtual_host = \\//rabbit_virtual_host = "
send -- [lindex $argv 5]
send -- "/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/rabbit_user = guest/rabbit_user = "
send -- [lindex $argv 5]
send -- "/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/rabbit_password = guest/rabbit_password = swordfish/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/auth_uri=http:\\/\\/localhost:5000\\/v3/auth_uri=http:\\/\\/"
send -- [lindex $argv 2]
send -- ":5000\\/v3/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/auth_host=localhost/auth_host="
send -- [lindex $argv 2]
send -- "/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/admin_user=admin/admin_user=AutotestUser/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/admin_password=password/admin_password=swordfish/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "sed -i \"s/admin_tenant_name=admin/admin_tenant_name=AutotestProject/\" mistral/etc/mistral.conf\n"
expect "@mistral"

send -- "cd mistral\n"
expect "@mistral"
send -- "screen -d -m bash -c 'tox -evenv -- python mistral/cmd/launch.py --server all --config-file etc/mistral.conf'\n"
sleep 120
