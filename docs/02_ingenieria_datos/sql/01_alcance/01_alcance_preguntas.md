# SQL-01: alcance y preguntas de consulta

## Objetivo

Definir qué debe poder responder la base de datos TSI antes de diseñar tablas y relaciones. La base se alimentará del consolidado limpio internacional y conservará Guadalajara como ciudad objetivo de calibración.

## Preguntas principales

### A. Exploración de observaciones

1. ¿Cuántas observaciones existen por ciudad, fuente y periodo?
2. ¿Qué segmentos o sensores tiene cada fuente?
3. ¿Qué métricas están disponibles para cada ciudad y fuente?
4. ¿Cuál es el rango temporal de cada fuente?
5. ¿Qué tipo de vía representa cada observación?

### B. Calidad y trazabilidad

6. ¿Cuántos registros son válidos y cuántos tienen advertencias?
7. ¿Qué registros tienen valores nulos en las variables principales?
8. ¿De qué archivo, fuente y ciudad proviene cada observación?
9. ¿Qué fuentes tienen duplicados, discontinuidades o cobertura limitada?
10. ¿Qué unidades o variables requieren interpretación antes de compararse?

### C. Comparación entre ciudades

11. ¿Qué ciudades tienen mayor volumen y continuidad de datos?
12. ¿Qué patrones temporales se observan dentro de cada fuente?
13. ¿Qué métricas pueden compararse directamente y cuáles deben analizarse por separado?
14. ¿Qué diferencias existen entre redes urbanas, autopistas e índices agregados?

### D. Preparación para el TSI

15. ¿Qué observaciones tienen variables suficientes para calcular componentes del TSI?
16. ¿Qué fuentes aportan velocidad, intensidad, ocupación o congestión?
17. ¿Qué variables pueden utilizarse para estudiar señales de pre-colapso?
18. ¿Qué datos deben quedar fuera de una comparación por incompatibilidad de unidad o significado?

### E. Calibración futura de Guadalajara

19. ¿Qué patrones externos pueden utilizarse como referencia para Guadalajara?
20. ¿Qué variables locales de Guadalajara faltan para calibrar el índice?
21. ¿Qué resultados deben validarse exclusivamente con datos de Guadalajara?
22. ¿Qué diferencia existe entre una fuente de transferencia y una evidencia local de validación?

## Límites del modelo

La base SQL debe servir para consultar datos observados y su trazabilidad. No debe:

- convertir automáticamente una métrica en otra;
- mezclar Istanbul con sensores como si tuviera segmentos viales;
- tratar São Paulo como fuente de velocidad;
- presentar METR-LA o PEMS-BAY como datos de Guadalajara;
- almacenar imágenes o notebooks como observaciones;
- guardar resultados de algoritmos dentro de la tabla principal de mediciones;
- crear una tabla por ciudad sin una necesidad analítica concreta.

## Resultado de SQL-01

La base debe permitir consultar observaciones por ciudad, fuente, segmento, métrica, periodo y calidad, manteniendo separadas las métricas que no tienen el mismo significado.

## Criterio de aprobación

SQL-01 queda aprobado cuando el modelo conceptual pueda responder estas preguntas sin crear tablas redundantes. El siguiente paso será SQL-02: dibujar las entidades y sus relaciones en papel.