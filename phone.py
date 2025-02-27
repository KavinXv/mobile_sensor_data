import socket
import android
import time

droid = android.Android()

class SensorGpsClient:
    def __init__(self, server_ip, server_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))

    def send_data(self, data):
        data = str(data)
        self.client_socket.send(data.encode())

    def close_connection(self):
        self.client_socket.close()

sensor_gps_client = SensorGpsClient('172.20.10.11', 5050)

def event_loop():
    while True:
        time.sleep(0.1)
        droid.eventClearBuffer()
        e = droid.eventPoll(1)
        if e.result is not None:
            return True
    return False

def start_sensors_and_gps():
    
    droid.startSensingTimed(2, 1000)  # Start accelerometer sensor
    droid.startSensingTimed(3, 1000)  # 3Ã¤Â»Â£Ã¨Â¡Â¨Ã§Â£ÂÃ¥ÂÂÃ¨Â®Â¡
    droid.startSensingTimed(4, 1000)  # 4Ã¤Â»Â£Ã¨Â¡Â¨Ã¥ÂÂÃ§ÂºÂ¿Ã¤Â¼Â Ã¦ÂÂÃ¥ÂÂ¨
    droid.startLocating()  # Start GPS

    try:
        while True:
            acc_data = droid.sensorsReadAccelerometer().result
            if acc_data:
                data = acc_data
                sensor_gps_client.send_data(data)
                print(f"Sent acc : {data}") 


            sensor_data = droid.readSensors().result
           
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        droid.stopSensing()  # Stop sensor
        droid.stopLocating()  # Stop GPS
        sensor_gps_client.close_connection()  # Close connection

start_sensors_and_gps()