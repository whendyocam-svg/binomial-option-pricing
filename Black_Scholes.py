#NOMBRE DEL CÓDIGO: MÉTODO_BS
#MÉTODO BLACK_SCHOLES CON PRUEBA DE PARIDAD PUT-CALL

import numpy as np
from numpy import*
from scipy.stats import norm
from math import exp,log

#Solicitamos al usuario los datos
tipo = input('Tipo de opción: call(compra) o Put(venta).Ingrese call o put . ')
spot = float(input('Precio Spot (S_0):'))
strik = float(input('Precio de ejercicio (k,Strik):'))
meses = float(input('Duración en meses:'))
r = float(input('Tasa Libre de Riesgo: '))
print('TLR =', r * 100, '%')
sigma = float(input('Volatilidad anual, sigma: '))
print('Volatilidad =', sigma * 100, '%')

T = meses / 12
#Definimos la función para BS
def blackScholes(r, spot, strik, T, sigma):

    d1 = (np.log(spot / strik) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    option1 = spot * norm.cdf(d1, 0, 1) - strik * np.exp(-r * T) * norm.cdf(d2, 0, 1)
    option2 = strik * np.exp(-r * T) * norm.cdf(-d2, 0, 1) - spot * norm.cdf(-d1, 0, 1)

    if tipo == "call":
        print("Valor del CALL europeo por Black-Scholes", option1)
        return option1
    else:
        print("Valor del PUT europeo por Black-Scholes", option2)
        return option2

# Llamamos a la función blackScholes para obtener los precios de call o put
precio_opcion = blackScholes(r,spot,strik,T,sigma)

# Verificación de la paridad PUT-CALL
def paridad_p_c(tipo, precio_opcion, spot, strik, r, T):
    if tipo == 'call':
        precio2 = precio_opcion + strik * np.exp(-r * T) - spot
        a= precio_opcion + strik * np.exp(-r * T)
        b= precio2+ spot
        print(f"Igualdad de la paridad Put-Call: {precio_opcion} + {strik * np.exp(-r * T)} = {precio2} + {spot}")
        print("Se cumple:",a,"=",b)
    elif tipo == 'put':
        # Calcula el valor del CALL utilizando la paridad Put-Call
        precio1 = precio_opcion - strik * np.exp(-r * T) + spot
        f= precio1 + strik * np.exp(-r * T)
        g= precio_opcion + spot
        print(f"Igualdad de la paridad Put-Call: {precio1} + {strik * np.exp(-r * T)} = {precio_opcion} + {spot}")
        print("Se cumple:",f,"=",g)

# Llamamos a la función para verificar la paridad Put-Call
paridad_p_c(tipo, precio_opcion, spot, strik, r, T)

