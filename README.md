# RaspberryPi_NRF24L01_RC
This is a previous project that might be useful for others attempting to use Raspberry Pis and the cheap NRF24L01 radio module. The current files in place were used with a custom made drone powered by a Pi zero and another Pi acting as the remote controller. This is configured to work with the Blavery NRF24L01 library, https://github.com/BLavery/lib_nrf24, which required me to make the necessary changes below to the library to work properly. Finding this out took me about two weeks of troubleshooting in my spare time, which is why I am uploading this project as I found very limited documentation about it elsewhere.  

***IMPORTANT CHANGES NEEDED TO WORK******************
add "self.spidev.max_speed_hz = 4000000" in the outlined location    

def begin(self, csn_pin, ce_pin=0):   # csn & ce are RF24 terminology. csn = SPI's CE!
        # Initialize SPI bus..
        # ce_pin is for the rx=listen or tx=trigger pin on RF24 (they call that ce !!!)
        # CE optional (at least in some circumstances, eg fixed PTX PRX roles, no powerdown)
        # CE seems to hold itself as (sufficiently) HIGH, but tie HIGH is safer!
        self.spidev.open(0, csn_pin)
   ----[self.spidev.max_speed_hz = 4000000]------***THIS LINE***
        self.ce_pin = ce_pin
  **************************************************

This program contains two files, the slave file is what was used with the actual drone itself while the master file is what was used with the controller setup. The controller is using a ADS1115 module connected to two analog joystick modules which is what is used to control the drone speed and rudders. The drone was setup to use three MG90S servos, one brushless motor, and a single button connected to the GPIO in order to calibrate the brushless motor module. 

In order to run this code, you likely need a Pi 4 or better. I originally tried using the drone with the first generation Pi Zero and due to sluggish performance and high packet loss during controller and drone communication, I had to use a Pi Zero 2. I would not recommend trying to use low powered boards with this configurations since this project uses Python for basically all its code. Another important note about the drone code, if you noticed that all the servos are using different functions and thinking that it would be more efficient to use them all in a single function, I already tried this and was not successful. If you are able to make the program more efficient and make this change feel free to add to this!
