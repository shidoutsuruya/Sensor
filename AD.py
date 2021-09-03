import smbus  
import time
import matplotlib.pyplot as plt
import numpy as np
bus = smbus.SMBus(1)        
def setup(Addr):
    global address
    address = Addr

def read(chn): #channel
    if chn == 0:
        bus.write_byte(address,0x40)   
    if chn == 1:
        bus.write_byte(address,0x41)
    if chn == 2:
        bus.write_byte(address,0x42)
    if chn == 3:
        bus.write_byte(address,0x43)
    bus.read_byte(address)        
    return bus.read_byte(address)  

def write(val):
    temp = int(val)
    bus.write_byte_data(address, 0x40, temp) 


if __name__ == "__main__":
    plt.ion()
    plt.figure("temperature") 
    plt.title('hello world')
    setup(0x48)
    t_now=0
    t=[]
    m=[]
    m2=[]
    print(type(read(0)))
    print(type(read(1)))
    while True: 
        t_now+=1
        t.append(t_now)
        m.append(read(0))
        m2.append(read(1))
        plt.plot(t,m,'-r')
        plt.plot(t,m2,'-r')
        plt.pause(0.001)
       # print ( 'AIN0:',read(0),'AIN1:',read(1),'AIN2:',read(2))