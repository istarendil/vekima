import numpy as np
import matplotlib.pyplot as plt
from time import sleep,time
import threading

from CPG import oscillators
from Mapper import tc_joint, ctr_joint
from Servos import set_servo_deg


def plot_osc():

    fig1 = plt.figure()
    fig1.suptitle('CPG outputs')
    plt.subplot(2, 1, 1)
    plt.plot(t, osc1, t, osc3, t, osc5)
    plt.grid()
    plt.title('Left oscillators')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.subplot(2, 1, 2)
    plt.plot(t, osc2, t, osc4, t, osc6)
    plt.grid()
    plt.title('Rigth oscillators')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')


def plot_joint(tc_1, ctr_1):
    plt.figure()
    plt.title('Joint space')
    plt.plot(t, tc_1, t, ctr_1)
    plt.grid()


if __name__ == '__main__':


    # CPG parameters
    CPG_period = 2.5                # seconds
    CPG_phase = 180                 # deg
    CPG_freq = 1 / CPG_period

    # Simulation parameters
    sim_time = 8*CPG_period
    sample_time = 0.04

    # Oscillators curves
    t = np.arange(0, sim_time, sample_time)
    y0 = [0, 0, 0, 0.01, 0, 0]
    # Parameters (time_interval, initial_conditions, frequency, amplitude, theta, alpha, eps)
    start =time()
    [osc1, osc3, osc5] = oscillators(t, y0, CPG_freq, CPG_phase, 6, 0.4)
    [osc2, osc4, osc6] = [-osc1, -osc3, -osc5]
    stop = time()-start
    print('total CPG time:', stop)

    # Map from CPG to TC-joint space
    TC_amp = 40

    TC_offset = 90       # deg
    [TC_1, TC_2, TC_3, TC_4, TC_5, TC_6] = tc_joint(TC_amp, TC_offset, osc1, osc2, osc3, osc4, osc5, osc6)

    # Map from CPG to CTr-joint space
    CTr_amp = 90
    CTr_offset = 90       # deg
    CTr_phase = 90         # deg
    CTr_lag = np.int(np.round(CTr_phase*CPG_period/(360*sample_time)))
    start =time()
    [CTr_1, CTr_2, CTr_3, CTr_4, CTr_5, CTr_6] = ctr_joint(CTr_amp, CTr_offset, CTr_lag, osc1, osc2, osc3, osc4, osc5, osc6)
    stop = time()-start
    print('total Mapper time:', stop)

    # Plot CPG results
    plot_osc()

    # Plot joints
    plot_joint(TC_1, CTr_1)
    plot_joint(TC_2, CTr_2)
    #plot_joint(TC_3, CTr_3)
    #plot_joint(TC_4, CTr_4)
    #plot_joint(TC_5, CTr_5)
    #plot_joint(TC_6, CTr_6)

    plt.show()

    i = 0
    c = 1
    min_t =float('-inf')
    def servo_execute():
        global i
        global c
        
        start = time()
        #set_servo_deg(2, TC_1[i])
        #set_servo_deg(3, CTr_1[i])
        #set_servo_deg(4, TC_2[i])
        #set_servo_deg(5, CTr_2[i])
            
        #set_servo_deg(6, TC_3[i])
        #set_servo_deg(7, CTr_3[i])
        #set_servo_deg(8, TC_4[i])
        #set_servo_deg(9, CTr_4[i])

        #set_servo_deg(10, TC_5[i])
        #set_servo_deg(11, CTr_5[i])
        #set_servo_deg(12, TC_6[i])
        #set_servo_deg(13, CTr_6[i])
        #stop = time()-start
        #print('I2c_time:',stop)

        if c == 1:
            t_timer = threading.Timer(sample_time-stop,servo_execute).start()
        
        if i>=t.size-1:
            i=0
        else:
            i = i+1


    servo_execute()
    
    # Enviamos a los servos

    while True:
        key_in = input('Press s to quit or r to restart...')
        if key_in == 's':
            c = 0
            print('CPG active...')
        elif key_in == 'r':
            c = 1
            print('CPG stopped...')
            servo_execute()

