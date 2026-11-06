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

                    if len(data) >= 4:
                        if slave_id == 1:
                            if data[2] == 1:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[1]}")
                                F1_T = (data[1] << 24) | (data[2] << 16) | (data[3] << 8) | data[4]
                                F1_F = (data[5] << 16) | (data[6] << 8) | data[7] 
                                print(f"totalizer in DEC : {F1_T} Flowrate in DEC : {F1_F}")
                                F1_T = (hex(F1_T))
                                F1_F = (hex(F1_F))
                                print(f"totalizer in HEX : {F1_T} Flowrate in HEX : {F1_F}")
                        
                            if data[8] == 2:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[2]}")
                                F2_T = (data[9] << 24) | (data[10] << 16) | (data[11] << 8) | data[12]
                                F2_F = (data[13] << 8) | (data[14] << 8) | data[15]
                                print(f"totalizer in DEC : {F2_T} Flowrate in DEC : {F2_F}")
                                F2_T = (hex(F2_T))
                                F2_F = (hex(F2_F))
                                print(f"totalizer in HEX : {F2_T} Flowrate in HEX : {F2_F}")
                        
                            if data[16] == 3:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[3]}")
                                F3_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F3_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F3_T} Flowrate in DEC : {F3_F}")
                                F3_T = (hex(F3_T))
                                F3_F = (hex(F3_F))
                                print(f"totalizer in HEX : {F3_T} Flowrate in HEX : {F3_F}")
                            
                            if data[24] == 4:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[4]}")
                                F4_T = (data[25] << 24) | (data[26] << 16) | (data[27] << 8) | data[28]
                                F4_F = (data[29] << 8) | (data[30] << 8) | data[31]
                                print(f"totalizer in DEC : {F4_T} Flowrate in DEC : {F4_F}")
                                F4_T = (hex(F4_T))
                                F4_F = (hex(F4_F))
                                print(f"totalizer in HEX : {F4_T} Flowrate in HEX : {F4_F}")
                                
                            if data[32] == 5:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[5]}")
                                F5_T = (data[1] << 24) | (data[2] << 16) | (data[3] << 8) | data[4]
                                F5_F = (data[5] << 16) | (data[6] << 8) | data[7] 
                                print(f"totalizer in DEC : {F5_T} Flowrate in DEC : {F5_F}")
                                F5_T = (hex(F5_T))
                                F5_F = (hex(F5_F))
                                print(f"totalizer in HEX : {F5_T} Flowrate in HEX : {F5_F}")
                        
                            if data[40] == 6:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[6]}")
                                F6_T = (data[9] << 24) | (data[10] << 16) | (data[11] << 8) | data[12]
                                F6_F = (data[13] << 8) | (data[14] << 8) | data[15]
                                print(f"totalizer in DEC : {F6_T} Flowrate in DEC : {F6_F}")
                                F6_T = (hex(F6_T))
                                F6_F = (hex(F6_F))
                                print(f"totalizer in HEX : {F6_T} Flowrate in HEX : {F6_F}")
                        
                            if data[48] == 7:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[7]}")
                                F7_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F7_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F7_T} Flowrate in DEC : {F7_F}")
                                F7_T = (hex(F7_T))
                                F7_F = (hex(F7_F))
                                print(f"totalizer in HEX : {F7_T} Flowrate in HEX : {F7_F}")
                            
                            if data[56] == 8:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[8]}")
                                F8_T = (data[25] << 24) | (data[26] << 16) | (data[27] << 8) | data[28]
                                F8_F = (data[29] << 8) | (data[30] << 8) | data[31]
                                print(f"totalizer in DEC : {F8_T} Flowrate in DEC : {F8_F}")
                                F8_T = (hex(F8_T))
                                F8_F = (hex(F8_F))
                                print(f"totalizer in HEX : {F8_T} Flowrate in HEX : {F8_F}")
                                
                            if data[64] == 9:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[9]}")
                                F9_T = (data[1] << 24) | (data[2] << 16) | (data[3] << 8) | data[4]
                                F9_F = (data[5] << 16) | (data[6] << 8) | data[7] 
                                print(f"totalizer in DEC : {F9_T} Flowrate in DEC : {F9_F}")
                                F9_T = (hex(F9_T))
                                F9_F = (hex(F9_F))
                                print(f"totalizer in HEX : {F9_T} Flowrate in HEX : {F9_F}")
                        
                            if data[72] == 10:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[10]}")
                                F10_T = (data[9] << 24) | (data[10] << 16) | (data[11] << 8) | data[12]
                                F10_F = (data[13] << 8) | (data[14] << 8) | data[15]
                                print(f"totalizer in DEC : {F10_T} Flowrate in DEC : {F10_F}")
                                F10_T = (hex(F10_T))
                                F10_F = (hex(F10_F))
                                print(f"totalizer in HEX : {F10_T} Flowrate in HEX : {F10_F}")
                        
                            if data[80] == 11:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[11]}")
                                F11_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F11_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F11_T} Flowrate in DEC : {F11_F}")
                                F11_T = (hex(F11_T))
                                F11_F = (hex(F11_F))
                                print(f"totalizer in HEX : {F11_T} Flowrate in HEX : {F11_F}")
                            
                            if data[88] == 12:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[12]}")
                                F12_T = (data[25] << 24) | (data[26] << 16) | (data[27] << 8) | data[28]
                                F12_F = (data[29] << 8) | (data[30] << 8) | data[31]
                                print(f"totalizer in DEC : {F12_T} Flowrate in DEC : {F12_F}")
                                F12_T = (hex(F12_T))
                                F12_F = (hex(F12_F))
                                print(f"totalizer in HEX : {F12_T} Flowrate in HEX : {F12_F}")
                            if data[96] == 13:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[3]}")
                                F13_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F13_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F13_T} Flowrate in DEC : {F13_F}")
                                F13_T = (hex(F13_T))
                                F13_F = (hex(F13_F))
                                print(f"totalizer in HEX : {F13_T} Flowrate in HEX : {F13_F}")
                            
                            if data[104] == 14:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[14]}")
                                F14_T = (data[25] << 24) | (data[26] << 16) | (data[27] << 8) | data[28]
                                F14_F = (data[29] << 8) | (data[30] << 8) | data[31]
                                print(f"totalizer in DEC : {F14_T} Flowrate in DEC : {F14_F}")
                                F14_T = (hex(F14_T))
                                F14_F = (hex(F14_F))
                                print(f"totalizer in HEX : {F14_T} Flowrate in HEX : {F14_F}")
