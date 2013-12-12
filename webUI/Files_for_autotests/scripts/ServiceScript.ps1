$stream = [System.IO.StreamWriter] "C:/test_report.txt"
	$stream.WriteLine(“Test Report”)

	$host_name = [System.Net.Dns]::GetHostByName((hostname)).HostName
	$stream.WriteLine(“Host: $host_name”)

	$ip_address = [System.Net.Dns]::GetHostByName((hostname)).AddressList.IPAddressToString
	$stream.WriteLine(“IP Address: $ip_address”)

	$win_agent = Get-Process WindowsAgent | Select-Object name,fileversion,productversion,company
	if ($win_agent) { $agent_status = ‘running’ } else { $agent_status = ‘error’ }
	$stream.WriteLine(“Murano Windows Agent Process Status: $agent_status”)
	if ($win_agent) { $agent_version = $win_agent.FileVersion
	$stream.WriteLine(“Murano Windows Agent Version: $agent_version”) }

	$stream.WriteLine(“Firewall Opened Ports:”)
	$firewall_rules = Get-NetFirewallPortFilter | Select-Object Protocol, RemotePort, LocalPort
	foreach ($rule in $firewall_rules) { $stream.WriteLine($rule) }

	$stream.close()
