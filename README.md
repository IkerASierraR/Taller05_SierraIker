# Taller 05 · Diagnóstico de Cultura Organizacional con Competing Values Framework (CVF)

**Asignatura:** SI-886 · Planeamiento Estratégico de TI  
**Ciclo y Semestre:** 2026-II · Semana 05  
**Estudiante:** Iker Alberto Sierra Ruiz  
**Docente:** Dr. Oscar Juan Jimenez Flores  
**Institución:** Universidad Privada de Tacna (UPT)  
**Organización Caso:** Distribuidora Comercial del Sur S.A.C. (DICOSUR)  

---

## 1. Resumen Ejecutivo del Diagnóstico

Este repositorio contiene la evidencia completa del **Diagnóstico de Cultura Organizacional** aplicado a la empresa **Distribuidora Comercial del Sur S.A.C. (DICOSUR)** (Tacna, 48 colaboradores) utilizando el **Competing Values Framework (CVF)** (Cameron & Quinn, 2011) y el modelo de tres niveles de Edgar Schein (artefactos, valores adoptados y supuestos básicos).

El diagnóstico sustenta las **Secciones 2.3 (Valores)** y **2.4 (Cultura)** del **Plan Estratégico de Tecnologías de Información (PETI)**.

### Resultados Clave del CVF

| Tipo Cultural | Estado Actual | Estado Deseado (5 años) | Brecha (Deseado − Actual) |
|---|---:|---:|---:|
| **Clan (A)** | 17.02 | 21.79 | **+4.77** |
| **Adhocracia (B)** | 19.96 | 31.37 | **+11.41** |
| **Mercado (C)** | 33.21 | 27.20 | **−6.01** |
| **Jerarquía (D)** | 29.81 | 19.64 | **−10.17** |

- **Cultura Dominante Actual:** **Mercado (C)** con 33.21 puntos, seguido de cerca por **Jerarquía (D)** con 29.81 puntos. Refleja una organización comercial de distribución altamente orientada a cuotas de venta y procedimientos formalizados.
- **Cultura Deseada:** **Adhocracia (B)** con 31.37 puntos.
- **Mayor Brecha de Transformación:** **Adhocracia (+11.41)**, indicando la urgencia de agilidad, innovación en canales digitales y autonomía en la gestión del cambio.
- **Mayor Reducción:** **Jerarquía (−10.17)**, requiriendo flexibilización de trámites y descentralización de aprobaciones.

### Congruencia Interna por Áreas
- **Administración y Finanzas:** Jerarquía dominante (D = 47.20).
- **Comercial / Ventas:** Mercado dominante (C = 54.13).
- **Tecnologías de Información:** Adhocracia dominante (B = 36.67).

---

## 2. Estructura del Repositorio

```
para github/
├── .gitignore
├── README.md
├── 02_identidad/
│   ├── CU01_instrumento.md          # Instrumento CVF (6 dimensiones × 4 tipos)
│   ├── CU02_perfil_cultura.py       # Script de validación, cálculo y generación de radar
│   ├── CU03_supuestos.csv           # 5 supuestos básicos con columna 'Fuente' y fechas
│   ├── CU04_implicancias_peti.md    # Matriz de riesgos, estrategias y secciones del PETI
│   ├── 2.3_valores.md               # Sección 2.3: Valores conductuales y decisión tecnológica
│   ├── 2.4_cultura.md               # Sección 2.4: Diagnóstico cultural consolidado
│   └── generar_datos.py             # Script de datos realistas para DICOSUR
├── datos/
│   └── encuesta_cultura.csv         # 90 bloques (15 respondientes × 6 dimensiones)
├── informe/
│   └── SI886-S05-TALLER-Grupo01.pdf # Informe oficial PDF con plantilla UPT (12 páginas)
└── docs/
    ├── PROCEDIMIENTO_INFORME.md     # Guía procedimental y checklist de entrega
    └── evidencias/
        └── S05/
            ├── anexo_A_instrumento_cvf.pdf        # Anexo A: Instrumento CVF oficial (PDF)
            ├── anexo_B_resultados_cultura.xlsx    # Anexo B: Respuestas, calidad y brechas (Excel)
            ├── anexo_C_perfil_cultura.png         # Anexo C: Gráficos de radar comparativos HD
            ├── anexo_D_supuestos_basicos.xlsx     # Anexo D: Matriz Schein de supuestos (Excel)
            ├── anexo_E_secciones_2_3_2_4.pdf      # Anexo E: Secciones PETI 2.3 y 2.4 (PDF)
            └── salidas/
                ├── CU02_perfil_cultura.csv        # Tabla consolidada de puntajes y brechas
                ├── CU_perfil_cultura.png          # Radar comparativo Actual vs. Deseado
                ├── CU_perfil_cultura_por_area.png # Radar de divergencias entre áreas
                └── salida_ejecucion.txt           # Log de control de calidad y verificación
```

---

## 3. Instrucciones de Replicación y Ejecución

### Requisitos
- Python 3.11+
- Paquetes requeridos: `pandas`, `matplotlib`, `numpy`

```bash
# 1. Instalar dependencias
python -m pip install pandas matplotlib numpy

# 2. Ejecutar análisis de cultura
python 02_identidad/CU02_perfil_cultura.py
```

### Control de Calidad Ejecutado
- Suma de respuestas: 100 puntos exactos en cada bloque.
- Bloques procesados: 90 válidos, 0 inválidos.
- Respondientes: 15 colaboradores (5 por cada área).

---

## 4. Supuestos Básicos y Brechas Culturales

Se identificaron 4 contradicciones entre los valores adoptados y los supuestos básicos reales:
1. **Autonomía declarada vs. Concentración de decisiones:** Ningún proyecto se aprueba sin firma del gerente general (Observación y entrevista).
2. **Mejora continua vs. Temor al reporte:** Solo 4 tickets de incidentes en 12 meses (Revisión documental ServiceDesk).
3. **Trabajo en equipo vs. Silos de datos:** Cada área mantiene hojas de cálculo propias de clientes (Observación en servidor de archivos).
4. **Excelencia/Innovación vs. Resistencia al cambio:** Servidor ERP en Windows Server 2012 R2 sin soporte (Inventario de activos).

---

## 5. Etiquetas de Versión (Git Tags)

El repositorio cuenta con los tags oficiales según los requerimientos del taller:
- `v0.5`: PETI v0.5 — Identidad estratégica completa (Secciones 2.3 y 2.4).
- `taller-05`: Taller 05 · SI886 (Evidencia procedimental evaluada).

```bash
# Para publicar en GitHub:
git remote add origin <URL-DEL-REPOSITORIO>
git branch -M master
git push -u origin master --tags
```
