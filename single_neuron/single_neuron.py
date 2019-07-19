"""A single neuron."""

from __future__ import absolute_import, print_function

import numpy as np
import matplotlib.pyplot as plt

import nengo
from nengo.utils.matplotlib import rasterplot
from nengo.dists import Uniform

# create a single neuron

model = nengo.Network(label="A single neuron")

with model:
    neuron = nengo.Ensemble(
        1,
        dimensions=1,
        intercepts=Uniform(-.5, -.5),
        max_rates=Uniform(100, 100),
        encoders=[[1]])

with model:
    cos = nengo.Node(lambda t: np.cos(10*t))
    nengo.Connection(cos, neuron)


# add probes
with model:
    cos_probe = nengo.Probe(cos)
    spikes = nengo.Probe(neuron.neurons)
    voltage = nengo.Probe(neuron.neurons, "voltage")
    filtered = nengo.Probe(neuron, synapse=0.01)


with nengo.Simulator(model) as sim:
    sim.run(1)

plt.figure()
plt.plot(sim.trange(), sim.data[filtered])
plt.plot(sim.trange(), sim.data[cos_probe])
plt.xlim(0, 1)

plt.show()

plt.figure(figsize=(10, 8))
plt.subplot(221)
rasterplot(sim.trange(), sim.data[spikes])
plt.ylabel("Neuron")
plt.xlim(0, 1)

plt.subplot(222)
plt.plot(sim.trange(), sim.data[voltage][:, 0], 'r')
plt.xlim(0, 1)

plt.show()
