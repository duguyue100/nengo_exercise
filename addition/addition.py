"""Addition."""

from __future__ import print_function, absolute_import

import nengo

import matplotlib.pyplot as plt


model = nengo.Network(label="Addition")

with model:
    A = nengo.Ensemble(100, dimensions=1)
    B = nengo.Ensemble(100, dimensions=1)
    C = nengo.Ensemble(100, dimensions=1)

with model:
    input_a = nengo.Node(output=0.5)
    input_b = nengo.Node(output=0.3)

    nengo.Connection(input_a, A)
    nengo.Connection(input_b, B)

    nengo.Connection(A, C)
    nengo.Connection(B, C)

with model:
    input_a_probe = nengo.Probe(input_a)
    input_b_probe = nengo.Probe(input_b)
    A_probe = nengo.Probe(A, synapse=0.01)
    B_probe = nengo.Probe(B, synapse=0.01)
    C_probe = nengo.Probe(C, synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(5)

t = sim.trange()

plt.figure()
plt.plot(t, sim.data[A_probe], label="decoded ensemble A")
plt.plot(t, sim.data[B_probe], label="decoded ensemble B")
plt.plot(t, sim.data[C_probe], label="decoded ensemble C")
plt.plot(t, sim.data[input_a_probe], label="input A", color="k",
         linewidth=2.0)
plt.plot(t, sim.data[input_b_probe], label="input B", color="0.75",
         linewidth=2.0)

plt.legend()
plt.show()
