import numpy as np

temps = np.random.normal(30, 5, (365,))  
print("Average Temperature:", np.mean(temps))
print("Hottest Day:", np.max(temps))
print("Coldest Day:", np.min(temps))