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
- [x] T3 Construir el acervo de referencias de §2 (bibliógrafo)
- [x] T4 Despachar al redactor para `redaccion/sections/02_justificacion.tex` +
      mirror del vault
- [x] T5 Guardia: re-indexar el vault y armar el bloque `EVIDENCIA DE GRAFO`
- [x] T5b Auditar los campos bibliográficos de las 16 entradas nuevas con DOI
- [x] T5c Auditar la prosa con `grant-flow-auditor` (94/100, tres cambios)
- [x] T5d Arreglar el enlace clave↔nota de paper (28 notas) y apuntar el vault al
      registro canónico (28 notas)
- [ ] T6 Re-despachar al revisor sobre el texto pulido y presentar el GATE G3
      al usuario
- [ ] T8 (antes de Fase 7) Completar el bloque `## Verificación` en las 50 notas
      del corpus semilla — ver el hallazgo abajo
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

## Decisiones del operador (2026-09-30)

Las dos estaban señaladas como pendientes en `insumos/ideas/idea.md` y ninguna se
podía resolver sin él.

**1. TRL objetivo: 6.** El cierre (b) de §2 lo nombra explícitamente como
prototipo validado en entorno relevante. El razonamiento que sostiene la decisión:
la línea del equipo ya está validada en un benchmark (DAIC-WOZ), y lo que aporta
el proyecto es su extensión al dominio del desastre y su despliegue portable con
estudiantes reales de la Sede Manizales. Se descartó TRL 7 porque el criterio de
evaluación *Alcance del proyecto* (15 pts) castiga prometer lo que 12 meses no
sostienen.

**2. Enfoque territorial: que el bibliógrafo busque y verifique fuentes
oficiales.** El criterio vale 20 puntos y exige que el proyecto se desarrolle en
los territorios afectados, pero el epicentro fue San José del Palmar (Chocó) y la
sede es Manizales. §2 lo resuelve con datos verificados y **sin exagerar el
vínculo local**.

## T3 — Acervo construido (bibliógrafo, `muolxpta-1-hw5r`)

`refs.bib` pasó de 51 a **79 entradas**, con 79 claves únicas y sin duplicados.
Las 28 nuevas se reparten en 65 `@article`, 1 `@inproceedings`, 9 `@misc` y 4
`@techreport`, estas últimas la clase institucional recién admitida.

- **15 referencias Q1/Q2 nuevas**, por encima del piso de 13.
- **13 instrumentos institucionales** con URL oficial confirmada y fecha de
  consulta: ODS 3 (meta 3.4) y el informe mundial de salud mental de la OMS, PND
  2022-2026 (Ley 2294 de 2023) y el Plan de Desarrollo de Caldas (Ordenanza 974
de 2024) con su Plan Territorial de Salud, OCDE *Health at a Glance LAC 2023* y
  OPS, más los instrumentos del sismo (SGC, Decreto 1171 de 2026, SITREP 4).
- Trazabilidad completa: `artefactos/scoping/papers/paper-51.md` a `paper-78.md`
  con su bloque `## Verificación`, y 28 notas espejo en
  `artefactos/vault/insumos/`.

**Evidencia territorial encontrada**, que era el punto crítico: 2.130 personas
caracterizadas en Caldas con **5,25 % que requiere acompañamiento psicológico**
(`ucaldas2026_caracterizacion`), sedes de la UNAL Manizales afectadas
(`mineducacion2026_unal`) y daño hospitalario en el eje cafetero
(`paho2026_sitrep`). El bibliógrafo separó deliberadamente lo que sostiene
afectación **local** de lo que solo sostiene afectación **nacional o de otras
regiones**, y el redactor recibió esa distinción explícita.

**Lo que el bibliógrafo se negó a inventar** (y por qué es la conducta correcta):
no pudo verificar texto en mano un eje o meta del PND específica de salud mental,
no encontró un lema propio del plan de Caldas, y descartó cifras de daño que
venían de una fuente no gubernamental. Todo eso quedó reportado como pendiente en
lugar de rellenarse.

**Gap preexistente detectado:** `artefactos/vault/insumos/` tiene 29 notas contra
79 entradas de `refs.bib`. Las notas del corpus semilla (las 51 originales) nunca
se escribieron. No es de esta fase, pero conviene cerrarlo antes de la auditoría
final de Fase 7.

## Desviación de proceso en G3 (2026-09-30)

**Qué pasó.** Despaché al `revisor` sin haber despachado antes al
`grant-flow-auditor`. La regla del pipeline es explícita: cuando la unidad
produjo o editó secciones narrativas —`redactor` o `investigador`— el auditor de
prosa va **antes** que el revisor, y la auditoría incluye como paso propio el
pulido de la skill `estilo-natural-es`.