#################################################################################################################################################  
                        elif slave_id == 2:
                            if data[0] == 1:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft2[1]}")
                                F15_T = (data[1] << 24) | (data[2] << 16) | (data[3] << 8) | data[4]
                                F15_F = (data[5] << 16) | (data[6] << 8) | data[7] 
                                print(f"totalizer in DEC : {F15_T} Flowrate in DEC : {F15_F}")
                                F15_T = (hex(F15_T))
                                F15_F = (hex(F15_F))
                                print(f"totalizer in HEX : {F15_T} Flowrate in HEX : {F15_F}")
                        
                            if data[8] == 2:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft2[2]}")
                                F16_T = (data[9] << 24) | (data[10] << 16) | (data[11] << 8) | data[12]
                                F16_F = (data[13] << 8) | (data[14] << 8) | data[15]
                                print(f"totalizer in DEC : {F16_T} Flowrate in DEC : {F16_F}")
                                F16_T = (hex(F16_T))
                                F16_F = (hex(F16_F))
                                print(f"totalizer in HEX : {F16_T} Flowrate in HEX : {F16_F}")
                        
                            if data[16] == 3:
                                print(f"Flowmeter_ID: {flowmeter_ids_saft2[3]}")
                                F17_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F17_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F17_T} Flowrate in DEC : {F17_F}")
                                F17_T = (hex(F17_T))
                                F17_F = (hex(F17_F))
                                print(f"totalizer in HEX : {F17_T} Flowrate in HEX : {F17_F}")
                            
                            if data[24] == 4:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft2[4]}")
                                F18_T = (data[25] << 24) | (data[26] << 16) | (data[27] << 8) | data[28]
                                F18_F = (data[29] << 8) | (data[30] << 8) | data[31]
                                print(f"totalizer in DEC : {F18_T} Flowrate in DEC : {F18_F}")
                                F18_T = (hex(F18_T))
                                F18_F = (hex(F18_F))
                                print(f"totalizer in HEX : {F18_T} Flowrate in HEX : {F18_F}")
                                
                            if data[32] == 5:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[5]}")
                                F19_T = (data[1] << 24) | (data[2] << 16) | (data[3] << 8) | data[4]
                                F5_F = (data[5] << 16) | (data[6] << 8) | data[7] 
                                print(f"totalizer in DEC : {F19_T} Flowrate in DEC : {F19_F}")
                                F19_T = (hex(F19_T))
                                F19_F = (hex(F19_F))
                                print(f"totalizer in HEX : {F19_T} Flowrate in HEX : {F19_F}")
                        
                            if data[40] == 6:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[6]}")
                                F20_T = (data[9] << 24) | (data[10] << 16) | (data[11] << 8) | data[12]
                                F20_F = (data[13] << 8) | (data[14] << 8) | data[15]
                                print(f"totalizer in DEC : {F20_T} Flowrate in DEC : {F20_F}")
                                F20_T = (hex(F20_T))
                                F20_F = (hex(F20_F))
                                print(f"totalizer in HEX : {F20_T} Flowrate in HEX : {F20_F}")
                        
                            if data[48] == 7:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[7]}")
                                F21_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F21_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F21_T} Flowrate in DEC : {F21_F}")
                                F21_T = (hex(F21_T))
                                F21_F = (hex(F21_F))
                                print(f"totalizer in HEX : {F21_T} Flowrate in HEX : {F21_F}")
                            
                            if data[56] == 8:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[8]}")
                                F22_T = (data[25] << 24) | (data[26] << 16) | (data[27] << 8) | data[28]
                                F22_F = (data[29] << 8) | (data[30] << 8) | data[31]
                                print(f"totalizer in DEC : {F22_T} Flowrate in DEC : {F22_F}")
                                F22_T = (hex(F22_T))
                                F22_F = (hex(F22_F))
                                print(f"totalizer in HEX : {F22_T} Flowrate in HEX : {F22_F}")
                                
                            if data[64] == 9:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[9]}")
                                F23_T = (data[1] << 24) | (data[2] << 16) | (data[3] << 8) | data[4]
                                F23_F = (data[5] << 16) | (data[6] << 8) | data[7] 
                                print(f"totalizer in DEC : {F23_T} Flowrate in DEC : {F23_F}")
                                F23_T = (hex(F23_T))
                                F23_F = (hex(F23_F))
                                print(f"totalizer in HEX : {F23_T} Flowrate in HEX : {F23_F}")
                        
                            if data[72] == 10:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[10]}")
                                F24_T = (data[9] << 24) | (data[10] << 16) | (data[11] << 8) | data[12]
                                F24_F = (data[13] << 8) | (data[14] << 8) | data[15]
                                print(f"totalizer in DEC : {F24_T} Flowrate in DEC : {F24_F}")
                                F24_T = (hex(F24_T))
                                F24_F = (hex(F24_F))
                                print(f"totalizer in HEX : {F24_T} Flowrate in HEX : {F24_F}")
                        
                            if data[80] == 11:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[11]}")
                                F25_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F25_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F25_T} Flowrate in DEC : {F25_F}")
                                F25_T = (hex(F25_T))
                                F25_F = (hex(F25_F))
                                print(f"totalizer in HEX : {F25_T} Flowrate in HEX : {F25_F}")
                            
                            if data[88] == 12:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[12]}")
                                F26_T = (data[25] << 24) | (data[26] << 16) | (data[27] << 8) | data[28]
                                F26_F = (data[29] << 8) | (data[30] << 8) | data[31]
                                print(f"totalizer in DEC : {F26_T} Flowrate in DEC : {F26_F}")
                                F26_T = (hex(F26_T))
                                F26_F = (hex(F26_F))
                                print(f"totalizer in HEX : {F26_T} Flowrate in HEX : {F26_F}")
                            if data[96] == 13:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[13]}")
                                F27_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F27_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F27_T} Flowrate in DEC : {F27_F}")
                                F27_T = (hex(F27_T))
                                F27_F = (hex(F27_F))
                                print(f"totalizer in HEX : {F27_T} Flowrate in HEX : {F27_F}")
                            
                            if data[104] == 14:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft1[14]}")
                                F28_T = (data[25] << 24) | (data[26] << 16) | (data[27] << 8) | data[28]
                                F28_F = (data[29] << 8) | (data[30] << 8) | data[31]
                                print(f"totalizer in DEC : {F28_T} Flowrate in DEC : {F28_F}")
                                F28_T = (hex(F28_T))
                                F28_F = (hex(F28_F))
                                print(f"totalizer in HEX : {F28_T} Flowrate in HEX : {F28_F}")
