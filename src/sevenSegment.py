import smbus
import time
class sevenSegment:
    def __init__(self, address):
        self.address = address
        self.i2c_object = smbus.SMBus(1)
        
    def write_number(self,number):
        self.i2c_object.write_byte(self.address,number)
 
    def clear_display(self):
        clear = 0x76
        self.i2c_object.write_byte(self.address, clear)
        
    def place_cursor(self, position):
	    self.i2c_object.write_byte(self.address, 0x79)
	    self.i2c_object.write_byte(self.address, position)
	
    def decimal_control(self,placement):    
        self.i2c_object.write_byte(self.address, 0x77)
        self.i2c_object.write_byte(self.address, placement)	    
	
def main():
    display = sevenSegment(0x71)
    display.clear_display()
    display.place_cursor(0x3)
    display.write_number(0x1)
    display.decimal_control(0b00000100)
    display.place_cursor(0x2)
    display.write_number(0x2)
    
if __name__ == "__main__":
	main()	
