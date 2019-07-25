"""Simple Harmonic Oscillator."""

from __future__ import print_function, absolute_import

import nengo
from nengo.processes import Piecewise

import matplotlib.pyplot as plt

# build model
model = nengo.Network(label="Oscillator")
with model:
    neurons = nengo.Ensemble(200, dimensions=2)

with model:
    input = nengo.Node(Piecewise({0: [1, 0], 0.1: [0, 0]}))

    nengo.Connection(input, neurons)

    nengo.Connection(neurons, neurons,
                     transform=[[1, 1], [-1, 1]],
                     synapse=0.1)

with model:
    input_probe = nengo.Probe(input, "output")
    neuron_probe = nengo.Probe(neurons, "decoded_output", synapse=0.1)

with nengo.Simulator(model) as sim:
    sim.run(5)


plt.figure()
plt.plot(sim.trange(), sim.data[neuron_probe])
plt.legend(["$x_0$", "$x_1$"])

plt.show()

data = sim.data[neuron_probe]
plt.figure()
plt.plot(data[:, 0], data[:, 1], label="decoded output")
plt.show()
