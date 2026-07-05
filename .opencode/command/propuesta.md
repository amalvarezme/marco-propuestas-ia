---
description: Inicia el pipeline multi-agente de redacción de una propuesta de investigación en IA a partir de la idea del usuario y sus insumos.
agent: coordinador-propuesta
---

El usuario quiere redactar una propuesta de investigación en IA siguiendo el
marco multi-agente. Ejecuta el pipeline interactivo con puertas de revisión
definido en AGENTS.md.

Entrada del usuario:

$ARGUMENTS

Instrucciones de inicio:

1. Si no hay insumos (PDFs/papers/enlaces) en el mensaje ni en `info_data/`,
   pídelos al usuario antes de avanzar. Los archivos fuente se guardan en
   `info_data/`. Si los hay, despacha al `insumos-observador` (Fase 0) para extraer
   y estructurar el contexto en `proposal/insumos.md`.
2. Crea/mantén un registro de estado del documento en
   `proposal/estado_propuesta.md` con: sección actual, artefactos clave
   (pregunta de investigación, subproblemas, objetivos, hipótesis) y estado de
   cada gate.
3. Avanza fase por fase según el pipeline. Tras cada gate, presenta al usuario:
   (a) resumen de lo producido, (b) veredicto del revisor, (c) petición de
   aprobación explícita. NO avances sin aprobación.
4. Recuerda: toda la salida del documento es en español; los archivos van en
   `proposal/sections/*.tex` y `proposal/refs.bib`; ensambla `proposal/main.tex`
   al final (Fase 7).
5. Consulta `guiaProyectosIA_Agente.md` para las instrucciones párrafo a
   párrafo de cada sección.

Comienza ahora confirmando la idea del usuario y listando los insumos
detectados, luego arranca la Fase 0.
