from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import requests
import time

# Modbus TCP device parameters
ip_address = "169.254.231.239"
port = 502
function_code = 3  # Function code
start_address = 0x0000  # Start address
length = 100  # Length of address to read
timeout = 2  # Timeout in seconds

# List of slave IDs
slave_ids = list(range(1, 8))  # Slave IDs from 1 to 7

# Dictionary mapping slave IDs to flowmeter IDs
flowmeter_ids = {
    1: "GFA0001",
    2: "GFA0002",
    3: "GFA0003",
    4: "GFA0004",
    5: "GFA0005",
    6: "GFA0006",
    7: "GFA0007"
}

# Local API endpoint
api_url = "http://192.9.101.52/incor/push.php"

while True:
    for slave_id in slave_ids:
        # Connect to Modbus TCP device with specified timeout
        client = ModbusTcpClient(ip_address, port, timeout=timeout)

        try:
            # Connect to Modbus TCP device
            if not client.connect():
                print("Failed to connect to Modbus TCP device")
            else:
                # Read holding registers
                response = client.read_holding_registers(start_address, length, unit=slave_id)

                if response.isError():
                    print(f"Modbus Error from slave {slave_id}: {response}")
                    # Set combined values to -1 in case of Modbus error
                    Totalizer = -1
                    Flowrate = -1
                    payload = {
                        "project_id": "incor",
                        "data": f"flowmeter_id:{flowmeter_ids.get(slave_id, 'Unknown')},flowrate:{Flowrate},totalizer:{Totalizer},ver:1.00"
                    }
                    print(payload)	
                    # Send data to the local API
                    update_API = requests.get(api_url, params=payload)
                    print(update_API)
                    # Check if the request was successful
                    if update_API.status_code == 200:
                        print(f"Data sent to API for slave {slave_id}")
                    else:
                        print(f"Failed to send data to API for slave {slave_id}. Status code: {response.status_code}")
                else:
                    # Decode the response data
                    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Big)
                    data = [decoder.decode_8bit_uint() for _ in range(length)]

                    # Perform bitwise operation on registers 2 and 3
                    if len(data) >= 4:  # Assuming registers 2 and 3 are available
                        register_0 = data[0]
                        register_1 = data[1]
                        register_2 = data[2]
                        register_3 = data[3]
                        combined_value = (register_0 << 24) | (register_1 << 16) | (register_2 << 8) | register_3

                        register_6 = data[4]
                        register_7 = data[5]
                        combined_value_2 = (register_6 << 8) | register_7

                    # Print data in hexadecimal format
                    print(f"Data from slave {slave_id} in HEX:", end=" ")
                    for value in data:
                        print(hex(value), end=" ")
                    print()  # Print a newline after printing all values
                    print()

                    # Prepare data for API request
                    payload = {
                        "project_id": "incor",
                        "data": f"flowmeter_id:{flowmeter_ids.get(slave_id, 'Unknown')},flowrate:{Flowrate},totalizer:{Totalizer},ver:1.00"
                    }

                    # Send data to the local API
                    update_API = requests.get(api_url, params=payload)

                    # Check if the request was successful
                    if update_API.status_code == 200:
                        print(f"Data sent to API for slave {slave_id}")
                    else:
                        print(f"Failed to send data to API for slave {slave_id}. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection
            client.close()
    #time.sleep(3)
