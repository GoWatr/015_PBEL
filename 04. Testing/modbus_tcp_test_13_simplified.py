from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import requests
import requests.exceptions
import time
import threading

ip_address = "169.254.231.239"
port = 502
function_code = 3  # Function code
start_address = 0x0000  # Start address
length = 120  # Length of address to read
timeout = 4  # Timeout in seconds

# Local API endpoint
api_url = "http://192.9.101.52/incor/push.php"

slave_ids = list(range(1, 7))

# Generate flowmeter IDs for each shaft
flowmeter_ids = {}

for shaft_number in range(1, 7):
    start_index = (shaft_number - 1) * 14 + 1
    flowmeter_ids[f'shaft{shaft_number}'] = {i: f'GFA{str(start_index + i - 1).zfill(4)}' for i in range(1, 15)}

def process_data(slave_id, data, shaft_number):
    for i in range(1, 15):
        index = (i - 1) * 8
        if data[index] == i:
            flowmeter_id = flowmeter_ids[f'shaft{shaft_number}'][i]
            print(f"Flowmeter_ID: {flowmeter_id}")
            totalizer = (data[index + 1] << 24) | (data[index + 2] << 16) | (data[index + 3] << 8) | data[index + 4]
            flowrate = (data[index + 5] << 16) | (data[index + 6] << 8) | data[index + 7]
            print(f"totalizer in DEC : {totalizer} Flowrate in DEC : {flowrate}")
            print(f"totalizer in HEX : {hex(totalizer)} Flowrate in HEX : {hex(flowrate)}")
            
            payload = {
                "project_id": "incor",
                "data": f"flowmeter_id:{flowmeter_id},flowrate:{flowrate},totalizer:{totalizer},ver:1.00"
            }
            
            try:
                update_API = requests.get(api_url, params=payload, timeout=5)
                update_API.raise_for_status()
                print(f"Data sent to API for slave {slave_id}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send data to API for slave {slave_id}: {e}")

def watchdog_timer():
    while True:
        time.sleep(60)  # Adjust the interval as needed
        # Check if the main thread is still alive
        if not main_thread.is_alive():
            print("Main thread stopped. Restarting...")
            main_thread.start()

def main():
    global main_thread
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()

def main_loop():
    while True:
        for slave_id in slave_ids:
            client = ModbusTcpClient(ip_address, port, timeout=timeout)
            try:
                if not client.connect():
                    print("Failed to connect to Modbus TCP device")
                else:
                    time.sleep(1)
                    response = client.read_holding_registers(start_address, length, unit=slave_id)
                    if response.isError():
                        print(f"Modbus Error from slave {slave_id}: {response}")
                    else:
                        decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Big)
                        data = [decoder.decode_8bit_uint() for _ in range(length)]
                        print()
                        print(f"Read data from slave {slave_id}:", data)
                        print(f"Read data from slave {slave_id}:", [hex(value) for value in data])

                        shaft_number = (slave_id - 1) % 6 + 1
                        process_data(slave_id, data, shaft_number)

            except requests.exceptions.RequestException as e:
                print(f"Failed to send data to API for slave {slave_id}: {e}")
            except Exception as e:
                print(f"Exception occurred: {e}")

            finally:
                client.close()

if __name__ == "__main__":
    main_thread = None
    main()
    watchdog_thread = threading.Thread(target=watchdog_timer)
    watchdog_thread.start()
