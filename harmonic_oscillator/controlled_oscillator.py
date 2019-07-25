"""Controlled Oscillator."""

from __future__ import print_function, absolute_import

import nengo
from nengo.processes import Piecewise

import matplotlib.pyplot as plt

tau = 0.1
w_max = 10

model = nengo.Network(label="Controlled Oscillator")

with model:
    oscillator = nengo.Ensemble(500, dimensions=3, radius=1.7)

    def feedback(x):
        x0, x1, w = x
        return x0+w*w_max*tau*x1, x1-w*w_max*tau*x0, 0

    nengo.Connection(oscillator, oscillator, function=feedback, synapse=tau)

    frequency = nengo.Ensemble(100, dimensions=1)

    nengo.Connection(frequency, oscillator[2])

# create input
with model:
    initial = nengo.Node(Piecewise({
        0: [1, 0, 0],
        0.15: [0, 0, 0]}))

    nengo.Connection(initial, oscillator)

    input_frequency = nengo.Node(
        Piecewise({
            0: 1,
            1: 0.5,
            2: 0,
            3: -0.5,
            4: -1}))

    nengo.Connection(input_frequency, frequency)

with model:
    oscillator_probe = nengo.Probe(oscillator, synapse=0.03)

with nengo.Simulator(model) as sim:
    sim.run(5)

plt.figure()
plt.plot(sim.trange(), sim.data[oscillator_probe])
plt.legend(["x0", "x1", r"$\omega$"])

plt.show()
