import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

S0 = float(input("Precio Spot (S_0): "))
K = float(input("Precio de ejercicio(K): "))
T = float(input("Tiempo de duración (T) en meses: "))
r = float(input("Tasa Libre de Riesgo (r): "))
tipo = input("Tipo de opción call o put. Ingrese call o put: ").lower()
ops = input("Tipo de opción americana o europea. Ingrese americana o europea: ").lower()
N = int(input("Número de pasos en el modelo binomial: "))
vol = input("¿Tiene el valor de la volatilidad? . Indique si o no: ").lower()

T1 = T / 12
dt = T1 / N

# PARÁMETROS

if vol == 'si':
    sigma = float(input("Volatilidad del activo (sigma): "))
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
else:
    u = float(input("Valor de u: "))
    d = float(input("Valor de d: "))
    sigma = np.log(u) / np.sqrt(dt)
    print("Valor de sigma calculado:", sigma)

p = (np.exp(r * dt) - d) / (u - d)
q = 1 - p
disc = np.exp(-r * dt)

# Validación básica
if not (0 <= p <= 1):
    raise ValueError("Probabilidad p fuera de rango (revisar parámetros)")

print("Valor de u:", u)
print("Valor de d:", d)
print("Valor de p:", p)
print("Valor de q:", q)


# FUNCIÓN EUROPEA

def europea_b(K, T1, S0, r, N, tipo):

    S = np.zeros((N + 1, N + 1))
    C = np.zeros((N + 1, N + 1))

    # Precios al vencimiento
    for j in range(N + 1):
        S[N, j] = S0 * u**j * d**(N - j)

        if tipo == 'put':
            C[N, j] = max(0, K - S[N, j])
        else:
            C[N, j] = max(0, S[N, j] - K)

    # Backward
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            S[i, j] = S0 * u**j * d**(i - j)
            C[i, j] = disc * (p * C[i + 1, j + 1] + q * C[i + 1, j])

    return C[0, 0], S, C


# FUNCIÓN AMERICANA

def americana_b(K, T1, S0, r, N, tipo):

    S = np.zeros((N + 1, N + 1))
    C = np.zeros((N + 1, N + 1))

    for j in range(N + 1):
        S[N, j] = S0 * u**j * d**(N - j)

        if tipo == 'put':
            C[N, j] = max(0, K - S[N, j])
        else:
            C[N, j] = max(0, S[N, j] - K)

    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            S[i, j] = S0 * u**j * d**(i - j)
            valor_esperado = disc * (p * C[i + 1, j + 1] + q * C[i + 1, j])

            if tipo == 'put':
                C[i, j] = max(valor_esperado, K - S[i, j])
            else:
                C[i, j] = max(valor_esperado, S[i, j] - K)

    return C[0, 0], S, C


# EJECUCIÓN

if ops == "europea":
    precio, S, C = europea_b(K, T1, S0, r, N, tipo)
else:
    precio, S, C = americana_b(K, T1, S0, r, N, tipo)

print("\nPrecio de la opción:", precio)
