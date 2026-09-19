# Procedimiento de Generación y Presentación del Informe Oficial

**Asignatura:** SI-886 · Planeamiento Estratégico de TI  
**Semana:** 05 — Diagnóstico de Cultura con el Competing Values Framework  
**Caso:** Distribuidora Comercial del Sur S.A.C. (DICOSUR)  
**Estudiante:** Iker Alberto Sierra Ruiz  

---

## 1. Inventario de Entregables en esta Carpeta (`informeasdf/`)

| Archivo | Tipo | Descripción |
|---|---|---|
| [`SI886-S05-TALLER-Grupo01.pdf`](SI886-S05-TALLER-Grupo01.pdf) | **Informe Principal** | Documento oficial de 12 páginas con carátula UPT, índice, secciones 1 a 6 y evidencias enlazadas. |
| [`anexo_A_instrumento_cvf.pdf`](anexo_A_instrumento_cvf.pdf) | **Anexo A** | Instrumento de diagnóstico CVF completo con 6 dimensiones e instrucciones ipsativas de 100 puntos. |
| [`anexo_B_resultados_cultura.xlsx`](anexo_B_resultados_cultura.xlsx) | **Anexo B** | Libro de Excel con datos brutos, control de calidad, perfiles consolidados, por área y brechas. |
| [`anexo_C_perfil_cultura.png`](anexo_C_perfil_cultura.png) | **Anexo C** | Gráfico de radar comparativo de alta resolución (Perfil general y congruencia departamental). |
| [`anexo_D_supuestos_basicos.xlsx`](anexo_D_supuestos_basicos.xlsx) | **Anexo D** | Matriz de artefactos, fuentes, valores y supuestos básicos de Schein con análisis de coincidencia. |
| [`anexo_E_secciones_2_3_2_4.pdf`](anexo_E_secciones_2_3_2_4.pdf) | **Anexo E** | Texto formal de las Secciones 2.3 (Valores) y 2.4 (Cultura) listo para integrarse al PETI master. |
| [`generar_informe.py`](generar_informe.py) | **Script de Compilación** | Código fuente Python para regenerar el informe PDF principal automáticamente. |

---

## 2. Metodología y Paso a Paso Procedimental

### Paso A — Aplicación del Instrumento CVF
- Se utilizó el marco de Cameron & Quinn (2011) con 6 dimensiones evaluadas en escala forzada (ipsativa) de 100 puntos.
- Población: 48 colaboradores. Muestra evaluada: 15 respondientes (31.25% de la empresa, superando el 30% requerido).
- Cobertura de áreas: Administración (5), Comercial/Ventas (5), TI (5).

### Paso B — Control de Calidad y Cálculo de Perfiles
- Validación programática mediante `02_identidad/CU02_perfil_cultura.py`:
  - Se verificó que `A + B + C + D = 100` en cada respondiente y dimensión tanto en situación actual como deseada.
  - Resultado: 90 bloques evaluados, 90 válidos, 0 inválidos (100.0% de calidad).
- Resultados obtenidos:
  - **Cultura Dominante Actual:** Mercado (C) = 33.21 pts (seguido de Jerarquía D = 29.81 pts).
  - **Cultura Dominante Deseada:** Adhocracia (B) = 31.37 pts.
  - **Brecha de Transformación Crítica:** Adhocracia = +11.41 pts.
  - **Mayor Reducción:** Jerarquía = −10.17 pts.

### Paso C — Identificación de Supuestos Básicos (Modelo de Schein)
- No se formularon preguntas directas; se infirieron a partir de artefactos observables y registros documentales contrastados contra los valores formales.
- Se documentaron 5 artefactos con sus respectivas fuentes y fechas en `CU03_supuestos.csv` y `anexo_D_supuestos_basicos.xlsx`.
- Se detectaron 4 brechas valor-supuesto (concentración de decisiones, subreporte de errores, silos de datos, infraestructura obsoleta) y 1 congruencia (disciplina de reuniones).

### Paso D — Derivación de Implicancias para el PETI
- Cada brecha y hallazgo cultural fue traducido a riesgos concretos de adopción tecnológica y estrategias de gestión del cambio distribuidas en el PETI (Portafolio, Objetivos, Gobierno TI, Gobierno del Dato y Gestión del Cambio).

### Paso E — Formulación de Valores Conductuales
- Se superó la formulación meramente discursiva estableciendo para cada valor: qué conducta lo cumple, qué conducta lo viola, cuál es la consecuencia exigible ante el incumplimiento y a qué se renuncia al sostenerlo.
- Se aplicó un valor concreto (*Experimentar con control*) a una decisión tecnológica real (Plataforma de Gestión Documental).

---

## 3. Instrucciones para la Entrega en el Aula Virtual

1. **Archivo principal:** Subir el PDF [`SI886-S05-TALLER-Grupo01.pdf`](SI886-S05-TALLER-Grupo01.pdf) en la tarea «Taller · Semana 05».
2. **Archivos adjuntos/anexos:** Incluir los archivos `anexo_A_instrumento_cvf.pdf`, `anexo_B_resultados_cultura.xlsx`, `anexo_C_perfil_cultura.png`, `anexo_D_supuestos_basicos.xlsx` y `anexo_E_secciones_2_3_2_4.pdf`.
3. **Enlace a GitHub:** En la entrega y en el informe se incluye la URL del repositorio con el tag `taller-05`:
   `https://github.com/<organizacion>/<repositorio>/tree/taller-05`
