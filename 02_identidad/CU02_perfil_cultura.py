#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CU02_perfil_cultura.py
Taller 05 · SI-886 · Planeamiento Estratégico de TI
Diagnóstico de Cultura Organizacional — Competing Values Framework

Este script:
  1. Lee las respuestas del instrumento CVF desde datos/encuesta_cultura.csv
  2. Valida que A + B + C + D = 100 en cada bloque (actual y deseado)
  3. Calcula el perfil cultural actual y deseado (general y por área)
  4. Calcula las brechas (Deseado − Actual)
  5. Identifica cultura dominante y cultura deseada
  6. Genera el gráfico de radar comparativo
  7. Imprime los resultados por consola y guarda evidencias

Requisitos: Python >= 3.11, pandas, matplotlib, numpy
Instalación: python -m pip install pandas matplotlib numpy
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend sin GUI para servidores y CI
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

# ────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ────────────────────────────────────────────────────────────────────────────

TIPOS = ["A", "B", "C", "D"]
NOMBRES_TIPO = {
    "A": "Clan (A)",
    "B": "Adhocracia (B)",
    "C": "Mercado (C)",
    "D": "Jerarquía (D)",
}
COLORES = {
    "A": "#3b82f6",   # azul
    "B": "#f59e0b",   # ámbar
    "C": "#ef4444",   # rojo
    "D": "#10b981",   # verde
}
COLOR_ACTUAL = "#2563eb"
COLOR_DESEADO = "#f97316"

DIMENSIONES_ORDEN = [
    "Caracteristicas dominantes",
    "Liderazgo",
    "Gestion del personal",
    "Cohesion",
    "Enfasis estrategico",
    "Criterio de exito",
]

# Rutas relativas al directorio raíz del proyecto
SCRIPT_DIR = Path(__file__).resolve().parent
RAIZ = SCRIPT_DIR.parent
CSV_PATH = RAIZ / "datos" / "encuesta_cultura.csv"
SALIDA_DIR = RAIZ / "docs" / "evidencias" / "S05" / "salidas"
RADAR_PATH = SALIDA_DIR / "CU_perfil_cultura.png"
PERFIL_CSV = SALIDA_DIR / "CU02_perfil_cultura.csv"


# ────────────────────────────────────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ────────────────────────────────────────────────────────────────────────────

def cargar_datos(ruta: Path) -> pd.DataFrame:
    """Lee el CSV de respuestas y verifica columnas mínimas."""
    if not ruta.exists():
        print(f"[ERROR] No se encontró el archivo: {ruta}")
        sys.exit(1)

    df = pd.read_csv(ruta)
    cols_requeridas = [
        "respondiente", "area", "dimension",
        "A_actual", "B_actual", "C_actual", "D_actual",
        "A_deseado", "B_deseado", "C_deseado", "D_deseado",
    ]
    faltantes = [c for c in cols_requeridas if c not in df.columns]
    if faltantes:
        print(f"[ERROR] Columnas faltantes en el CSV: {faltantes}")
        sys.exit(1)
    return df


