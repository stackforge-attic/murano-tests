from pysphere import VIServer
server = VIServer()
server.connect("1.2.2.2", "user", "password")

vm = server.get_vm_by_name("vm")
vm.revert_to_snapshot()

print "VM prepared."
