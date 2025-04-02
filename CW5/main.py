#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:51:50 2021

@author: Rafał Biedrzycki
Kodu tego mogą używać moi studenci na ćwiczeniach
z przedmiotu Wstęp do Sztucznej Inteligencji.
Kod ten powstał aby przyspieszyć i ułatwić pracę studentów,
aby mogli skupić się na algorytmach sztucznej inteligencji.
Kod nie jest wzorem dobrej jakości programowania w Pythonie,
nie jest również wzorem programowania obiektowego, może zawierać błędy.

Nie ma obowiązku używania tego kodu.
"""

import numpy as np
import matplotlib.pyplot as plt

# ToDo tu prosze podac pierwsze cyfry numerow indeksow
p = [3, 3]

L_BOUND = -5
U_BOUND = 5
NEURONS = 1


def q(x):
    return np.sin(x * np.sqrt(p[0] + 1)) + np.cos(x * np.sqrt(p[1] + 1))


x = np.linspace(L_BOUND, U_BOUND, 100)
y = q(x)

np.random.seed(1)


# f logistyczna jako przykład sigmoidalej
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# pochodna fun. 'sigmoid'
def d_sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s * (1 - s)


# f. straty
def nloss(y_out, y):
    return (y_out - y) ** 2


# pochodna f. straty
def d_nloss(y_out, y):
    return 2 * (y_out - y)


class DlNet:
    def __init__(self, x, y, neurons=9):
        self.x = x
        self.y = y
        self.y_out = 0

        self.HIDDEN_L_SIZE = neurons
        self.LR = 0.003

        # CHANGED

        self.weights = np.random.randn(self.HIDDEN_L_SIZE, 1) * 0.1
        self.biases = np.zeros((self.HIDDEN_L_SIZE, 1))
        self.weights_out = np.random.randn(self.HIDDEN_L_SIZE) * 0.1
        self.biases_out = 0.0

        # END

    def forward(self, x):
        # CHANGED
        x = np.array([[x]])
        self.argument = np.dot(self.weights, x) + self.biases
        self.value = sigmoid(self.argument)

        self.y_out = np.dot(self.weights_out, self.value) + self.biases_out
        return self.y_out.item()
        # END

    def predict(self, x):
        # CHANGED
        return self.forward(x)
        # END

    def backward(self, x, y):
        # CHANGED
        gradient = d_nloss(self.y_out, y)

        dWeights_out = gradient * self.value
        dBiases_out = gradient

        dBiases = (gradient * self.weights_out).reshape(-1, 1) * d_sigmoid(self.argument)
        dWeights = dBiases * x

        self.weights_out -= self.LR * dWeights_out.flatten()
        self.biases_out -= self.LR * dBiases_out
        self.weights -= self.LR * dWeights
        self.biases -= self.LR * dBiases
        # END

    def train(self, x_set, y_set, iters):
        # CHANGED
        for i in range(1, iters + 1):
            loss_sum = 0
            for x, y in zip(x_set, y_set):
                self.forward(x)
                loss_sum += nloss(self.y_out, y)
                self.backward(x, y)
            if i % 100 == 0:
                print(i)
        # END


def mse(y, yh):
    return np.mean((y - yh) ** 2)



nn = DlNet(x, y, neurons=NEURONS)
nn.train(x, y, 100)

yh = [nn.predict(point) for point in x]

mse_val = mse(y, yh)
print(mse_val)



fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.plot(x, y, 'r', label='Exact function')
plt.plot(x, yh, 'b', label=f'Predicted function (neurons={NEURONS})')
plt.legend(loc='upper left', fontsize = 8)
plt.xlim(L_BOUND-1, U_BOUND+1)
plt.ylim(-2.5, 2.5)

plt.title(f"NN Approximation for {NEURONS} neurons (MSE={mse_val:.5f})", fontsize=10)

plt.savefig('plot.png')
plt.show()
