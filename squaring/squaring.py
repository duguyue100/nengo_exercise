"""Squaring the input."""

from __future__ import print_function, absolute_import

import numpy as np

import nengo

import matplotlib.pyplot as plt

model = nengo.Network(label="Squaring")

with model:
    A = nengo.Ensemble(100, dimensions=1)
    B = nengo.Ensemble(100, dimensions=1)

with model:
    sin = nengo.Node(np.sin)

    nengo.Connection(sin, A)

    def square(x):
        return x[0]*x[0]

    nengo.Connection(A, B, function=square)

with model:
    sin_probe = nengo.Probe(sin)
    A_probe = nengo.Probe(A, synapse=0.01)
    B_probe = nengo.Probe(B, synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(5)

plt.figure()
plt.plot(sim.trange(), sim.data[A_probe], label="output A")
plt.plot(sim.trange(), sim.data[B_probe], label="output B")
plt.plot(sim.trange(), sim.data[sin_probe], label="Sine",
         color="k", linewidth=2.0)
plt.legend(loc="best")

plt.show()
