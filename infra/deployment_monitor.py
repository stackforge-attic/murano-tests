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

import json
from flask import Flask, jsonify, request

app = Flask(__name__)


config_file = open('server.conf', 'r')
try:
    hosts = json.loads(config_file.read())
    config_file.close()
except:
    hosts = {}


@app.route('/')
def index():
    return "This is the Deployment Monitor server"


@app.route('/hosts', methods = ['GET', 'POST'])
def hosts_url():
    if request.method == 'GET':
        return jsonify( { 'hosts': hosts } )

    if request.method == 'POST':
        data = json.loads(request.data)

        if not 'host_name' in data or not 'ip' in data:
            msg = "Need to specify the host name and IP address"
            return msg, 403

        host = {data['host_name']: {'ip': data['ip'], 'files':[]}}
        hosts.update(host)

        config_file = open('server.conf', 'w')
        config_file.write(str(hosts))
        config_file.close()

        return jsonify( { 'host': host } ), 201


@app.route('/hosts/<host_name>', methods = ['GET', 'POST', 'DELETE'])
def specific_host_url(host_name):
    if not host_name in hosts:
        return 'Host does not exist', 404

    if request.method == 'GET':
        return jsonify( { 'host': hosts[host_name] } )

    if request.method == 'DELETE':
        del hosts[host_name]
        return 'OK', 200

    if request.method == 'POST':
        for f in request.files:
            hosts[host_name]['files'].append(f.filename)
            directory = '/var/monitor/files/{0}/'.format(host_name)
            if os.path.exists(directory):
                os.makedirs(directory)
            f.save(directory + secure_filename(f.filename))

        return jsonify( { 'host': hosts[host_name] } )


@app.route('/hosts/<host_name>/files/<file_name>')
def files(host_name, file_name):
    try:
        directory = '/var/monitor/files/{0}/'.format(host_name)
        data = open(directory + file_name, 'r').read()
    except:
        msg = "ERROR: File {0}{1} not found"
        return msg.format(directory, file_name), 404

    return jsonify( { 'file': {'name': file_name, 'data': data} } )


if __name__ == '__main__':
    app.run(debug = True, port = 7007)
