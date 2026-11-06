from pyModbusTCP.client import ModbusClient

# Define the Modbus TCP server parameters
SERVER_HOST = '169.254.231.239'
SERVER_PORT = 502  # Default Modbus TCP port

# Define the slave ID (address)
SLAVE_ID = 1

# Define the starting address and number of registers to read
STARTING_ADDRESS = 0  # Address of the first register to read
NUM_REGISTERS = 10  # Number of registers to read

try:
    # Connect to the Modbus TCP server
    client = ModbusClient(host=SERVER_HOST, port=SERVER_PORT)
    client.open()

    if client.is_open:
        # Read holding registers (function code 3)
        regs = client.read_holding_registers(STARTING_ADDRESS, NUM_REGISTERS)
        
        # Check if the response is valid
        if regs:
            # Print the values read from the registers in hexadecimal format
            print("Data read from flowmeter (in hexadecimal):")
            for i, reg in enumerate(regs):
                # Convert each register value to hexadecimal format
                data_hex = hex(reg)
                print(f"Register {STARTING_ADDRESS + i}: {data_hex}")
        else:
            print("Failed to read data from the flowmeter.")

    else:
        print("Failed to connect to the Modbus TCP server.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    if client.is_open:
        client.close()
