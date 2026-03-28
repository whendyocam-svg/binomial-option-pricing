import numpy as np
from scipy.stats import norm

# Funciones

def europea_b(S0, K, r, N, u, d, p, tipo, T):
    dt = T / N
    disc = np.exp(-r * dt)
    valores = []
    for i in range(N+1):
        ST = S0 * (u**i) * (d**(N-i))
        if tipo == "call":
            valores.append(max(0, ST - K))
        else:
            valores.append(max(0, K - ST))
    for j in range(N-1, -1, -1):
        for i in range(j+1):
            valores[i] = disc * (p * valores[i+1] + (1-p) * valores[i])
    return valores[0]
def americana_b(S0, K, r, N, u, d, p, tipo, T):
    dt = T / N
    disc = np.exp(-r * dt)
    valores = np.zeros((N+1, N+1))
    for i in range(N+1):
        ST = S0 * (u**i) * (d**(N-i))
        if tipo == "call":
            valores[N, i] = max(0, ST - K)
        else:
            valores[N, i] = max(0, K - ST)
    for j in range(N-1, -1, -1):
        for i in range(j+1):
            ST = S0 * (u**i) * (d**(j-i))
            if tipo == "call":
                ejercicio = max(0, ST - K)
            else:
                ejercicio = max(0, K - ST)
            mantener = disc * (p * valores[j+1, i+1] + (1-p) * valores[j+1, i])
            valores[j, i] = max(ejercicio, mantener)
    return valores[0, 0]

def black_scholes(S0, K, T, r, sigma, tipo):
    d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if tipo == "call":
        return S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        return K*np.exp(-r*T)*norm.cdf(-d2) - S0*norm.cdf(-d1)

# Programa principal


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
    precio = europea_b(S0, K, r, N, u, d, p, tipo, T)
else:
    precio = americana_b(S0, K, r, N, u, d, p, tipo, T)

print("\nPrecio Binomial:", precio)

# BLACK-SCHOLES
precio_bs = black_scholes(S0, K, T, r, sigma, tipo)
print("Precio Black-Scholes:", precio_bs)
