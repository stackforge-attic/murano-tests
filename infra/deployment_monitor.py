# Copyright (c) 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import json
from flask import Flask, jsonify, request, abort, send_file


app = Flask(__name__)
hosts = {}


@app.route('/hosts', methods = ['GET'])
def get_list_of_hosts():
    return jsonify( {'hosts': hosts} )


@app.route('/hosts', methods = ['POST'])
def add_host():
    data = json.loads(request.data)

    if not 'host_name' in data or not 'ip' in data:
        abort(403)

    host = {data['host_name']: {'ip': data['ip'], 'files':[]}}
    hosts.update(host)

    with open('server.conf', 'w') as config_file:
        config_file.write(json.dumps(hosts))

    return jsonify( {'hosts': hosts} ), 201


@app.route('/hosts/<path:host_name>', methods = ['GET'])
def get_host(host_name):
    if not host_name in hosts:
        abort(404)

    return jsonify( {'host': hosts[host_name]} )


@app.route('/hosts/<path:host_name>', methods = ['DELETE'])
def delete_host(host_name):
    if not host_name in hosts:
        abort(404)

    del hosts[host_name]
    with open('server.conf', 'w') as config_file:
        config_file.write(json.dumps(hosts))

    return 'OK', 200


@app.route('/hosts/<path:host_name>/files', methods = ['POST'])
def add_file(host_name):
    if not host_name in hosts:
        abort(404)

    for f in request.files:
        hosts[host_name]['files'].append(f.filename)
        directory = os.path.join('/var/monitor/files', host_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = os.path.join(directory, secure_filename(f.filename))
        f.save(file_name)

    with open('server.conf', 'w') as config_file:
        config_file.write(json.dumps(hosts))

    return jsonify( {'host': hosts[host_name]} )


@app.route('/hosts/<path:host_name>/files/<path:file_name>',
           methods = ['GET'])
def get_file(host_name, file_name):
    if (not host_name in hosts or
        not file_name in hosts[host_name]['files']):
        abort(404)

    path = os.path.join('/var/monitor/files', host_name)
    return send_from_directory(path, file_name)


if __name__ == '__main__':
    with open('server.conf', 'r') as config_file:
        hosts = json.loads(config_file.read())
    app.run(debug = True, port = 7007)
