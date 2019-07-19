"""2D Representation."""

from __future__ import print_function, absolute_import

import numpy as np

import nengo

import matplotlib.pyplot as plt


# build model
model = nengo.Network(label="2D Representation")

with model:
    neurons = nengo.Ensemble(100, dimensions=2)

with model:
    sin = nengo.Node(output=np.sin)
    cos = nengo.Node(output=np.cos)

with model:
    nengo.Connection(sin, neurons[0])
    nengo.Connection(cos, neurons[1])

with model:
    sin_probe = nengo.Probe(sin, "output")
    cos_probe = nengo.Probe(cos, "output")
    neurons_prob = nengo.Probe(neurons, "decoded_output", synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(10)


plt.figure()
plt.plot(sim.trange(), sim.data[neurons_prob], label="Decoded output")
plt.plot(sim.trange(), sim.data[sin_probe], "r", label="Sine")
plt.plot(sim.trange(), sim.data[cos_probe], "k", label="Cosine")

plt.legend()
plt.show()
