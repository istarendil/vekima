import numpy as np


# TC-joint
def tc_joint(tc_amp, offset, osc1, osc2, osc3, osc4, osc5, osc6):

    tc1 = np.multiply(osc1, tc_amp) + offset
    tc2 = np.multiply(-osc2, tc_amp) + offset
    tc3 = np.multiply(osc3, tc_amp) + offset
    tc4 = np.multiply(-osc4, tc_amp) + offset
    tc5 = np.multiply(osc5, tc_amp) + offset
    tc6 = np.multiply(-osc6, tc_amp) + offset

    return tc1, tc2, tc3, tc4, tc5, tc6


def ctr_joint(ctr_amp, offset, ctr_lag, osc1, osc2, osc3, osc4, osc5, osc6):

    ctr_1 = lag2(offset, ctr_amp, ctr_lag, osc1)
    ctr_2 = lag1(offset, ctr_amp, ctr_lag, osc2)
    ctr_3 = lag2(offset, ctr_amp, ctr_lag, osc3)
    ctr_4 = lag1(offset, ctr_amp, ctr_lag, osc4)
    ctr_5 = lag2(offset, ctr_amp, ctr_lag, osc5)
    ctr_6 = lag1(offset, ctr_amp, ctr_lag, osc6)

    return ctr_1, ctr_2, ctr_3, ctr_4, ctr_5, ctr_6


def lag1(offset, ctr_amp, samples_phase, osc):

    buff = np.empty(osc.size)
    buff.fill(offset)
    buff[samples_phase:-1] = ctr_amp*osc[0:-1-samples_phase] + offset
    np.place(buff, buff < offset, offset)
    #buff[0:samples_phase] = buff[4*samples_phase:5*samples_phase]


    return buff

def lag2(offset, ctr_amp, samples_phase, osc):

    buff = np.empty(osc.size)
    buff.fill(offset)
    buff[samples_phase:-1] = -ctr_amp*osc[0:-1-samples_phase] + offset
    np.place(buff, buff > offset, offset)
    #buff[0:samples_phase] = buff[4*samples_phase:5*samples_phase]

    return buff

