# Energy meter logging 
# Selec 1P 100A 
# Refer the datasheet for more details
#
import pymodbus
import serial
import time
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient
import struct
import sys
client= ModbusClient(method = "rtu", port="COM19",stopbits = 1, bytesize = 8, parity = 'N', baudrate= 9600,timeout=1)
connection = client.connect()
file = open('EM2M_1P_C_100a.txt','a')
while True:
    result= client.read_holding_registers(0x01,2,unit= 0x01)# starting address, no of registers, device ID(sensor address)
    SLAVE=result.registers[0]
    print("Slave ID :",SLAVE)
    try:
        print("-----------------------------------------------------------------------------------------------------")
        reading = client.read_input_registers(0x14,2,unit= 0x01) # AC Input Voltage addres is 21 software base address is starting from 0 so 21-1 = 20
        raw = struct.pack('>HH', reading.registers[1], reading.registers[0])    # from two registers
        V_IN = struct.unpack('>f', raw)[0]
        print("INput Voltage is :",V_IN)
        print("-----------------------------------------------------------------------------------------------------")
    except:
        print("modbus error")
        V_IN = "-NA-"
    try:
        print("-----------------------------------------------------------------------------------------------------")
        reading = client.read_input_registers(0x16,2,unit= 0x01) # AC Input Current addres is 23 software base address is starting from 0 so 23-1 = 22
        raw = struct.pack('>HH', reading.registers[1], reading.registers[0])    # from two registers
        A_IN = struct.unpack('>f', raw)[0]
        print("AC Input Current:",A_IN)
        print("-----------------------------------------------------------------------------------------------------")
    except:
        print("modbus error")
        A_IN = "-NA-"
    try:
        print("-----------------------------------------------------------------------------------------------------")
        reading = client.read_input_registers(24,2,unit= 0x01) # Power Factor addres is 25 software base address is starting from 0 so 25-1 = 24
        raw = struct.pack('>HH', reading.registers[1], reading.registers[0])    # from two registers
        PF = struct.unpack('>f', raw)[0]
        print("AC Power Factor:",PF)
        print("-----------------------------------------------------------------------------------------------------")
    except:
        print("modbus error")
        PF = "-NA-"
    try:
        print("-----------------------------------------------------------------------------------------------------")
        reading = client.read_input_registers(26,2,unit= 0x01) # AC Frequency addres is 27 software base address is starting from 0 so 27-1 = 26
        raw = struct.pack('>HH', reading.registers[1], reading.registers[0])    # from two registers
        Frequency = struct.unpack('>f', raw)[0]
        print("AC Input Frequency:",Frequency)
        print("-----------------------------------------------------------------------------------------------------")
    except:
        print("modbus error")
        Frequency = "-NA-"
    try:
        print("-----------------------------------------------------------------------------------------------------")
        reading = client.read_input_registers(149,1,unit= 0x01) # Total Kwh addres is 150 software base address is starting from 0 so 150-1 = 149
        raw = struct.pack('>HH', reading.registers[1], reading.registers[0])    # from two registers
        Kwh = struct.unpack('>f', raw)[0]
        print("Kilo Whatt Hourt:",Kwh)
        print("-----------------------------------------------------------------------------------------------------")
    except:
        print("modbus error")
        Kwh = "-NA-"
    try:
        print("-----------------------------------------------------------------------------------------------------")
        reading = client.read_input_registers(0x00,2,unit= 0x01) # AC Frequency addres is 27 software base address is starting from 0 so 27-1 = 26
        raw = struct.pack('>HH', reading.registers[1], reading.registers[0])    # from two registers
        TAE = struct.unpack('>f', raw)[0]
        print("Total Active Energy:",TAE)
        print("-----------------------------------------------------------------------------------------------------")
    except:
        print("modbus error")
        TAE = "-NA-"
    file = open('EM2M_1P_C_100a.csv','a')
    file.write('\n')
    file.write(str(int(time.time())))
    file.write('\t')
    file.write(str(V_IN))
    file.write('\t')
    file.write(str(A_IN))
    file.write('\t')
    file.write(str(PF))
    file.write('\t')
    file.write(str(Frequency))
    file.write('\t')
    file.write(str(TAE))
    file.flush
    file.close
    time.sleep(60)
