#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyDatalog import pyDatalog

# Utilizamos create_terms para declarar variables y predicados
pyDatalog.create_terms('X, Y, Y1, Y2, DX, DY')
pyDatalog.create_terms('PosicionPelota, PosicionRaqueta, DireccionPelota')
pyDatalog.create_terms('MoverArriba, MoverAbajo, Quedarse, GolpeaPelota, PelotaEnZonaRaqueta')

# Configuración del juego
ANCHO_TABLERO = 10
POSICION_X_RAQUETA = 10  # Raqueta en el extremo derecho

# Hechos iniciales - usamos el operador + para aserciones (original API)
+PosicionPelota(5, 3)  # La pelota está en la posición (5, 3)
+PosicionRaqueta(3)    # La raqueta está alineada en y = 3
+DireccionPelota(1, -1) # Movimiento en diagonal
# Reglas lógicas
# Regla para determinar si la pelota está en la zona donde puede ser golpeada por la raqueta
# Usando comparación pyDatalog
PelotaEnZonaRaqueta(X, Y) <= PosicionPelota(X, Y) & (X == POSICION_X_RAQUETA)

# Reglas para mover la raqueta
MoverArriba(Y1, Y2) <= PosicionPelota(X, Y1) & PosicionRaqueta(Y2) & (Y1 > Y2)
MoverAbajo(Y1, Y2) <= PosicionPelota(X, Y1) & PosicionRaqueta(Y2) & (Y1 < Y2)
Quedarse(Y) <= PosicionPelota(X, Y) & PosicionRaqueta(Y)

# Regla para determinar si la pelota es golpeada por la raqueta
GolpeaPelota(X, Y) <= PosicionPelota(X, Y) & PosicionRaqueta(Y) & (X == POSICION_X_RAQUETA)
# Consultas - usamos el método correcto para obtener resultados
print("\n--- Estado Actual del Juego ---")
# Agregar comprobaciones para valores None
pelota_pos_result = pyDatalog.ask('PosicionPelota(X, Y)')
print("Posición de la pelota:", pelota_pos_result.answers if pelota_pos_result else "No disponible")

raqueta_pos_result = pyDatalog.ask('PosicionRaqueta(Y)')
print("Posición de la raqueta:", raqueta_pos_result.answers if raqueta_pos_result else "No disponible")

direccion_result = pyDatalog.ask('DireccionPelota(DX, DY)')
print("Dirección de la pelota:", direccion_result.answers if direccion_result else "No disponible")

# Consulta si la pelota está en la zona de la raqueta
pelota_en_zona_result = pyDatalog.ask('PelotaEnZonaRaqueta(X, Y)')
pelota_en_zona = pelota_en_zona_result.answers if pelota_en_zona_result else None
print("\n--- Análisis de la Pelota ---")
if pelota_en_zona:
    print("¿Pelota en zona de raqueta?: Sí - En posición ({}, {})".format(
        pelota_en_zona[0][0], pelota_en_zona[0][1]))
else:
    print("¿Pelota en zona de raqueta?: No - La pelota no está en la zona de la raqueta")

# Consultas sobre el movimiento de la raqueta
print("\n--- Acciones Recomendadas ---")
arriba_query_result = pyDatalog.ask('MoverArriba(Y1, Y2)')
arriba_result = arriba_query_result.answers if arriba_query_result else None
if arriba_result:
    print("Acción: Mover Arriba. La pelota está en y={} y la raqueta en y={}".format(
        arriba_result[0][0], arriba_result[0][1]))

abajo_query_result = pyDatalog.ask('MoverAbajo(Y1, Y2)')
abajo_result = abajo_query_result.answers if abajo_query_result else None
if abajo_result:
    print("Acción: Mover Abajo. La pelota está en y={} y la raqueta en y={}".format(
        abajo_result[0][0], abajo_result[0][1]))

quedarse_query_result = pyDatalog.ask('Quedarse(Y)')
quedarse_result = quedarse_query_result.answers if quedarse_query_result else None
if quedarse_result:
    print("Acción: Quedarse. La pelota y la raqueta están alineadas en y={}".format(
        quedarse_result[0][0]))

# Consulta si la pelota es golpeada
golpea_query_result = pyDatalog.ask('GolpeaPelota(X, Y)')
golpea = golpea_query_result.answers if golpea_query_result else None
print("\n--- Resultado del Golpe ---")
if golpea:
    print("¡Golpe exitoso! La pelota en ({}, {}) fue golpeada por la raqueta en y={}".format(
        golpea[0][0], golpea[0][1], golpea[0][1]))
else:
    print("No hay golpe. La pelota no está en posición para ser golpeada por la raqueta.")
