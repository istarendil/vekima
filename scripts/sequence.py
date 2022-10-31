# Import the PCA9685 module.
import Adafruit_PCA9685
from time import sleep

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()


# Configure min and max servo pulse lengths (out of 4096)
servo_min = 0.5  # (1ms)
servo_max = 2.5  # (2ms)

# Set frequency to 50hz
freq = 50
pwm.set_pwm_freq(freq)

# Helper function to make setting a servo pulse width simpler.
def set_servo_ms(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length /= freq       # 50 Hz
    pulse_length /= 4096     # 12 bits of resolution
    pulse *= 1000
    pulse /= pulse_length
    pwm.set_pwm(channel, 0,int(pulse))


min = 0.95
max = 2.1
print('Moving servo, press Ctrl-C to quit...')
x = 1.5

while True:
    # Move servo on channel O between extremes.
    while x > min: 
        x = x - 0.005
        sleep(0.005)
        set_servo_ms(2,x)
        set_servo_ms(4,x)
    while x < max:
        x = x + 0.005
        set_servo_ms(2,x)
        set_servo_ms(4,x)
        sleep(0.005)
    #set_servo_ms(2,x)
    #set_servo_ms(4,y)
    sleep(0.005)
