## Network management UI
# Provides tools for wi-fi setup
from app import app
from flask import render_template
import os
from tools.misc import list_apps

with open('database/default_app') as f:
    default_app = f.readline()

def get_nets():

    string = os.popen('nmcli -t -m multiline dev wifi').read()
    schema = []
    net_list = []
    for row in string.split('\n'):

        data = row.split(':')
        if data[0] not in schema and data[0] != '':
            schema.append(data[0])
    net = {}
    for row in string.split('\n'):
        data = row.split(':')

        if data[0] == 'IN-USE':
            if len(net) == len(schema):
                net_list.append(net)
            else:
                print(len(net), len(schema))
            net = {data[0]: bool(data[1] == '*')}

            print(net)
        else:
            print(data[0])
            net[data[0]] = data[1:]

    return net_list

@app.route('/netui')
def networkUI():
    nets = get_nets()
    rows = ''
    for i in nets:
        if i['SSID'][0] != '':
            active = {False: '', True: '*'}[i['IN-USE']]
            rows += '''<tr><td>{active}</td><td>{ssid}</td><td>{security}</td><td>{rate}</td><td>{bars}</td></tr>
            '''.format(active=active,
                       ssid=i['SSID'][0],
                       security=i['SECURITY'][0],
                       rate=i['RATE'][0],
                       bars=i['BARS'][0])

    html = '''
    <table id=netui-table>
    <tr>
    <th>Active</th><th>SSID</th> <th>Security</th> <th>Rate</th> <th>Bars</th></tr>
    </tr>
    {}
    </table>
    <style>
    table, th{{
    margin: auto;
    border: 1px solid black;
    }}
    
    </style>
    '''.format(rows)

    x = list_apps()

    return render_template('config.html', netui = html, list_apps = x, current_app = default_app, netui_dir = 'config')

