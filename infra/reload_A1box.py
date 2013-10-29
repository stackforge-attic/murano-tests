from pysphere import VIServer
server = VIServer()
server.connect("172.18.79.68", "root", "WinDCaaS")

vm = server.get_vm_by_name("A1box")
vm.revert_to_snapshot()

print "VM prepared."
