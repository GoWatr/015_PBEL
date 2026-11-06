from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import requests
import time

ip_address = "169.254.231.239"
# ip_address = "192.168.1.200"//panama
port = 502
function_code = 3
start_address = 0x0000
length = 120
timeout = 4

api_url = "http://localhost/push/push.php"

slave_ids = list(range(1, 14))  # Updated to include 13 devices

flowmeter_ids_shaft1 = {1: "GFI0110", 2: "GFI0166", 3: "GFI0173", 4: "GFI0144", 5: "GFI0100", 6: "GFI0188", 7: "GFI0141", 8: "GFI0172", 9: "GFI0183", 10: "GFI0153", 11: "GFI0341", 12: "GFI0182", 13: "GFI0115", 14: "GFI0120"}
flowmeter_ids_shaft2 = {1: "GFI0052", 2: "GFI0168", 3: "GFI0195", 4: "GFI0152", 5: "GFI0130", 6: "GFI0187", 7: "GFI0154", 8: "GFI0198", 9: "GFI0190", 10: "GFI0159", 11: "GFI0342", 12: "GFI0196", 13: "GFI0119", 14: "GFI0134"}
flowmeter_ids_shaft3 = {1: "GFI0111", 2: "GFI0135", 3: "GFI0123", 4: "GFI0149", 5: "GFI0147", 6: "GFI0125", 7: "GFI0151", 8: "GFI0137", 9: "GFI0142", 10: "GFI0129", 11: "GFI0335", 12: "GFI0326", 13: "GFI0113", 14: "GFI0131"}
flowmeter_ids_shaft4 = {1: "GFI", 2: "GFI0157", 3: "GFI0121", 4: "GFI0143", 5: "GFI0146", 6: "GFI0126", 7: "GFI0156", 8: "GFI0136", 9: "GFI0140", 10: "GFI0128", 11: "GFI0336", 12: "GFI0327", 13: "GFI0053", 14: "GFI0133"}
flowmeter_ids_shaft5 = {1: "GFI", 2: "GFI0138", 3: "GFI0122", 4: "GFI0150", 5: "GFI0353", 6: "GFI0127", 7: "GFI0158", 8: "GFI0139", 9: "GFI0148", 10: "GFI0124", 11: "GFI0334", 12: "GFI0328", 13: "GFI0351", 14: "GFI0132"}
flowmeter_ids_shaft6 = {1: "GFI0015", 2: "GFI0016", 3: "GFI0017", 4: "GFI0018", 5: "GFI0019", 6: "GFI0020", 7: "GFI0021", 8: "GFI0022", 9: "GFI0023", 10: "GFI0024", 11: "GFI0025", 12: "GFI0026", 13: "GFI0027", 14: "GFI0028"}

flowmeter_ids_shaft7 = {1: "GFI0177", 2: "GFI0350", 3: "GFI0338", 4: "GFI0333", 5: "GFI0180", 6: "GFI0330", 7: "GFI0186", 8: "GFI0178", 9: "GFI0174", 10: "GFI0200", 11: "GFI0030", 12: "GFI0352", 13: "GFI0192", 14: "GFI0051"}
flowmeter_ids_shaft8 = {1: "GFI0088", 2: "GFI0163", 3: "GFI0339", 4: "GFI0332", 5: "GFI0162", 6: "GFI0348", 7: "GFI0114", 8: "GFI0199", 9: "GFI0167", 10: "GFI0117", 11: "GFI0181", 12: "GFI0 ", 13: "GFI0323", 14: "GFI0194"}
flowmeter_ids_shaft9 = {1: "GFI0086", 2: "GFI0160", 3: "GFI0340", 4: "GFI0331", 5: "GFI0145", 6: "GFI0349", 7: "GFI0109", 8: "GFI0116", 9: "GFI0161", 10: "GFI0112", 11: "GFI0184", 12: "GFI0 ", 13: "GFI0322", 14: "GFI0193"}
flowmeter_ids_shaft10 = {1: "GFI", 2: "GFI0062", 3: "GFI0197", 4: "GFI0325", 5: "GFI0324", 6: "GFI0175", 7: "GFI0185", 8: "GFI0155", 9: "GFI0165", 10: "GFI0169", 11: "GFI0170", 12: "GFI0337", 13: "GFI0164", 14: "GFI0171"}
flowmeter_ids_shaft11 = {1: "GFI", 2: "GFI0038", 3: "GFI0039", 4: "GFI0040", 5: "GFI0041", 6: "GFI0042", 7: "GFI0043", 8: "GFI0044", 9: "GFI0045", 10: "GFI0046", 11: "GFI0047", 12: "GFI0048", 13: "GFI0049", 14: "GFI0050"}
flowmeter_ids_shaft12 = {1: "GFI0001", 2: "GFI0002", 3: "GFI0003", 4: "GFI0004", 5: "GFI0005", 6: "GFI0006", 7: "GFI0007", 8: "GFI0008", 9: "GFI0009", 10: "GFI0010", 11: "GFI0011", 12: "GFI0012", 13: "GFI0013", 14: "GFI0014"}
flowmeter_ids_shaft13 = {1: "GFI0054", 2: "GFI0345", 3: "GFI0346", 4: "GFI0347", 5: "GFI0055", 6: "GFI0056", 7: "GFI0060", 8: "GFI0058", 9: "GFI0059", 10: "GFI0179", 11: "GFI0061", 12: "GFI0329", 13: "GFI0063", 14: "GFI0064"}

def process_data(slave_id, data, flowmeter_ids):
    for i in range(1, 15):
        index = (i - 1) * 8
        if data[index] == i:
            print(f"Flowmeter_ID: {flowmeter_ids[i]}")
            totalizer = (data[index + 1] << 24) | (data[index + 2] << 16) | (data[index + 3] << 8) | data[index + 4]
            flowrate = (data[index + 5] << 16) | (data[index + 6] << 8) | data[index + 7]
            print(f"totalizer in DEC : {totalizer} Flowrate in DEC : {flowrate}")
            print(f"totalizer in HEX : {hex(totalizer)} Flowrate in HEX : {hex(flowrate)}")
            
            payload = {
                "project_id": "incor",
                "data": f"flowmeter_id:{flowmeter_ids[i]},flowrate:{flowrate},totalizer:{totalizer},ver:1.00"
            }
        
            time.sleep(1)
            try:
                if data[index] == i:
                    update_API = requests.get(api_url, params=payload)

                    if update_API.status_code == 200:
                        print(f"Data sent to API for slave {slave_id}")
                    else:
                        print(f"Failed to send data to API for slave {slave_id}. Status code: {update_API.status_code}")
            except Exception as e:
                print(f"Failed to send data to API for slave {slave_id}. Exception: {e}")

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
                    elif slave_id == 7:
                        process_data(slave_id, data, flowmeter_ids_shaft7)
                    elif slave_id == 8:
                        process_data(slave_id, data, flowmeter_ids_shaft8)
                    elif slave_id == 9:
                        process_data(slave_id, data, flowmeter_ids_shaft9)
                    elif slave_id == 10:
                        process_data(slave_id, data, flowmeter_ids_shaft10)
                    elif slave_id == 11:
                        process_data(slave_id, data, flowmeter_ids_shaft11)
                    elif slave_id == 12:
                        process_data(slave_id, data, flowmeter_ids_shaft12)
                    elif slave_id == 13:
                        process_data(slave_id, data, flowmeter_ids_shaft13)

        except Exception as e:
            print(f"Exception occurred: {e}")

        finally:
            client.close()
