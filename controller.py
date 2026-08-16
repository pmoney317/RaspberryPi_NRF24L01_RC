#Master file that sends joystick values to slave 
#3/19/2025
#Python 3.11.2
#File receives values from joysticks and ADC module and sends them to the slave through the radio
#---Joystick button Pin 26

import time
import smbus2
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import spidev

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Set up GPIO pin 26 as an input with a pull-up resistor

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPALevel(NRF24.PA_HIGH)
radio.setPayloadSize(32)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setChannel(0x60)
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
#Set up the radio with the following settings

ADS1115_ADDRESS = 0x48

REG_CONVERT = 0x00
REG_CONFIG = 0x01

CONFIG_X = [0xC3, 0x83]
CONFIG_Y = [0xD3, 0x83]
CONFIG_Z = [0xE3, 0x83]
#Set up the ADS1115 with the following settings

bus = smbus2.SMBus(1)

#Reads ADC values from ADS1115
def read_adc(channel):
    if channel == 0:
        bus.write_i2c_block_data(ADS1115_ADDRESS, REG_CONFIG, CONFIG_X)
    elif channel == 1:
        bus.write_i2c_block_data(ADS1115_ADDRESS, REG_CONFIG, CONFIG_Y)
    elif channel == 2:
        bus.write_i2c_block_data(ADS1115_ADDRESS, REG_CONFIG, CONFIG_Z)

    time.sleep(0.1)

    raw_data = bus.read_i2c_block_data(ADS1115_ADDRESS, REG_CONVERT, 2)

    raw_value = (raw_data[0] << 8) | raw_data[1]

    if raw_value > 0x7FFF:
        raw_value -= 0x10000

    return raw_value

#Reads joystick values from ADC, scales them, then sends to radio
def read_joystick():
    x_raw = read_adc(0)
    y_raw = read_adc(1)
    z_raw = read_adc(2)

    x_scaled = (x_raw * .00685)
    y_scaled = (y_raw * .0068)
    z_scaled = (z_raw * .00052)
    #Adjust values depending on joystick sensitivity

    return x_scaled, y_scaled, z_scaled

try:
    while True:
        x_value, y_value, z_value = read_joystick()
        messagex = list(f"B{x_value:.0f}")
        messagey = list(f"A{y_value:.0f}")
        messagez = list(f"C{z_value:.0f}")
        messagebutton = list("D0")

        radio.write(messagex)
        print("Sent: {}".format(messagex))
        radio.write(messagey)
        print("Sent: {}".format(messagey))
        radio.write(messagez)
        print("Sent: {}".format(messagez))
        button_state = GPIO.input(26)
        if GPIO.input(26) == GPIO.LOW:
            radio.write(messagebutton)
            print("Sent: Button Pressed")
        else:
            pass
        time.sleep(0.1)
            #Sends joystick values to receiver

except KeyboardInterrupt:
    print("Transmission Error")
