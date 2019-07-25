"""Controlled Integrator 2."""

from __future__ import print_function, absolute_import

import numpy as np

import nengo
from nengo.processes import Piecewise

import matplotlib.pyplot as plt


# build model
model = nengo.Network(label="Controlled Integrator 2")

with model:
    A = nengo.Ensemble(225, dimensions=2, radius=1.5)

with model:
    input_func = Piecewise({
        0.2: 5,
        0.3: 0,
        0.44: -10,
        0.54: 0,
        0.8: 5,
        0.9: 0})
    inp = nengo.Node(output=input_func)

    tau = 0.1
    nengo.Connection(inp, A, transform=[[tau], [0]], synapse=0.1)

with model:
    control_func = Piecewise({0: 0, 0.6: -0.5})
    control = nengo.Node(output=control_func)

    nengo.Connection(control, A[1], synapse=0.005)

with model:
    nengo.Connection(
        A, A[0], function=lambda x: x[0]*x[1]+x[0], synapse=tau)
    A_probe = nengo.Probe(A, "decoded_output", synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(1.4)

t = sim.trange()
dt = t[1]-t[0]
input_sig = input_func.run(t[-1], dt=dt)
control_sig = control_func.run(t[-1], dt=dt)
ref = dt*np.cumsum(input_sig)

plt.figure(figsize=(6, 8))
plt.subplot(211)
plt.plot(t, input_sig, label="input")
plt.ylabel("label")
plt.legend()

plt.subplot(212)
plt.plot(t, ref, "k--", label="exact")
plt.plot(t, sim.data[A_probe][:, 0], label="A (value)")
plt.plot(t, sim.data[A_probe][:, 1], label="A (control)")
plt.ylabel("x(t)")
plt.legend()

plt.show()
