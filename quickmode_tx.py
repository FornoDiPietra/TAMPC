import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev


def fillWithPadding(byteBlock, blockSize):
    while (len(byteBlock) < blockSize):
        byteBlock = byteBlock + chr(0x00)

    return byteBlock

def readFile(fileName, blockSize):
    blocks = []

    with open(fileName, "rb") as f:
        byteBlock = f.read(blockSize)

        while byteBlock != b'':
            if (len(byteBlock) < blockSize):
                byteBlock = fillWithPadding(byteBlock, blockSize)
            
            blocks.append(  byteBlock ) 
            byteBlock = f.read(blockSize)
        f.close()

    return blocks

def bytesToString(bytesObj):
    formattedString = ""
    for b in bytesObj:
        #s = format(b, '02x')
        s = format(b, '02d')
        formattedString += s + ' '
    return formattedString



blockSize = 32

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)
radio.setRetries(15,0)
radio.setPayloadSize(blockSize)
radio.setChannel(0x60)               #change channel here

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)       #change power here
radio.setAutoAck(False)
#radio.enableDynamicPayloads()
#radio.enableAckPayload()


radio.openWritingPipe(pipes[1])

# ######################################################################

# radio.write_register(0x00,0b00001110)   #transmitter
# radio.write_register(0x01,0b00000000)   # disable auto ACK for any pipe
# radio.write_register(0x02,0b00000001)   # disable all pipes except for pipe 0
# radio.write_register(0x03,0b00000001)   # 3 bytes addresses
# radio.write_register(0x04,0b00000000)   # disable retransmissions
# radio.write_register(0x05,0x60)
# radio.write_register(0x06,0b00000110)   # maximum output power
# #radio.write_register(0x07,)
# radio.write_register(0x0A,[0xE7, 0xE7, 0xE7],3)
# #print(radio.read_register(0x0A,5))
# radio.write_register(0x10,[0xE7, 0xE7, 0xE7],3)
# radio.write_register(0x11,32)

radio.print_status(radio.get_status())

radio.printDetails()



## Read the file
print("reading file")
blocks = readFile("test.txt",blockSize-1)
print("blocks:", len(blocks))


raw_input("press button to start transmission")

i=0
while True:
    tx_buffer = bytearray(chr(i) + blocks[i])
        

    radio.write( tx_buffer )
    print("Transmitting: " + bytesToString(tx_buffer))
    i+=1
    if (i >= len(blocks)):
        i = 0

    time.sleep(0.01)

    #n = raw_input("wait for key press")
    
    
for a in final_buf:
    newFileByteArray = bytearray(a)
    newFile.write(newFileByteArray)

newFile.close()
