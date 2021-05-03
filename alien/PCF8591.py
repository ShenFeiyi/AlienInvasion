import smbus

bus = smbus.SMBus(1)

#通过 sudo i2cdetect -y -1 可以获取到IIC的地址
def setup(Addr):
	global address
	address = Addr

def read(chn): # 读取模拟量,通道范围在0-3之间
	try:
		bus.write_byte(address,0x40+int(chn))
		bus.read_byte(address) # 开始进行读取转换
	except Exception as e:
		print ("Device address: 0x%2X" % address)
		print (e)
	return bus.read_byte(address)

def write(val): # 模拟量输出控制，范围为0-255
	try:
		bus.write_byte_data(address, 0x40, int(val))
	except Exception as e:
		print ("Device address: 0x%2X" % address)
		print (e)

