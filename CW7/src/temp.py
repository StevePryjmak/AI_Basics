import numpy as np

# Definicja przestrzeni probabilistycznej
omega = np.arange(1, 11)

# Definicja zmiennych losowych X i Y
X = omega % 3
Y = (omega ** 2) % 3

# Obliczenie wartości Z i T
Z = X + 2 * Y - 3
T = Y - X - 1

# Obliczenie średnich
mean_Z = np.mean(Z)
mean_T = np.mean(T)

# Obliczenie kowariancji
cov_ZT = np.mean((Z - mean_Z) * (T - mean_T))

# Wyświetlenie wyników
print("Wartości X:", X)
print("Wartości Y:", Y)
print("Wartości Z:", Z)
print("Wartości T:", T)
print("Średnia Z:", mean_Z)
print("Średnia T:", mean_T)
print("Kowariancja (Z, T):", cov_ZT)