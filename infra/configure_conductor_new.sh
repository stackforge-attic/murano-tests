set timeout 30

send_user "\n\nStart to login to the test bed...\n\n"

spawn /usr/bin/ssh  [lindex $argv 0]@[lindex $argv 1]
expect "@murano"
send -- "sudo su\n"
expect "@murano"
send -- "sed -i \"s/#amqp_durable_queues=false/amqp_durable_queues=false/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#amqp_auto_delete=false/amqp_auto_delete=false/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_host=localhost/rabbit_host="
send -- [lindex $argv 2]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_port=5672/rabbit_port="
send -- [lindex $argv 3]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_hosts=\$rabbit_host:\$rabbit_port/rabbit_hosts=\$rabbit_host:\$rabbit_port/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_use_ssl=false/rabbit_use_ssl="
send -- [lindex $argv 4]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_userid=guest/rabbit_userid="
send -- [lindex $argv 5]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_password=guest/rabbit_password=swordfish/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_virtual_host=\\//rabbit_virtual_host="
send -- [lindex $argv 5]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_retry_interval=1/rabbit_retry_interval=1/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_retry_backoff=2/rabbit_retry_backoff=2/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_max_retries=0/rabbit_max_retries=0/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/#rabbit_ha_queues=false/rabbit_ha_queues=false/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/auth_url = http:\\/\\/localhost:5000\\/v2.0/auth_url = http:\\/\\/"
send -- [lindex $argv 2]
send -- ":5000\\/v2.0/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/host = localhost/host = "
send -- [lindex $argv 2]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/port = 5672/port = "
send -- [lindex $argv 3]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/ssl = False/ssl = "
send -- [lindex $argv 4]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/login = guest/login = "
send -- [lindex $argv 5]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/password = guest/password = swordfish/\" /etc/murano-api.conf\n"
expect "@murano"
send -- "sed -i \"s/virtual_host = \\//virtual_host = "
send -- [lindex $argv 5]
send -- "/\" /etc/murano-api.conf\n"
expect "@murano"
