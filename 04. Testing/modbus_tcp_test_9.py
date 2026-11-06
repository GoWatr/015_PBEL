from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import time

ip_address = "169.254.231.239"
port = 502
function_code = 3  # Function code
start_address = 0x0000  # Start address
length = 120  # Length of address to read
timeout = 4  # Timeout in seconds

slave_ids = list(range(1, 7))

flowmeter_ids_shaft1 = {
    1: "GFA0001", 2: "GFA0002", 3: "GFA0003", 4: "GFA0004", 5: "GFA0005", 6: "GFA0006", 7: "GFA0007", 8: "GFA0008", 9: "GFA0009", 10: "GFA0010", 11: "GFA0011", 12: "GFA0012", 13: "GFA0013", 14: "GFA0014"
}

flowmeter_ids_shaft2 = {
    1: "GFA0015", 2: "GFA0016", 3: "GFA0017", 4: "GFA0018", 5: "GFA0019", 6: "GFA0020", 7: "GFA0021", 8: "GFA0022", 9: "GFA0023", 10: "GFA0024", 11: "GFA0025", 12: "GFA0026", 13: "GFA0027", 14: "GFA0028"
}

flowmeter_ids_shaft3 = {
    1: "GFA0029", 2: "GFA0030", 3: "GFA0031", 4: "GFA0032", 5: "GFA0033", 6: "GFA0034", 7: "GFA0035", 8: "GFA0036", 9: "GFA0037", 10: "GFA0038", 11: "GFA0039", 12: "GFA0040", 13: "GFA0041", 14: "GFA0042"
}

flowmeter_ids_shaft4 = {
    1: "GFA0043", 2: "GFA0044", 3: "GFA0045", 4: "GFA0046", 5: "GFA0047", 6: "GFA0048", 7: "GFA0049", 8: "GFA0050", 9: "GFA0051", 10: "GFA0052", 11: "GFA0053", 12: "GFA0054", 13: "GFA0055", 14: "GFA0056"
}

flowmeter_ids_shaft5 = {
    1: "GFA0057", 2: "GFA0058", 3: "GFA0059", 4: "GFA0060", 5: "GFA0061", 6: "GFA0062", 7: "GFA0063", 8: "GFA0064", 9: "GFA0065", 10: "GFA0066", 11: "GFA0067", 12: "GFA0068", 13: "GFA0069", 14: "GFA0070"
}

flowmeter_ids_shaft6 = {
    1: "GFA0071", 2: "GFA0072", 3: "GFA0073", 4: "GFA0074", 5: "GFA0075", 6: "GFA0076", 7: "GFA0077", 8: "GFA0078", 9: "GFA0079", 10: "GFA0080", 11: "GFA0081", 12: "GFA0082", 13: "GFA0083", 14: "GFA0084"
}

def process_data(slave_id, data, flowmeter_ids):
    for i in range(1, 15):
        index = (i - 1) * 8
        if data[index] == i:
            print(f"Flowmeter_ID: {flowmeter_ids[i]}")
            totalizer = (data[index + 1] << 24) | (data[index + 2] << 16) | (data[index + 3] << 8) | data[index + 4]
            flowrate = (data[index + 5] << 16) | (data[index + 6] << 8) | data[index + 7]
            print(f"totalizer in DEC : {totalizer} Flowrate in DEC : {flowrate}")
            print(f"totalizer in HEX : {hex(totalizer)} Flowrate in HEX : {hex(flowrate)}")

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

                    if slave_id == 1:
                        process_data(slave_id, data, flowmeter_ids_shaft1)
                    elif slave_id == 2:
                        process_data(slave_id, data, flowmeter_ids_shaft2)
                    elif slave_id == 3:
                        process_data(slave_id, data, flowmeter_ids_shaft3)
                    elif slave_id == 4:
                        process_data(slave_id, data, flowmeter_ids_shaft4)
                    elif slave_id == 5:
                        process_data(slave_id, data, flowmeter_ids_shaft5)
                    elif slave_id == 6:
                        process_data(slave_id, data, flowmeter_ids_shaft6)

        except Exception as e:
            print(f"Exception occurred: {e}")

        finally:
            client.close()
