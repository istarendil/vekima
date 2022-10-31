# Import the PCA9685 module.
import Adafruit_PCA9685
from time import sleep

# Initialize the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()


# Configure min and max servo pulse lengths (out of 4096)
servo_min = 0.95  # (1ms)
servo_max = 2.1  # (2ms)

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

def set_servo_deg(channel,angle):
    factor = (servo_max - servo_min)/2
    pulse = (angle*factor/90) + servo_min
    set_servo_ms(channel, pulse)


if __name__ == '__main__':
    
    print('Moving servo, press Ctrl-C to quit...')
    x = 90

    while True:
        # Move servo on channel O between extremes.
        while x > 60: 
            x = x - 2
            set_servo_deg(4,x,0.05)
        while x < 120:
            x = x + 5
            set_servo_deg(4,x,0.05)