def validar_sumas(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Verifica que A+B+C+D = 100 para actual y deseado.
    Retorna (df_válido, df_inválido).
    """
    cols_actual = ["A_actual", "B_actual", "C_actual", "D_actual"]
    cols_deseado = ["A_deseado", "B_deseado", "C_deseado", "D_deseado"]

    suma_actual = df[cols_actual].sum(axis=1)
    suma_deseado = df[cols_deseado].sum(axis=1)

    mask_valido = (suma_actual == 100) & (suma_deseado == 100)

    df_valido = df[mask_valido].copy()
    df_invalido = df[~mask_valido].copy()

    return df_valido, df_invalido


def calcular_perfil_general(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula el perfil promedio general (actual y deseado)."""
    resultados = []
    for t in TIPOS:
        actual = df[f"{t}_actual"].mean()
        deseado = df[f"{t}_deseado"].mean()
        brecha = deseado - actual
        resultados.append({
            "Tipo cultural": NOMBRES_TIPO[t],
            "Actual": round(actual, 2),
            "Deseado": round(deseado, 2),
            "Brecha": round(brecha, 2),
        })
    return pd.DataFrame(resultados)


def calcular_perfil_por_dimension(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula el perfil promedio por dimensión."""
    resultados = []
    for dim in DIMENSIONES_ORDEN:
        sub = df[df["dimension"] == dim]
        if sub.empty:
            continue
        fila = {"Dimensión": dim}
        for t in TIPOS:
            fila[f"{t}_actual"] = round(sub[f"{t}_actual"].mean(), 2)
            fila[f"{t}_deseado"] = round(sub[f"{t}_deseado"].mean(), 2)
        resultados.append(fila)
    return pd.DataFrame(resultados)


def calcular_perfil_por_area(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula el perfil actual promedio por área."""
    resultados = []
    for area in sorted(df["area"].unique()):
        sub = df[df["area"] == area]
        fila = {"Area": area}
        for t in TIPOS:
            fila[f"{NOMBRES_TIPO[t]} actual"] = round(sub[f"{t}_actual"].mean(), 2)
        resultados.append(fila)
    return pd.DataFrame(resultados)


def identificar_dominante(perfil: pd.DataFrame) -> tuple[str, str]:
    """Identifica cultura dominante actual y deseada."""
    idx_actual = perfil["Actual"].idxmax()
    idx_deseado = perfil["Deseado"].idxmax()
    return perfil.loc[idx_actual, "Tipo cultural"], perfil.loc[idx_deseado, "Tipo cultural"]


def generar_radar(perfil: pd.DataFrame, ruta_salida: Path):
    """
    Genera un gráfico de radar profesional comparando
    el perfil actual con el deseado.
    """
    categorias = [NOMBRES_TIPO[t] for t in TIPOS]
    N = len(categorias)

    actual = perfil["Actual"].values.tolist()
    deseado = perfil["Deseado"].values.tolist()

    # Cerrar el polígono
    actual += actual[:1]
    deseado += deseado[:1]

    angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    # Grilla y ejes
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)

    # Líneas de la grilla
    ax.yaxis.grid(True, color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.xaxis.grid(True, color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.spines["polar"].set_color("#475569")

    # Etiquetas angulares
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias, fontsize=12, fontweight="bold", color="#e2e8f0")

    # Límites radiales
    max_val = max(max(actual), max(deseado))
    ax.set_ylim(0, max_val + 10)
    ax.set_yticks(range(0, int(max_val) + 15, 10))
    ax.set_yticklabels(
        [str(v) for v in range(0, int(max_val) + 15, 10)],
        fontsize=8, color="#94a3b8"
    )

    # Perfil actual
    ax.plot(angulos, actual, "o-", linewidth=2.5, color=COLOR_ACTUAL,
            label="Actual", markersize=7, zorder=3)
    ax.fill(angulos, actual, alpha=0.15, color=COLOR_ACTUAL)

    # Perfil deseado
    ax.plot(angulos, deseado, "s--", linewidth=2.5, color=COLOR_DESEADO,
            label="Deseado", markersize=7, zorder=3)
    ax.fill(angulos, deseado, alpha=0.15, color=COLOR_DESEADO)

    # Valores sobre los puntos
    for i in range(N):
        ax.annotate(f"{actual[i]:.1f}",
                     (angulos[i], actual[i]),
                     textcoords="offset points", xytext=(8, 8),
                     fontsize=9, color=COLOR_ACTUAL, fontweight="bold")
        ax.annotate(f"{deseado[i]:.1f}",
                     (angulos[i], deseado[i]),
                     textcoords="offset points", xytext=(-8, -14),
                     fontsize=9, color=COLOR_DESEADO, fontweight="bold")

    # Título y leyenda
    ax.set_title(
        "Perfil Cultural — Competing Values Framework\nActual vs. Deseado",
        fontsize=16, fontweight="bold", color="#f8fafc",
        pad=30
    )
    legend = ax.legend(
        loc="upper right", bbox_to_anchor=(1.25, 1.12),
        fontsize=11, frameon=True, fancybox=True,
        facecolor="#1e293b", edgecolor="#475569",
        labelcolor="#e2e8f0"
    )

    # Guardar
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta_salida, dpi=200, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"  [OK] Grafico de radar guardado en: {ruta_salida}")


def generar_radar_por_area(df: pd.DataFrame, ruta_dir: Path):
    """
    Genera un gráfico de radar comparativo por área (solo perfil actual).
    """
    areas = sorted(df["area"].unique())
    N = len(TIPOS)
    categorias = [NOMBRES_TIPO[t] for t in TIPOS]

    angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angulos += angulos[:1]

    colores_area = {
        "Administracion": "#8b5cf6",
        "Ventas": "#06b6d4",
        "TI": "#f43f5e",
    }

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)

    ax.yaxis.grid(True, color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.xaxis.grid(True, color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.spines["polar"].set_color("#475569")

    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias, fontsize=12, fontweight="bold", color="#e2e8f0")

    max_val = 0
    for area in areas:
        sub = df[df["area"] == area]
        valores = [round(sub[f"{t}_actual"].mean(), 2) for t in TIPOS]
        max_val = max(max_val, max(valores))
        valores += valores[:1]
        color = colores_area.get(area, "#ffffff")
        ax.plot(angulos, valores, "o-", linewidth=2.5, color=color,
                label=area, markersize=7, zorder=3)
        ax.fill(angulos, valores, alpha=0.10, color=color)

    ax.set_ylim(0, max_val + 10)
    ax.set_yticks(range(0, int(max_val) + 15, 10))
    ax.set_yticklabels(
        [str(v) for v in range(0, int(max_val) + 15, 10)],
        fontsize=8, color="#94a3b8"
    )

    ax.set_title(
        "Perfil Cultural por Area - Estado Actual",
        fontsize=16, fontweight="bold", color="#f8fafc", pad=30
    )
    legend = ax.legend(
        loc="upper right", bbox_to_anchor=(1.25, 1.12),
        fontsize=11, frameon=True, fancybox=True,
        facecolor="#1e293b", edgecolor="#475569",
        labelcolor="#e2e8f0"
    )

    ruta_salida = ruta_dir / "CU_perfil_cultura_por_area.png"
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta_salida, dpi=200, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"  [OK] Grafico por area guardado en: {ruta_salida}")


