# Name: mqtt_integration.py
#
# Description: Push measurement results from the DSO to the MQTT broker
# for reception using a mobile app or WebSocket client. Additionally,
# it is possible to push commands from the mobile app or WebSocket client
# to the broker, which are then received and executed by the DSO.
# (WebSocket client website: https://www.hivemq.com/demos/websocket-client
# or https://mqttx.app/web)
#
# Author: MK Huang
#
# Documentation:
#   https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import sys
import time
from umqtt.simple import MQTTClient

# [MQTT] mqtt server
mqtt_servers = ['test.mosquitto.org', 'mqtt-dashboard.com', 'broker.emqx.io']

# [MQTT] topic
sub_topic = 'gwpub'
pub_topic = 'gwsub'

def MQTTConnect(client, server):
    while True:
        try:
            client.connect(False)
            print(f"Connected to MQTT broker({server}).")
            return True
        except OSError as e:
            print("Connect failed({server}).")
            return None
            
def read_msg(client, topic, msg):
    #print(topic.decode())
    method_to_call = getattr(dso, msg.decode().lower(), None)
    if callable(method_to_call):
        result = method_to_call()
        if result is not None:
            client.publish(bytes(pub_topic,'utf-8'), bytes(result,'utf-8'), qos=0)
            try:
                gui.draw_popup(result, 3)
            except:
                pass
    else:
        try:
            gui.draw_popup("Please adjust the content of your publication to 'autoset' or 'run', 'stop'.", 3)
        except:
            pass

if __name__ == '__main__':
    if not sys.implementation.name == "micropython":
       raise ValueError('This Demo can only be used on DSO')
    from dso_const import *
    import gds_info as gds
    
    dso = gds.Dso()
    dso.__shm_thread()
    dso.connect()
    mod = f'{dso.idn().split(',')[1]}'
    ser = f'{dso.idn().split(',')[2]}'
    print(ser)

    try:
        import dso_gui
        gui = dso_gui.DrawObject()
    except: 
        pass

    # [MQTT] Connect to broker
    clients = []
    for server in mqtt_servers:
        client = MQTTClient(client_id="test2423", keepalive = 0, server = server)
        if MQTTConnect(client, server) is None:
            client = None
        clients.append(client)

    # [MQTT] Subscribe
    sub_ser_topic = sub_topic + '/' + ser.lower() + '/#'
    for client in clients:
        if client is not None:
            client.set_callback(lambda topic, msg: read_msg(client, topic, msg))
            client.subscribe(bytes(sub_ser_topic,'utf-8'))
        
    last_message = time.time()
    message_interval = 8
    pub_ser_topic = pub_topic + '/' + ser.lower()
    while True:
        try:
            if (time.time() - last_message) > message_interval:
                # [GDS] meas
                topic_str = f"[{ser}]"
                meas1 =  f"Frequency: {str(dso.meas.get_frequency(kCH1))}"
                meas2 =  f"Pulse: {str(dso.meas.get_pos_pulse(kCH1))}"
                
                # [MQTT] Publish
                for client in clients:
                    if client is not None:
                        client.publish(bytes(pub_ser_topic,'utf-8'), bytes(topic_str + meas1,'utf-8'), qos=0)
                        client.publish(bytes(pub_ser_topic,'utf-8'), bytes(topic_str + meas2,'utf-8'), qos=0)
                last_message = time.time()
            
            # [MQTT] Read from broker
            for client in clients:
                if client is not None:
                    client.check_msg()
            time.sleep(1)
        except OSError as e:
            print("Connecting...")
            client.connect(False)
            print("Connected to MQTT broker.")

