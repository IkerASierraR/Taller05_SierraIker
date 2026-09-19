#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_datos.py
Genera datos de encuesta CVF con variacion realista
para Distribuidora Comercial del Sur S.A.C. (DICOSUR), Tacna.

Los datos simulan respuestas individuales variadas que producen perfiles
coherentes con una empresa de distribucion y logistica:
  - Administracion: orientacion a Jerarquia (D)
  - Ventas/Comercial: orientacion a Mercado (C)
  - TI: orientacion a Adhocracia (B)
"""

import numpy as np
import csv
from pathlib import Path

np.random.seed(42)

DIMENSIONES = [
    "Caracteristicas dominantes",
    "Liderazgo",
    "Gestion del personal",
    "Cohesion",
    "Enfasis estrategico",
    "Criterio de exito",
]

# Ajustes por dimension para los valores deseados [A, B, C, D]
AJUSTE_DIM = [
    [ 0,  0,  0,  0],   # Dim 1: baseline
    [ 2,  0,  0, -2],   # Dim 2: mas clan en liderazgo
    [-3,  4,  2, -3],   # Dim 3: mucho mas adhocracia en gestion personal
    [-1,  0,  1,  0],   # Dim 4: baseline
    [ 0,  2,  0, -2],   # Dim 5: mas adhocracia en enfasis estrategico
    [ 4, -2, -2,  0],   # Dim 6: mas clan en criterio de exito
]

AREAS = {
    "Administracion": {
        "ids": [f"R{i:02d}" for i in range(1, 6)],
        "actual": [15, 12, 26, 47],
        "deseado": [22, 29, 27, 22],
        "ruido_act": 5,
        "ruido_des": 4,
    },
    "Ventas": {
        "ids": [f"R{i:02d}" for i in range(6, 11)],
        "actual": [14, 10, 54, 22],
        "deseado": [20, 30, 28, 22],
        "ruido_act": 6,
        "ruido_des": 4,
    },
    "TI": {
        "ids": [f"R{i:02d}" for i in range(11, 16)],
        "actual": [24, 35, 20, 21],
        "deseado": [22, 33, 26, 19],
        "ruido_act": 5,
        "ruido_des": 4,
    },
}


def generar_100(centro, ruido):
    """Genera 4 valores que suman exactamente 100, con variacion aleatoria."""
    raw = np.array(centro, dtype=float) + np.random.randint(-ruido, ruido + 1, size=4)
    raw = np.maximum(raw, 5)
    norm = np.round(raw * 100.0 / raw.sum()).astype(int)
    norm[np.argmax(norm)] += 100 - norm.sum()
    return norm.tolist()


def main():
    filas = []
    for area, cfg in AREAS.items():
        for rid in cfg["ids"]:
            for d, dim in enumerate(DIMENSIONES):
                actual = generar_100(cfg["actual"], cfg["ruido_act"])
                centro_des = [cfg["deseado"][i] + AJUSTE_DIM[d][i] for i in range(4)]
                deseado = generar_100(centro_des, cfg["ruido_des"])
                filas.append([rid, area, dim] + actual + deseado)

    ruta = Path(__file__).resolve().parent.parent / "datos" / "encuesta_cultura.csv"
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "respondiente", "area", "dimension",
            "A_actual", "B_actual", "C_actual", "D_actual",
            "A_deseado", "B_deseado", "C_deseado", "D_deseado",
        ])
        writer.writerows(filas)

    print(f"[OK] {len(filas)} registros generados -> {ruta}")

    # Verificar sumas
    errores = 0
    for fila in filas:
        s_act = sum(fila[3:7])
        s_des = sum(fila[7:11])
        if s_act != 100 or s_des != 100:
            errores += 1
            print(f"  [!] {fila[0]}/{fila[2]}: actual={s_act}, deseado={s_des}")
    if errores == 0:
        print(f"[OK] Todas las {len(filas)} filas suman 100 en actual y deseado.")
    else:
        print(f"[!] {errores} filas con error de suma.")


if __name__ == "__main__":
    main()