**Por qué importó.** El revisor devolvió PASS, pero entre sus observaciones
—marcadas como no bloqueantes— dejó constancia de dos repeticiones entre §3 y §2:
el cierre re-cita el par de AUC del habla (0,89 / 0,91) que §3 ya reporta con un
encuadre casi idéntico, y el párrafo 6 reutiliza la fórmula "déficits de
fidelidad, usabilidad y adaptación cultural" casi verbatim de §3. Eso es
exactamente la clase de fricción que el auditor existe para eliminar. El revisor
lo vio y lo anotó, pero su mandato es el cumplimiento, no el micro-estilo.

**Cómo se corrigió.** Se despachó al `grant-flow-auditor` sobre §2 con la ruta
exacta de la skill y con esos dos casos señalados como objetivos concretos. Como
el auditor **edita** el `.tex`, el veredicto PASS del revisor deja de aplicar al
texto final: hay que re-despachar al revisor sobre la versión pulida y solo
después presentar la compuerta. Un PASS obtenido antes de una edición posterior
del archivo no es un PASS válido.

**Regla para no repetirlo.** En cualquier unidad que produzca prosa nueva, el
orden es `redactor`/`investigador` → `grant-flow-auditor` → `revisor` → usuario. Si
por alguna razón el revisor corre primero y PASSa, y después se toca el texto, el
PASS queda invalidado y hay que repetir la revisión.

## Segundo dictamen de G3: FAIL por trazabilidad (2026-09-30)

Tras el pulido de prosa, el revisor devolvió **FAIL**, y todos los checks de
contenido volvieron a dar PASS (estructura, densidad de citas, unicidad de
claves, resolución en `refs.bib`, incisos, TRL 6, PND sin inventar, coherencia
§2↔§3, territorio, estilo). El único FAIL fue el *check 4*, el de no-huérfanas:
24-26 claves nuevas de §2 «resolvían únicamente» a su nota de
`artefactos/vault/insumos/`, y esas notas no tienen bloque `## Verificación`.

**El revisor acertó en el síntoma y se equivocó en la causa.** Lo comprobé:
las 28 notas nuevas de `artefactos/scoping/papers/paper-51.md` a `paper-78.md`
**SÍ tienen** el bloque `## Verificación` con ID resuelto (28 de 28). Lo que
faltaba era el **enlace**: ninguna nota registraba su `cite_key`, así que el
revisor no podía emparejar una clave con su nota de paper y concluyó que la clave
«solo resolvía» al vault, cuyo formato de nota legítimamente no incluye ese
bloque.

**El arreglo aplicado** ataca la causa, no el síntoma: se añadió `- Clave:
<cite_key>` a las 28 notas de paper (mapeadas 16 por DOI y 12 por URL oficial), y
un bloque `## Verificación` a las 28 notas del vault que **apunta** al registro
canónico en lugar de duplicarlo. Verificado después: las 28 claves nuevas de §2
resuelven a una nota con `## Verificación` y `Resuelto: sí`.

## Hallazgo nuevo: dos formatos de nota conviven en el corpus

Al perseguir el FAIL apareció algo más grande. Las **11 claves de reúso de §2**
que vienen del corpus semilla no resuelven a ninguna nota verificada, y la causa
no es el enlace: **las 50 notas del corpus semilla no tienen bloque
`## Verificación` en absoluto** (0 de 50).

| | `paper-1`…`paper-50` (semilla) | `paper-51`…`paper-78` (nuevas) |
|---|---|---|
| Metadatos | lista de viñetas (`- Autores:`, `- Año:`, …) | una línea |
| Bloque `## Verificación` | **no tiene** | sí, con ID resuelto |
| `cite_key` registrada | no | sí (tras el arreglo) |

No es de esta fase: el corpus semilla se escribió en la Fase 1 con la plantilla
anterior a que existiera el invariante de verificación, y el check del revisor
declara explícitamente los huérfanos preexistentes **fuera de alcance**. Tampoco
lo introdujo §2: las 11 claves ya se citaban en §3/§4/§5 y §4 pasó su compuerta.

**Por qué conviene cerrarlo antes de la Fase 7.** La auditoría final repasa el
documento completo, y toda clave del corpus semilla volverá a quedar sin registro
verificable. La plantilla se puede aplicar ahora porque las notas ya tienen
`DOI/URL`, pero exige verificar 50 DOI contra `semanticscholar`/`crossref`/`openalex`
antes de escribir cada bloque: no se puede rellenar de memoria. Es una tarea
delimitada y delegable al `bibliografo-propuesta`.

## Notas de ensamble

- La guía ajustada declara "sin entidades externas (el Anexo 3 no aplica)",
  mientras que los anexos del §8.6 redactados en Fase 1 sí prevén una entidad
  externa (UTP) con carta de compromiso de recursos adicionales. La
  contradicción no afecta a §2, pero hay que resolverla antes de §9 y del
  cierre; queda anotada para no perderla.
- §1 Título aún no existe en disco, así que el ensamble de esta compuerta no lo
  incluye (igual que en G1 y G2).
