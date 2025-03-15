import numpy as np

np.random.seed(0)
days = 365
initial_price = 100
returns = np.random.normal(0, 1, days)
prices = initial_price * np.cumprod(1 + returns / 100)

import matplotlib.pyplot as plt
plt.plot(prices)
plt.title("Simulated Stock Prices")
plt.show()