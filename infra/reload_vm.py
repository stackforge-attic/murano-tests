import sys
from pysphere import VIServer
server = VIServer()
server.connect(sys.argv[1], sys.argv[2], sys.argv[3])

vm = server.get_vm_by_name(sys.argv[4])
vm.revert_to_snapshot()

print "VM prepared."
