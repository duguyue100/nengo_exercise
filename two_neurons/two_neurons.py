"""Two neurons."""

from __future__ import absolute_import, print_function

import numpy as np
import matplotlib.pyplot as plt

import nengo
from nengo.utils.matplotlib import rasterplot
from nengo.dists import Uniform

# build model
model = nengo.Network(label="Two neurons.")

with model:
    neurons = nengo.Ensemble(
        2,
        dimensions=1,
        intercepts=Uniform(-.5, -.5),
        max_rates=Uniform(100, 100),
        encoders=[[1], [-1]])

with model:
    sin = nengo.Node(lambda t: np.sin(8*t))
    nengo.Connection(sin, neurons, synapse=0.01)

with model:
    sin_probe = nengo.Probe(sin)
    spikes = nengo.Probe(neurons.neurons)
    voltage = nengo.Probe(neurons.neurons, "voltage")
    filtered = nengo.Probe(neurons, synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(2)

plt.figure()
plt.plot(sim.trange(), sim.data[filtered])
plt.plot(sim.trange(), sim.data[sin_probe])

plt.show()

plt.figure(figsize=(10, 8))
plt.subplot(221)
rasterplot(sim.trange(), sim.data[spikes], colors=[(1, 0, 0), [0, 0, 0]])
plt.yticks((0, 1))

plt.subplot(222)
plt.plot(sim.trange(), sim.data[voltage][:, 0]+1, "r")
plt.plot(sim.trange(), sim.data[voltage][:, 1], "k")
plt.yticks(())
#  plt.axis([0, 1, 0, 2])
plt.subplots_adjust(wspace=0.05)
plt.show()
