"""Integrator."""

from __future__ import print_function, absolute_import

import nengo
from nengo.processes import Piecewise

import matplotlib.pyplot as plt

# build model
model = nengo.Network(label="Integrator")

with model:
    A = nengo.Ensemble(100, dimensions=1)

with model:
    input = nengo.Node(
        Piecewise({
            0: 0,
            0.2: 1,
            1: 0,
            2: -2,
            3: 0,
            4: 1,
            5: 0}))

with model:
    tau = 0.1
    nengo.Connection(
        A, A, transform=[[1]],
        synapse=tau)

    nengo.Connection(
        input, A, transform=[[tau]], synapse=tau)

with model:
    input_probe = nengo.Probe(input)
    A_probe = nengo.Probe(A, synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(6)

plt.figure()
plt.plot(sim.trange(), sim.data[input_probe], label="input")
plt.plot(sim.trange(), sim.data[A_probe], "k", label="integrator output")
plt.legend()

plt.show()
