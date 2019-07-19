"""Communication channel."""

from __future__ import print_function, absolute_import

import numpy as np
import nengo

import matplotlib.pyplot as plt

# build model

model = nengo.Network(label="Communication Channel")

with model:
    sin = nengo.Node(np.sin)

    A = nengo.Ensemble(100, dimensions=1)
    B = nengo.Ensemble(100, dimensions=1)

    nengo.Connection(sin, A)
    nengo.Connection(A, B)

with model:
    sin_probe = nengo.Probe(sin)
    A_probe = nengo.Probe(A, synapse=0.01)
    B_probe = nengo.Probe(B, synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(10)

plt.figure(figsize=(9, 3))
plt.subplot(131)
plt.title("Input")
plt.plot(sim.trange(), sim.data[sin_probe])

plt.subplot(132)
plt.title("A")
plt.plot(sim.trange(), sim.data[A_probe])

plt.subplot(133)
plt.title("B")
plt.plot(sim.trange(), sim.data[B_probe])

plt.show()
