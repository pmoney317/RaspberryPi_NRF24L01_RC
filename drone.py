#Slave file that controls servos and brushless motor
#Includes debug statements for testing
#3/20/2025
#Python 3.11.2
#File receives NRF data and plugs into motors 
#---Motor1 Pin 12
#---Motor2 Pin 19
#---Motor3 Pin 21
#---Brushless Motor Pin 26
#---Button Pin 2

import time
from lib_nrf24 import NRF24
import spidev
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPALevel(NRF24.PA_HIGH)
radio.setPayloadSize(32)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setChannel(0x60)
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.startListening()
#Setup radio with the following settings

#*****MAKE SURE TO CALIBRATE MOTOR BEFORE TURNING ON TRANSMITTER*****
#Calibrates brushless motor before running loop
def calbratemotor():
    calpin = 26
    buttonpin = 2

    GPIO.setup(calpin, GPIO.OUT)
    GPIO.setup(buttonpin, GPIO.IN)

    pwm = GPIO.PWM(calpin, 50)
    pwm.start(0)


    print("Full throttle")
    pwm.ChangeDutyCycle(10)
    time.sleep(2)

    try:
        while GPIO.input(buttonpin) == GPIO.HIGH:
            pass
        else:
            print("Low Speed")
            pwm.ChangeDutyCycle(5)
            time.sleep(2)

            print("Half Speed")
            pwm.ChangeDutyCycle(7.5)
            time.sleep(4)
    finally:
        pass

#nrf receiver
def receive_message():
    if radio.available():
        received_message = []
        radio.read(received_message, radio.getDynamicPayloadSize())
        print("Raw Received Bytes: {}".format(received_message))
        string = ""
        for n in received_message:
            if 32 <= n <= 126:
                string += chr(n)
        print("Received message in text: {}".format(string))
        angle = string[1:]
        starterval = string[0]
        time.sleep(0.1)
        return starterval, angle
    return None, None
    

#first motor
def set_angle(angle):
    servo_pin1 = 12

    GPIO.setup(servo_pin1, GPIO.OUT)

    pwm = GPIO.PWM(servo_pin1, 50)
    pwm.start(0)
    motor1val = float(angle)

    def angle_to_duty_cycle(motor1val):
        if motor1val < 0 or motor1val > 180:
            print("Invalid angle received for servo 1")
            pass
        else:
            duty = motor1val / 18 + 2
            GPIO.output(servo_pin1, True)
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)
            GPIO.output(servo_pin1, False)
            pwm.ChangeDutyCycle(0)

    try:
        angle_to_duty_cycle(motor1val)
    finally:
        pwm.stop()

#secondmotor
def second_angle(angle):
    servo_pin2 = 19

    GPIO.setup(servo_pin2, GPIO.OUT)

    pwm = GPIO.PWM(servo_pin2, 50)
    pwm.start(0)
    motor2val = float(angle)

    def second_to_duty_cycle(motor2val):
        if motor2val < 0 or motor2val > 180:
            print("Invalid angle received for servo 2")
            pass
        else:
            duty = motor2val / 18 + 2
            GPIO.output(servo_pin2, True)
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)
            GPIO.output(servo_pin2, False)
            pwm.ChangeDutyCycle(0)

    try:
        second_to_duty_cycle(motor2val)
    finally:
        pwm.stop()

#thirdmotor
def third_angle(angle):
    servo_pin3 = 21

    GPIO.setup(servo_pin3, GPIO.OUT)

    pwm = GPIO.PWM(servo_pin3, 50)
    pwm.start(0)
    motor2val = float(angle)

    def third_to_duty_cycle(motor2val):
        if motor2val < 0 or motor2val > 180:
            print("Invalid angle received for servo 3")
            pass
        else:
            duty = motor2val / 18 + 2
            GPIO.output(servo_pin3, True)
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)
            GPIO.output(servo_pin3, False)
            pwm.ChangeDutyCycle(0)

    try:
        third_to_duty_cycle(motor2val)
    finally:
        pwm.stop()

def brushlessmotor(angle):
    brushpin = 26
    GPIO.setup(brushpin, GPIO.OUT)

    pwm = GPIO.PWM(brushpin, 50)
    pwm.start(0)

    try:
        brushval = float(angle)

        if brushval < 5:
            pwm.ChangeDutyCycle(5)
        elif brushval > 10:
            pwm.ChangeDutyCycle(10)
        else:
            pwm.ChangeDutyCycle(brushval)

        time.sleep(0.5)

    finally:
        pass

#Receiver command compiler
if __name__ == "__main__":
    calbratemotor()
    try:
        while True:
            starterval, angle = receive_message()
            if starterval and angle:
                if starterval == "A":
                    set_angle(angle)
                elif starterval == "B":
                    second_angle(angle)
                    third_angle(angle)
                elif starterval == "C":
                    brushlessmotor(angle)
                else:
                    print("Error receiver data not formatted correctly")
                    pass
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Receiver timeout")
    finally:
        GPIO.cleanup()
