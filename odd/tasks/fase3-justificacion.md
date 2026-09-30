# Fase 3 — §2 Justificación y pertinencia (unidad `fase3`, compuerta G3)

Corrida `2026-09-tept-depresion-ia-portable`. `next_step: fase3`.

## Objetivo

Producir §2 Justificación y pertinencia y pasarla por el Revisor en la compuerta
G3, sin avanzar hasta la aprobación del usuario.

Requisitos que impone la guía ajustada al TDR (`artefactos/guia_ajustada_TDR.md`,
§2), que es la guía aplicable de esta corrida:

- **Mínimo 6 párrafos** cubriendo: (1) motivación, (2) ODS con número y nombre
  oficial, (3) PND vigente **y Plan de Desarrollo Departamental de Caldas**,
  (4) informes de organismos multilaterales (OCDE, Banco Mundial u otro),
  (5) alineación con el TDR anclando la línea *Salud pública en el marco de
  desastres naturales* (15 pts) y el enfoque territorial en Manizales y Caldas
  (20 pts) con evidencia de afectación local, y (6) crecimiento y potencial de
  la IA en la temática.
- **Cierre obligatorio** con (a) justificación técnica del uso de IA frente a
  métodos tradicionales y (b) justificación del producto tangible con **TRL 6 o
  7 explícito**. §2 es la única sección que puede nombrar el TRL textualmente en
  su cierre, y puede autorreferirse como "la propuesta".
- **≥13 referencias Q1/Q2** adicionales a las de §4, con densidad obligatoria de
  3-4 claves distintas por párrafo y **ninguna clave repetida dentro de §2**.
- `\section` único, sin subsecciones. Prohibido el inciso `—texto—`.

## Tareas

- [x] T1 Reunir el contexto: guía ajustada §2, directrices generales,
      convenciones LaTeX, contrato del redactor, contrato del bibliógrafo
- [x] T2 **Cerrar el vacío de referencias institucionales** (ver abajo)
- [ ] T3 Construir el acervo de referencias de §2 (bibliógrafo) — en curso,
      tarea `muolxpta-1-hw5r`
- [ ] T4 Despachar al redactor para `redaccion/sections/02_justificacion.tex` +
      mirror del vault
- [ ] T5 Guardia: re-indexar el vault solo si
      `artefactos/vault/secciones/02_justificacion.md` cambió; armar e inyectar
      el bloque `EVIDENCIA DE GRAFO`
- [ ] T6 Despachar al revisor y presentar el GATE G3 al usuario
- [ ] T7 Registrar `artefactos/pipeline/40-fase3.md` y la telemetría en
      `artefactos/pipeline/_estado.md`

## T2 — Vacío encontrado y cómo se cerró

**El problema.** §2 está obligada a citar instrumentos oficiales (ODS con
número y nombre, PND, Plan de Desarrollo de Caldas, informes OCDE/Banco
Mundial). Pero el invariante de escritura de `refs.bib` del
Bibliografo-Propuesta exigía, para **toda** entrada nueva, un ID estable
académico (DOI/S2/arXiv) resuelto vía `semanticscholar`/`crossref`/`openalex`.
Un decreto o un informe del Banco Mundial no tiene DOI y no está indexado en
ninguna de esas fuentes. `refs.bib` lo confirmaba: 50 `@article` + 1
`@inproceedings`, **cero entradas institucionales**.

Sin resolver esto, §2 no se puede escribir al estándar de la guía: o se
inventan las citas de política (inaceptable), o se omite el punto 2/3/4 (la
guía lo prohíbe explícitamente).

**La solución.** Extender el invariante con una segunda clase de evidencia en
lugar de una excepción: los **documentos de política se verifican por URL
oficial**. La misma garantía —nada sin verificar, nota de trazabilidad por
entrada, cero entradas sin resolver— con una fuente de prueba distinta y
adecuada al tipo de fuente. Se escriben como `@techreport` o `@misc` con
`author` institucional entre dobles llaves, `url` y `note = {Consultado: ...}`,
y su nota `paper-N.md` registra `- Herramienta: url oficial`.

**Dónde vive.** `.claude/agents/bibliografo-propuesta.md`, sección «Clase de
evidencia institucional (documentos de política)», más la plantilla mínima de
`paper-N.md`. Los tres ports (`.pi/`, `.opencode/`, `.agent/`) se regeneraron
con los generadores y su `--check` da limpio, así que el aprendizaje queda en
los archivos del proyecto y no depende de la memoria de nadie.

Es un vacío recurrente, no de esta corrida: **toda** propuesta tiene que
alinear su §2 con los ODS, el PND y los organismos multilaterales.

## Notas de ensamble

- La guía ajustada declara "sin entidades externas (el Anexo 3 no aplica)",
  mientras que los anexos del §8.6 redactados en Fase 1 sí prevén una entidad
  externa (UTP) con carta de compromiso de recursos adicionales. La
  contradicción no afecta a §2, pero hay que resolverla antes de §9 y del
  cierre; queda anotada para no perderla.
- §1 Título aún no existe en disco, así que el ensamble de esta compuerta no lo
  incluye (igual que en G1 y G2).
