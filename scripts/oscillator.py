import numpy as np
from jitcode import y, jitcode
from sympy import symbols
from symengine import sin, cos
import matplotlib.pyplot as plt
import time


# ODE constants
y0 = [0, 0, 0.01, 0, 0, 0, 0, 0, 0, 0, 0, 0]        # Initial amplitudes
t0 = 0                                              # Initial time
alpha = 6                                           # Convergence speed factor
eps = 0.4                                           # Coupling strength

# ODE default parameters
CPG_period = 1                                      # Period (seconds)
CPG_freq = 2 * np.pi / CPG_period                   # Frequency (rad)
TC_amplitude = 0.9                                  # TC-joint amplitude
CTr_amplitude = np.square(0.4)                      # CTr-joint amplitude
TC_phase = 180                                      # TC-joint phase angle(deg)
CTr_phase = 90                                      # CTr-joint phase angle(deg)

# ODE symbols
mu1 = symbols('mu1')
mu2 = symbols('mu2')
w = symbols('w')
theta1 = symbols('theta1')
theta2 = symbols('theta2')

# No-variable parameters
mu2 = CTr_amplitude
theta1 = np.deg2rad(TC_phase)
theta2 = np.deg2rad(CTr_phase)


# Hopf ODEs definition function
def hopf():
    # Front leg (TC-joint)
    dydt0 = alpha * y(0) * (mu1 - y(0) ** 2 - y(1) ** 2) + w * y(1) + eps * (y(2) * cos(theta1) - y(3) * sin(theta1)) + eps * (y(6) * cos(theta2) - y(7) * sin(theta2))
    dydt1 = alpha * y(1) * (mu1 - y(0) ** 2 - y(1) ** 2) - w * y(0)

    # Middle leg (TC-joint)
    dydt2 = alpha * y(2) * (mu1 - y(2) ** 2 - y(3) ** 2) + w * y(3) + eps * (y(0) * cos(theta1) + y(4) * cos(theta1) - y(1) * sin(theta1) - y(2) * sin(theta1)) + eps * (y(8) * cos(theta2) - y(9) * sin(theta2))
    dydt3 = alpha * y(3) * (mu1 - y(2) ** 2 - y(3) ** 2) - w * y(2)

    # Hind leg (TC-joint)
    dydt4 = alpha * y(4) * (mu1 - y(4) ** 2 - y(5) ** 2) + w * y(5) + eps * (y(2) * cos(theta1) + y(3) * sin(theta1)) + eps * (y(10) * cos(theta2) - y(11) * sin(theta2))
    dydt5 = alpha * y(5) * (mu1 - y(4) ** 2 - y(5) ** 2) - w * y(4)

    # Front leg (CTr-joint)
    dydt6 = alpha * y(6) * (mu2 - y(6) ** 2 - y(7) ** 2) + w * y(7) + eps * (y(0) * cos(theta2) - y(1) * sin(theta2))
    dydt7 = alpha * y(7) * (mu2 - y(6) ** 2 - y(7) ** 2) - w * y(6)

    # Middle leg (CTr-joint)
    dydt8 = alpha * y(8) * (mu2 - y(8) ** 2 - y(9) ** 2) + w * y(9) + eps * (y(2) * cos(theta2) - y(3) * sin(theta2))
    dydt9 = alpha * y(9) * (mu2 - y(8) ** 2 - y(9) ** 2) - w * y(8)

    # Hind leg (CTr-joint)
    dydt10 = alpha * y(10) * (mu2 - y(10) ** 2 - y(11) ** 2) + w * y(11) + eps * (y(4) * cos(theta2) - y(5) * sin(theta2))
    dydt11 = alpha * y(11) * (mu2 - y(10) ** 2 - y(11) ** 2) - w * y(10)

    return np.array([dydt0, dydt1, dydt2, dydt3, dydt4, dydt5, dydt6, dydt7, dydt8, dydt9, dydt10, dydt11])


# Hopf numerical integration (compiled to C by jitcode)
def hopf_integrate(t):
    y = ODE.integrate(t)  # get one more value, add it to the array
    return y[1], y[3], y[5], y[7], y[9], y[11]


# Change parameters online
def hopf_parameters(tc_amplitude, cpg_freq):
    tc_amplitude = np.clip(tc_amplitude, 0.2, 0.9)
    ODE.set_parameters(np.square(tc_amplitude), cpg_freq)
    return


# Oscillator output plots
def hopf_plot(ti, osc1, osc2, osc3, osc4, osc5, osc6):
    fig1 = plt.figure()
    fig1.suptitle('CPG outputs')
    plt.subplot(2, 1, 1)
    plt.plot(ti, osc1, ti, osc3, ti, osc5)
    plt.grid()
    plt.title('Left oscillators')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.subplot(2, 1, 2)
    plt.plot(ti, osc2, ti, osc4, ti, osc6)
    plt.grid()
    plt.title('Rigth oscillators')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')


# Jitcode ODE definition and integration method selection
ODE = jitcode(f_sym=hopf(), control_pars=(mu1, w), wants_jacobian=False)
ODE.set_integrator('vode', method='adams')

# Set initial conditions and default parameters
ODE.set_initial_value(y0, t0)
hopf_parameters(TC_amplitude, CPG_freq)
