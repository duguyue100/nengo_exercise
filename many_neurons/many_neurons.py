"""Many Neurons."""

from __future__ import print_function, absolute_import

import numpy as np
import matplotlib.pyplot as plt

import nengo
from nengo.utils.ensemble import sorted_neurons
from nengo.utils.matplotlib import rasterplot

# build model
model = nengo.Network(label="Many neurons.")

with model:
    A = nengo.Ensemble(
        100,
        dimensions=1)


with model:
    sin = nengo.Node(lambda t: np.sin(8*t))
    nengo.Connection(sin, A, synapse=0.01)

with model:
    sin_probe = nengo.Probe(sin)
    A_probe = nengo.Probe(A, synapse=0.1)
    A_spikes = nengo.Probe(A.neurons)


with nengo.Simulator(model) as sim:
    sim.run(10)


plt.figure()
plt.plot(sim.trange(), sim.data[A_probe], label="A output")
plt.plot(sim.trange(), sim.data[sin_probe], "r", label="Input")
plt.legend()
plt.show()

plt.figure()
rasterplot(sim.trange(), sim.data[A_spikes])
plt.show()

indices = sorted_neurons(A, sim, iterations=250)
plt.figure()
rasterplot(sim.trange(), sim.data[A_spikes][:, indices])
plt.show()
