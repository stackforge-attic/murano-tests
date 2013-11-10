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
from flask import Flask, jsonify, request, abort


app = Flask(__name__)


with open('server.conf', 'r') as config_file:
    hosts = json.loads(config_file.read())


@app.route('/hosts', methods = ['GET', 'POST'])
def hosts_url():
    if request.method == 'GET':
        return jsonify('hosts': hosts)

    if request.method == 'POST':
        data = json.loads(request.data)

        if not 'host_name' in data or not 'ip' in data:
            msg = "Need to specify the host name and IP address"
            return msg, 403

        host = {data['host_name']: {'ip': data['ip'], 'files':[]}}
        hosts.update(host)

        with open('server.conf', 'w') as config_file:
            config_file.write(str(hosts))

        return jsonify('hosts': hosts), 201


@app.route('/hosts/<host_name>', methods = ['GET', 'POST', 'DELETE'])
def specific_host_url(host_name):
    if not host_name in hosts:
        return 'Host does not exist', 404

    if request.method == 'GET':
        return jsonify('host': hosts[host_name])

    if request.method == 'DELETE':
        del hosts[host_name]
        return 'OK', 200

    if request.method == 'POST':
        for f in request.files:
            hosts[host_name]['files'].append(f.filename)
            directory = os.path.join('/var/monitor/files', host_name)
            if os.path.exists(directory):
                os.makedirs(directory)
            file_name = os.path.join(directory, secure_filename(f.filename))
            f.save(file_name)

        return jsonify('host': hosts[host_name])


@app.route('/hosts/<host_name>/files/<file_name>')
def files(host_name, file_name):
    path = os.path.join('/var/monitor/files', host_name, file_name)
    with open(path, 'r') as data_file:
        try:
            data = data_file.read()
        except:
            abort(404)

    return jsonify('file': {'name': file_name, 'data': data})


if __name__ == '__main__':
    app.run(debug = True, port = 7007)