#################################################################################################################################################
                        elif slave_id == 3:
                            if data[0] == 1:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[1]}")
                                F29_T = (data[1] << 24) | (data[2] << 16) | (data[3] << 8) | data[4]
                                F29_F = (data[5] << 16) | (data[6] << 8) | data[7] 
                                print(f"totalizer in DEC : {F29_T} Flowrate in DEC : {F29_F}")
                                F29_T = (hex(F29_T))
                                F29_F = (hex(F29_F))
                                print(f"totalizer in HEX : {F29_T} Flowrate in HEX : {F29_F}")

                            if data[8] == 2:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[2]}")
                                F30_T = (data[9] << 24) | (data[10] << 16) | (data[11] << 8) | data[12]
                                F30_F = (data[13] << 8) | (data[14] << 8) | data[15]
                                print(f"totalizer in DEC : {F30_T} Flowrate in DEC : {F30_F}")
                                F30_T = (hex(F30_T))
                                F30_F = (hex(F30_F))
                                print(f"totalizer in HEX : {F30_T} Flowrate in HEX : {F30_F}")

                            if data[16] == 3:
                                print(f"Flowmeter_ID: {flowmeter_ids_saft3[3]}")
                                F31_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F31_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F31_T} Flowrate in DEC : {F31_F}")
                                F31_T = (hex(F31_T))
                                F31_F = (hex(F31_F))
                                print(f"totalizer in HEX : {F31_T} Flowrate in HEX : {F31_F}")
                                
                            if data[24] == 4:
                                print(f"Flowmeter_ID: {flowmeter_ids_saft3[4]}")
                                F32_T = (data[17] << 24) | (data[18] << 16) | (data[19] << 8) | data[20]
                                F32_F = (data[21] << 8) | (data[22] << 8) | data[23]
                                print(f"totalizer in DEC : {F32_T} Flowrate in DEC : {F32_F}")
                                F32_T = (hex(F32_T))
                                F32_F = (hex(F32_F))
                                print(f"totalizer in HEX : {F32_T} Flowrate in HEX : {F32_F}")

                            if data[32] == 5:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[5]}")
                                F33_T = (data[33] << 24) | (data[34] << 16) | (data[35] << 8) | data[36]
                                F33_F = (data[37] << 16) | (data[38] << 8) | data[39]
                                print(f"totalizer in DEC : {F33_T} Flowrate in DEC : {F33_F}")
                                F33_T = (hex(F33_T))
                                F33_F = (hex(F33_F))
                                print(f"totalizer in HEX : {F33_T} Flowrate in HEX : {F33_F}")

                            if data[40] == 6:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[6]}")
                                F34_T = (data[41] << 24) | (data[42] << 16) | (data[43] << 8) | data[44]
                                F34_F = (data[45] << 8) | (data[46] << 8) | data[47]
                                print(f"totalizer in DEC : {F34_T} Flowrate in DEC : {F34_F}")
                                F34_T = (hex(F34_T))
                                F34_F = (hex(F34_F))
                                print(f"totalizer in HEX : {F34_T} Flowrate in HEX : {F34_F}")

                            if data[48] == 7:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[7]}")
                                F35_T = (data[49] << 24) | (data[50] << 16) | (data[51] << 8) | data[52]
                                F35_F = (data[53] << 8) | (data[54] << 8) | data[55]
                                print(f"totalizer in DEC : {F35_T} Flowrate in DEC : {F35_F}")
                                F35_T = (hex(F35_T))
                                F35_F = (hex(F35_F))
                                print(f"totalizer in HEX : {F35_T} Flowrate in HEX : {F35_F}")

                            if data[56] == 8:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[8]}")
                                F36_T = (data[57] << 24) | (data[58] << 16) | (data[59] << 8) | data[60]
                                F36_F = (data[61] << 8) | (data[62] << 8) | data[63]
                                print(f"totalizer in DEC : {F36_T} Flowrate in DEC : {F36_F}")
                                F36_T = (hex(F36_T))
                                F36_F = (hex(F36_F))
                                print(f"totalizer in HEX : {F36_T} Flowrate in HEX : {F36_F}")

                            if data[64] == 9:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[9]}")
                                F37_T = (data[65] << 24) | (data[66] << 16) | (data[67] << 8) | data[68]
                                F37_F = (data[69] << 16) | (data[70] << 8) | data[71]
                                print(f"totalizer in DEC : {F37_T} Flowrate in DEC : {F37_F}")
                                F37_T = (hex(F37_T))
                                F37_F = (hex(F37_F))
                                print(f"totalizer in HEX : {F37_T} Flowrate in HEX : {F37_F}")

                            if data[72] == 10:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[10]}")
                                F38_T = (data[73] << 24) | (data[74] << 16) | (data[75] << 8) | data[76]
                                F38_F = (data[77] << 8) | (data[78] << 8) | data[79]
                                print(f"totalizer in DEC : {F38_T} Flowrate in DEC : {F38_F}")
                                F38_T = (hex(F38_T))
                                F38_F = (hex(F38_F))
                                print(f"totalizer in HEX : {F38_T} Flowrate in HEX : {F38_F}")

                            if data[80] == 11:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[11]}")
                                F39_T = (data[81] << 24) | (data[82] << 16) | (data[83] << 8) | data[84]
                                F39_F = (data[85] << 8) | (data[86] << 8) | data[87]
                                print(f"totalizer in DEC : {F39_T} Flowrate in DEC : {F39_F}")
                                F39_T = (hex(F39_T))
                                F39_F = (hex(F39_F))
                                print(f"totalizer in HEX : {F39_T} Flowrate in HEX : {F39_F}")

                            if data[88] == 12:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[12]}")
                                F40_T = (data[89] << 24) | (data[90] << 16) | (data[91] << 8) | data[92]
                                F40_F = (data[93] << 8) | (data[94] << 8) | data[95]
                                print(f"totalizer in DEC : {F40_T} Flowrate in DEC : {F40_F}")
                                F40_T = (hex(F40_T))
                                F40_F = (hex(F40_F))
                                print(f"totalizer in HEX : {F40_T} Flowrate in HEX : {F40_F}")

                            if data[96] == 13:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[13]}")
                                F41_T = (data[97] << 24) | (data[98] << 16) | (data[99] << 8) | data[100]
                                F41_F = (data[101] << 8) | (data[102] << 8) | data[103]
                                print(f"totalizer in DEC : {F41_T} Flowrate in DEC : {F41_F}")
                                F41_T = (hex(F41_T))
                                F41_F = (hex(F41_F))
                                print(f"totalizer in HEX : {F41_T} Flowrate in HEX : {F41_F}")

                            if data[104] == 14:
                                print(f"Flowmeter_ID: {flowmeter_ids_shaft3[14]}")
                                F42_T = (data[105] << 24) | (data[106] << 16) | (data[107] << 8) | data[108]
                                F42_F = (data[109] << 8) | (data[110] << 8) | data[111]
                                print(f"totalizer in DEC : {F42_T} Flowrate in DEC : {F42_F}")
                                F42_T = (hex(F42_T))
                                F42_F = (hex(F42_F))
                                print(f"totalizer in HEX : {F42_T} Flowrate in HEX : {F42_F}")

                            
        
                    #print(f"Data from slave {slave_id} in HEX:", end=" ")
                    #for value in data:
                    #    print(hex(value), end=" ")
                    #print()  
                    print()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()
            print(f"close#############################################")
            #time.sleep(2)

            
            

