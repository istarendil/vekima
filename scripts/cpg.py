import numpy as np
from oscillator import hopf_integrate, hopf_parameters, hopf_plot
from mapper import tc_joint, ctr_joint
import matplotlib.pyplot as plt
import time


# CPG constants
sample_time = 0.03                      # Sample time
ctr_offsset = 10


def get_angles(t):
    osc = np.zeros([6])
    osc[:] = hopf_integrate(t)
    return tc_joint(osc[0:2]), ctr_joint(osc[3:6], ctr_offsset)


if __name__ == '__main__':

    # Variables de prueba
    d_range = 300
    tc_out = np.zeros([d_range , 6])
    ctr_out = np.zeros([d_range , 6])

    # Get first two values separately (to compile C functions)
    tc_out[0, :], ctr_out[0, :] = get_angles(0)
    tc_out[1, :], ctr_out[1, :] = get_angles(sample_time)

    # Variables de prueba
    t_t = np.zeros([d_range])
    ti = 2*sample_time
    t_t[1] = ti

    # Variables de prueba
    max_t = float('-inf')

    for i in range(2, d_range):
        time.sleep(sample_time)
        start = time.time()

        tc_angles, ctr_angles = get_angles(ti)
        tc_out[i, :] = tc_angles
        ctr_out[i, :] = ctr_angles

        stop = time.time() - start
        print('Step time({}): {}'.format(i, stop))
        max_t = max(max_t, stop)

        ti += sample_time
        t_t[i] = ti

    print('Max step CPG time)', max_t)
    plt.plot(t_t, tc_out[:, 0], t_t, tc_out[:, 1], t_t, ctr_out[:, 0], t_t, ctr_out[:,1])
    plt.show()

