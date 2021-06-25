from ppadb.client import Client as AdbClient
import requests
import time
import os

# Credit to https://www.reddit.com/r/homeassistant/comments/o709m7/is_there_a_way_to_use_an_android_tv_controller/h2xrq66/

hassAddress = os.environ['HOME_ASSISTANT_ADDRESS']
token = os.environ['HOME_ASSISTANT_TOKEN']
tvHost = os.environ['ANDROID_HOST']
tvPort = os.getenv('ANDROID_PORT', 5555)
inputDevice = os.environ['ANDROID_INPUT_DEVICE']

authorization = f'Bearer {token}'

commands = {
    "EV_KEY       KEY_1                DOWN": {"entity" : "input_boolean.tv_key_1", "action": "toggle", "service": "input_boolean"},
    "EV_KEY       KEY_2                DOWN": {"entity" : "input_boolean.tv_key_2", "action": "toggle", "service": "input_boolean"},
    "EV_KEY       KEY_3                DOWN": {"entity" : "input_boolean.tv_key_3", "action": "toggle", "service": "input_boolean"},
    "EV_KEY       KEY_4                DOWN": {"entity" : "input_boolean.tv_key_4", "action": "toggle", "service": "input_boolean"},
    "EV_KEY       KEY_5                DOWN": {"entity" : "input_boolean.tv_key_5", "action": "toggle", "service": "input_boolean"},
    "EV_KEY       KEY_6                DOWN": {"entity" : "input_boolean.tv_key_6", "action": "toggle", "service": "input_boolean"},
}

def dump_getevent_by_line(connect):
    file_obj = connect.socket.makefile()
    while True:
        key_press = file_obj.readline().strip()
        print(key_press)
        if key_press in commands:
            print(key_press)
            send_keypress_to_hass(key_press)
        time.sleep(0.01)
    file_obj.close()
    connect.close()

def send_keypress_to_hass(key_press):
    d = commands[key_press]
    service = d['service']
    action = d['action']
    entity = d['entity']
    url = f"{hassAddress}/api/services/{service}/{action}"
    payload = "{\"entity_id\": \"" + entity + "\"}"
    headers = {
    'Authorization': authorization,
    'Content-Type': 'application/json'
    }
    requests.request("POST", url, headers=headers, data=payload)


# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
client.version()

while True:
    try:
        client.remote_connect(tvHost, tvPort)
        device = client.device(f'{tvHost}:{tvPort}')
        #print(f'device {device}')
        device.shell(f'getevent -l {inputDevice}', handler=dump_getevent_by_line)
    except ConnectionRefusedError:
        print("Connection refused. Retrying in 10s")
        sleep(10)

"""
"EV_KEY       KEY_VOLUMEUP         DOWN"
"EV_KEY       KEY_VOLUMEUP         UP"
"EV_KEY       KEY_VOLUMEDOWN       DOWN"
"EV_KEY       KEY_VOLUMEDOWN       UP"
"EV_KEY       KEY_TV               DOWN"    #source
"EV_KEY       KEY_TV               UP"
"EV_KEY       KEY_COFFEE           DOWN"    #power
"EV_KEY       KEY_COFFEE           UP"
"EV_KEY       KEY_MUTE             DOWN"
"EV_KEY       KEY_MUTE             UP"
"""

