from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import requests
import time

# ip_address = "169.254.231.239"
ip_address = "192.168.1.200"
port = 502
function_code = 3
start_address = 0x0000
length = 120
timeout = 4

api_url = "Hhttp://localhost/push/push.php"

slave_ids = list(range(1, 14))  # Updated to include 13 devices

flowmeter_ids_shaft1 = {1: "GFI0306", 2: "GFI0300", 3: "GFI0277", 4: "GFI0294", 5: "GFI0260", 6: "GFI0245", 7: "GFI0232", 8: "GFI0275", 9: "GFI0217", 10: "GFI0031", 11: "GFI0286", 12: "GFI0237", 13: "GFI0317", 14: "GFI0288"}
flowmeter_ids_shaft2 = {1: "GFI0318", 2: "GFI0298", 3: "GFI0257", 4: "GFI0297", 5: "GFI0292", 6: "GFI0242", 7: "GFI0248", 8: "GFI0276", 9: "GFI0356", 10: "GFI0032", 11: "GFI0246", 12: "GFI0355", 13: "GFI0314", 14: "GFI0278"}
flowmeter_ids_shaft3 = {1: "GFI0312", 2: "GFI0299", 3: "GFI0244", 4: "GFI0295", 5: "GFI0247", 6: "GFI0279", 7: "GFI0176", 8: "GFI0289", 9: "GFI0241", 10: "GFI0270", 11: "GFI0251", 12: "GFI0218", 13: "GFI0308", 14: "GFI0309"}
flowmeter_ids_shaft4 = {1: "GFI", 2: "GFI0301", 3: "GFI0255", 4: "GFI0293", 5: "GFI0230", 6: "GFI0273", 7: "GFI0235", 8: "GFI0240", 9: "GFI0222", 10: "GFI0263", 11: "GFI0215", 12: "GFI0285", 13: "GFI0316", 14: "GFI0037"}
flowmeter_ids_shaft5 = {1: "GFI", 2: "GFI0303", 3: "GFI0216", 4: "GFI0296", 5: "GFI0261", 6: "GFI0287", 7: "GFI0234", 8: "GFI0171", 9: "GFI0256", 10: "GFI0253", 11: "GFI0250", 12: "GFI0272", 13: "GFI0228", 14: "GFI0035"}
flowmeter_ids_shaft6 = {1: "GFI0065", 2: "GFI0066", 3: "GFI0067", 4: "GFI0068", 5: "GFI0069", 6: "GFI0070", 7: "GFI0071", 8: "GFI0072", 9: "GFI0073", 10: "GFI0074", 11: "GFI0075", 12: "GFI0076", 13: "GFI0077", 14: "GFI0078"}

flowmeter_ids_shaft7 = {1: "GFI0320", 2: "GFI0319", 3: "GFI0213", 4: "GFI0313", 5: "GFI0", 6: "GFI0269", 7: "GFI0285", 8: "GFI0266", 9: "GFI0211", 10: "GFI0227", 11: "GFI0291", 12: "GFI0280", 13: "GFI0214", 14: "GFI0284"}
flowmeter_ids_shaft8 = {1: "GFI0", 2: "GFI0209", 3: "GFI0304", 4: "GFI0231", 5: "GFI0221", 6: "GFI0267", 7: "GFI0252", 8: "GFI0265", 9: "GFI0224", 10: "GFI0249", 11: "GFI0", 12: "GFI0233", 13: "GFI0226", 14: "GFI0305"}
flowmeter_ids_shaft9 = {1: "GFI0208", 2: "GFI0229", 3: "GFI0310", 4: "GFI0223", 5: "GFI0220", 6: "GFI0283", 7: "GFI0254", 8: "GFI0282", 9: "GFI0236", 10: "GFI0206", 11: "GFI0", 12: "GFI0204", 13: "GFI0281", 14: "GFI0307"}
flowmeter_ids_shaft10 = {1: "GFI", 2: "GFI0079", 3: "GFI0080", 4: "GFI0081", 5: "GFI0082", 6: "GFI0083", 7: "GFI0084", 8: "GFI0085", 9: "GFI0087", 10: "GFI0089", 11: "GFI0090", 12: "GFI0091", 13: "GFI0092", 14: "GFI0093"}
flowmeter_ids_shaft11 = {1: "GFI", 2: "GFI0238", 3: "GFI0202", 4: "GFI0191", 5: "GFI0205", 6: "GFI0036", 7: "GFI0057", 8: "GFI0207", 9: "GFI0311", 10: "GFI0201", 11: "GFI0189", 12: "GFI0203", 13: "GFI0259", 14: "GFI0268"}
flowmeter_ids_shaft12 = {1: "GFI0094", 2: "GFI0095", 3: "GFI0096", 4: "GFI0097", 5: "GFI0098", 6: "GFI0099", 7: "GFI0101", 8: "GFI0102", 9: "GFI0103", 10: "GFI0104", 11: "GFI0105", 12: "GFI0106", 13: "GFI0107", 14: "GFI0108"}
flowmeter_ids_shaft13 = {1: "GFI0321", 2: "GFI0315", 3: "GFI0219", 4: "GFI0210", 5: "GFI0", 6: "GFI0225", 7: "GFI0174", 8: "GFI0243", 9: "GFI0212", 10: "GFI0262", 11: "GFI0290", 12: "GFI0", 13: "GFI0239", 14: "GFI0264"}

def process_data(slave_id, data, flowmeter_ids):
    for i in range(1, 15):
        index = (i - 1) * 8
        if data[index] == i and data[index + 1] != 255 and data[index + 2] != 255:
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