# ────────────────────────────────────────────────────────────────────────────
# EJECUCIÓN PRINCIPAL
# ────────────────────────────────────────────────────────────────────────────

def main():
    separador = "=" * 72

    print(separador)
    print("  TALLER 05 · SI-886 · Diagnóstico de Cultura Organizacional")
    print("  Competing Values Framework — Cálculo de Perfiles y Brechas")
    print(separador)
    print()

    # ── 1. Carga ──
    print("1. Cargando datos...")
    df = cargar_datos(CSV_PATH)
    n_respondientes = df["respondiente"].nunique()
    n_areas = df["area"].nunique()
    n_filas = len(df)
    print(f"   Archivo: {CSV_PATH}")
    print(f"   Respondientes: {n_respondientes}")
    print(f"   Áreas: {n_areas} ({', '.join(sorted(df['area'].unique()))})")
    print(f"   Registros: {n_filas}")
    print()

    # ── 2. Validación ──
    print("2. Control de calidad (A + B + C + D = 100)...")
    df_valido, df_invalido = validar_sumas(df)
    n_bloques_validos = len(df_valido)
    n_bloques_invalidos = len(df_invalido)
    print(f"   Bloques válidos:   {n_bloques_validos}")
    print(f"   Bloques inválidos: {n_bloques_invalidos}")
    if n_bloques_invalidos > 0:
        print("   [!] Bloques excluidos del calculo:")
        for _, row in df_invalido.iterrows():
            print(f"      - {row['respondiente']} / {row['dimension']}")
    else:
        print("   [OK] Todas las respuestas cumplen la regla de validez.")
    print()

    # ── 3. Perfil general ──
    print("3. Perfil cultural general...")
    perfil = calcular_perfil_general(df_valido)
    print(perfil.to_string(index=False))
    print()

    dominante_actual, dominante_deseado = identificar_dominante(perfil)
    print(f"   -> Cultura dominante actual:  {dominante_actual}")
    print(f"   -> Cultura dominante deseada: {dominante_deseado}")

    mayor_brecha = perfil.loc[perfil["Brecha"].abs().idxmax()]
    signo = "+" if mayor_brecha["Brecha"] > 0 else ""
    print(f"   -> Mayor brecha: {mayor_brecha['Tipo cultural']} "
          f"({signo}{mayor_brecha['Brecha']})")
    print()

    # ── 4. Perfil por dimensión ──
    print("4. Perfil por dimension...")
    perfil_dim = calcular_perfil_por_dimension(df_valido)
    print(perfil_dim.to_string(index=False))
    print()

    # ── 5. Perfil por área ──
    print("5. Perfil cultural por area (estado actual)...")
    perfil_area = calcular_perfil_por_area(df_valido)
    print(perfil_area.to_string(index=False))
    print()

    # -- 6. Analisis de congruencia --
    print("6. Analisis de congruencia...")
    for _, row in perfil_area.iterrows():
        area = row["Area"]
        vals = {t: row[f"{NOMBRES_TIPO[t]} actual"] for t in TIPOS}
        dom = max(vals, key=vals.get)
        print(f"   {area}: dominante -> {NOMBRES_TIPO[dom]} ({vals[dom]})")
    print()

    # -- 7. Graficos --
    print("7. Generando graficos de radar...")
    SALIDA_DIR.mkdir(parents=True, exist_ok=True)
    generar_radar(perfil, RADAR_PATH)
    generar_radar_por_area(df_valido, SALIDA_DIR)
    print()

    # -- 8. Guardar perfil como CSV --
    print("8. Guardando perfil consolidado como CSV...")
    perfil.to_csv(PERFIL_CSV, index=False, encoding="utf-8-sig")
    print(f"   [OK] Perfil guardado en: {PERFIL_CSV}")
    print()

    # -- 9. Resumen --
    print(separador)
    print("  RESUMEN DE EJECUCION")
    print(separador)
    print(f"  Respondientes procesados: {n_respondientes}")
    print(f"  Bloques validos:          {n_bloques_validos}")
    print(f"  Bloques invalidos:        {n_bloques_invalidos}")
    print(f"  Cultura dominante actual: {dominante_actual}")
    print(f"  Cultura deseada:          {dominante_deseado}")
    print(f"  Mayor brecha:             {mayor_brecha['Tipo cultural']} "
          f"({signo}{mayor_brecha['Brecha']})")
    print(f"  Radar general:            {RADAR_PATH}")
    print(f"  Radar por area:           {SALIDA_DIR / 'CU_perfil_cultura_por_area.png'}")
    print(f"  Perfil CSV:               {PERFIL_CSV}")
    print(separador)
    print()
    print("  Ejecucion completada exitosamente. [OK]")
    print()


if __name__ == "__main__":
    main()
