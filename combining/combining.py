"""Combining."""

from __future__ import print_function, absolute_import

import numpy as np

import matplotlib.pyplot as plt

import nengo


# build model

model = nengo.Network(label="Combining")

with model:
    A = nengo.Ensemble(100, dimensions=1)
    B = nengo.Ensemble(100, dimensions=1)

    output = nengo.Ensemble(200, dimensions=2, label="2D population")


with model:
    sin = nengo.Node(output=np.sin)
    cos = nengo.Node(output=np.cos)

with model:
    nengo.Connection(sin, A)
    nengo.Connection(cos, B)

    nengo.Connection(A, output[1])
    nengo.Connection(B, output[0])

# probes
with model:
    sin_probe = nengo.Probe(sin)
    cos_probe = nengo.Probe(cos)

    A_probe = nengo.Probe(A, synapse=0.01)
    B_probe = nengo.Probe(B, synapse=0.01)

    out_probe = nengo.Probe(output, synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(5)

plt.figure()
plt.plot(sim.trange(), sim.data[out_probe][:, 0], "b", label="2D output")
plt.plot(sim.trange(), sim.data[out_probe][:, 1], "g", label="2D output")
plt.plot(sim.trange(), sim.data[A_probe], "r", label="A output")
plt.plot(sim.trange(), sim.data[sin_probe], "k", label="Sine")

plt.legend()
plt.show()
