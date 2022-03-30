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
        self.write_number(clear)
        
    def place_cursor(self, position):
        self.write_number(0x79)
        self.write_number(position)
	
    def decimal_control(self,placement):
        self.write_number(0x77)
        self.write_number(placement)

    def individual_segment(self, digit, segment):
        self.write_number(hex(digit+0x7B))
        segment_binary = 0
        if "a" in segment.lower():
            segment_binary += 0b0000001 
        if "b" in segment.lower():
            segment_binary += 0b0000010 
        if "c" in segment.lower():
            segment_binary += 0b0000100
        if "d" in segment.lower():
            segment_binary += 0b0001000 
        if "e" in segment.lower():
            segment_binary += 0b0010000
        if "f" in segment.lower():
            segment_binary += 0b0100000
        if "g" in segment.lower():
            segment_binary += 0b1000000
            
        self.write_number(segment_binary)


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
