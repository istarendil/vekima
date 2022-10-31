import numpy as np
from scipy import integrate
from time import time


def hopf(t, y, f, theta, alpha, eps):
    #mu = np.square(mu)  # Amplitue
    mu = 1
    w = 2 * np.pi * f  # freq radians/s

    dydt0 = alpha * y[0] * (mu - y[0] ** 2 - y[1] ** 2) + w * y[1] + eps * (y[2] * np.cos(theta) - y[3] * np.sin(theta))
    dydt1 = alpha * y[1] * (mu - y[0] ** 2 - y[1] ** 2) - w * y[0]

    dydt2 = alpha * y[2] * (mu - y[2] ** 2 - y[3] ** 2) + w * y[3] + eps * (y[0] * np.cos(theta) + y[4] * np.cos(theta) + y[1] * np.sin(theta) - y[2] * np.sin(theta))
    dydt3 = alpha * y[3] * (mu - y[2] ** 2 - y[3] ** 2) - w * y[2]

    dydt4 = alpha * y[4] * (mu - y[4] ** 2 - y[5] ** 2) + w * y[5] + eps * (y[2] * np.cos(theta) + y[3] * np.sin(theta))
    dydt5 = alpha * y[5] * (mu - y[4] ** 2 - y[5] ** 2) - w * y[4]

    return np.array([dydt0, dydt1, dydt2, dydt3, dydt4, dydt5])


def oscillators(t, y0, f, theta, alpha, eps):

    theta = np.deg2rad(theta)
    y = np.zeros((len(t), len(y0)))  # array for solution
    y[0, :] = y0

    r = integrate.ode(hopf).set_integrator("dopri5")  # choice of method
    r.set_initial_value(y0, t[0])  # initial values
    # Parámetros extra (frequancy, Amplitude, theta, alpha, eps)
    r.set_f_params(f, theta, alpha, eps)

    max_t = float('-inf')
    for i in range(1, t.size):
        start = time()
        y[i, :] = r.integrate(t[i])  # get one more value, add it to the array
        if not r.successful():
            raise RuntimeError("Could not integrate")
        stop = time()-start
        max_t = max(max_t,stop)
    print('Step CPG time:', max_t)
    return y[:, 1], y[:, 3], y[:, 5]
