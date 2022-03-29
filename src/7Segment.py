import smbus
class sevenSegment:
    def __init__(self, address):
        self.address = address
        self.i2c_object = smbus.SMBus(1)

    def write_number(self,number):
        self.i2c_object.write_byte(self.address,number)