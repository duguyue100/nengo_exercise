"""Make a subnetwork."""

from __future__ import print_function, absolute_import

import numpy as np

import nengo
from nengo.dists import Choice
from nengo.processes import Piecewise

import matplotlib.pyplot as plt


def Product(neuron_per_dimension, input_magnitude):
    model = nengo.Network(label="Product")
    with model:

        model.A = nengo.Node(output=None, size_in=1)
        model.B = nengo.Node(output=None, size_in=1)

        model.combined = nengo.Ensemble(
            neuron_per_dimension*2,
            dimensions=2,
            radius=np.sqrt(input_magnitude**2+input_magnitude**2),
            encoders=Choice([[1, 1], [-1, 1], [1, -1], [-1, -1]]))

        model.prod = nengo.Ensemble(
            neuron_per_dimension, dimensions=1, radius=input_magnitude*2)

        nengo.Connection(model.A, model.combined[0], synapse=None)
        nengo.Connection(model.B, model.combined[1], synapse=None)

        def product(x):
            return x[0] * x[1]

        nengo.Connection(model.combined, model.prod, function=product)

    return model


model = nengo.Network(label="Multiplication")

with model:
    input_A = nengo.Node(Piecewise({0: 0, 2.5: 10, 4: -10}))
    input_B = nengo.Node(Piecewise({0: 10, 1.5: 2, 3: 0, 4.5: 2}))

    A = nengo.Ensemble(100, dimensions=1, radius=10)
    B = nengo.Ensemble(100, dimensions=1, radius=10)

    prod = Product(100, input_magnitude=10)

    nengo.Connection(input_A, A)
    nengo.Connection(input_B, B)
    nengo.Connection(A, prod.A)
    nengo.Connection(B, prod.B)

    inputA_probe = nengo.Probe(input_A)
    inputB_probe = nengo.Probe(input_B)
    A_probe = nengo.Probe(A, synapse=0.01)
    B_probe = nengo.Probe(B, synapse=0.01)
    combined_prob = nengo.Probe(prod.combined, synapse=0.01)
    prod_probe = nengo.Probe(prod.prod, synapse=0.01)

    correct_ans = Piecewise({0: 0, 1.5: 0, 2.5: 20, 3: 0, 4: 0, 4.5: -20})

with nengo.Simulator(model) as sim:
    sim.run(5)

plt.figure()
plt.plot(sim.trange(), sim.data[A_probe], label="decoded A")
plt.plot(sim.trange(), sim.data[B_probe], label="decoded B")
plt.plot(sim.trange(), sim.data[prod_probe], label="decoded product")
plt.plot(sim.trange(), correct_ans.run(sim.time, dt=sim.dt),
         c="k", label="Actual product")
plt.legend()

plt.show()
