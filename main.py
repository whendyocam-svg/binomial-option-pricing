from binomial_model import europea_b, americana_b
from black_scholes import black_scholes
import numpy as np


S0 = float(input("Precio Spot (S_0): "))
K = float(input("Precio de ejercicio(K): "))
T = float(input("Tiempo en meses: "))
r = float(input("Tasa libre de riesgo: "))
tipo = input("call o put: ").lower()
ops = input("americana o europea: ").lower()
N = int(input("Número de pasos: "))
sigma = float(input("Volatilidad: "))

T = T / 12
dt = T / N

u = np.exp(sigma * np.sqrt(dt))
d = 1 / u
p = (np.exp(r * dt) - d) / (u - d)

# MODELO BINOMIAL
if ops == "europea":
    precio = europea_b(S0, K, r, N, u, d, p, tipo)
else:
    precio = americana_b(S0, K, r, N, u, d, p, tipo)

print("\nPrecio Binomial:", precio)

# BLACK-SCHOLES
precio_bs = black_scholes(S0, K, T, r, sigma, tipo)
print("Precio Black-Scholes:", precio_bs)
