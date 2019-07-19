"""Multiplication."""

from __future__ import absolute_import, print_function

import nengo
from nengo.dists import Choice
from nengo.processes import Piecewise

import matplotlib.pyplot as plt

# model
model = nengo.Network(label="Multiplication")

with model:
    A = nengo.Ensemble(100, dimensions=1, radius=10)
    B = nengo.Ensemble(100, dimensions=1, radius=10)

    combined = nengo.Ensemble(
        220, dimensions=2, radius=15)

    prod = nengo.Ensemble(100, dimensions=1, radius=20)

combined.encoders = Choice([[1, 1], [-1, 1], [1, -1], [-1, -1]])

with model:
    input_A = nengo.Node(Piecewise({0: 0, 2.5: 10, 4: -10}))
    input_B = nengo.Node(Piecewise({0: 10, 1.5: 2, 3: 0, 4.5: 2}))

    correct_ans = Piecewise({0: 0, 1.5: 0, 2.5: 20, 3: 0, 4: 0, 4.5: -20})

with model:
    nengo.Connection(input_A, A)
    nengo.Connection(input_B, B)

    nengo.Connection(A, combined[0])
    nengo.Connection(B, combined[1])

    def product(x):
        return x[0] * x[1]

    nengo.Connection(combined, prod, function=product)

with model:
    inputA_probe = nengo.Probe(input_A)
    inputB_probe = nengo.Probe(input_B)

    A_probe = nengo.Probe(A, synapse=0.01)
    B_probe = nengo.Probe(B, synapse=0.01)

    combined_probe = nengo.Probe(combined, synapse=0.01)
    prod_probe = nengo.Probe(prod, synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(5)

plt.figure()
plt.plot(sim.trange(), sim.data[A_probe], label="Decoded A")
plt.plot(sim.trange(), sim.data[B_probe], label="Decoded B")
plt.plot(sim.trange(), sim.data[prod_probe], label="Decoded product")

plt.plot(sim.trange(), correct_ans.run(sim.time, dt=sim.dt),
         c="k", label="Actual product")
plt.legend(loc="best")
plt.show()
