# Feature: revisión de figuras + equipo, entidad externa y anexos (G2 → G3)

## Goal

Apply the operator's revision round after G2:

1. **Árbol de problemas**: reducir a **máximo 3 causas por subproblema** (hoy 5/5/4 = 14 raíces) y **máximo 4 efectos** (hoy 7 ramas).
2. **Mapa de estado del arte**: reconstruirlo con una composición más armónica —revisar estilo y estructura— y que funcione mejor en la página.
3. **Equipo y entidad externa**: incorporar a la UTP (grupo de investigación en Automática, profesor David Augusto Cárdenas) como entidad externa, y a los coinvestigadores UNAL Germán Castellanos y Jorge Iván Montes, con horas de dedicación y roles.
4. **Encabezado de `main.tex`**: bajo el título, investigador principal + Laboratorio de IA + GCPDS + Semillero de Ciencia de Datos e Inteligencia Artificial.
5. **Anexos de la convocatoria**: crear una carpeta nueva en Drive (dentro de `proyectos unal`) con los anexos por generar: avales de horas de jornada docente por investigador, carta de la entidad externa, carta de estudiantes y demás documentos obligatorios del §8.6 del TDR.

## Datos aportados por el operador (autoridad)

| Rol | Persona | Entidad | Horas/semana | Aporte |
|---|---|---|---|---|
| Investigador principal | Andrés Marino Álvarez-Meza | UNAL LIA | 4 | Dirección del proyecto + estrategias de implementación de agentes |
| Coinvestigador | Germán Castellanos-Domínguez | UNAL GCPDS | 2 | Técnicas de procesamiento de bioseñales |
| Coinvestigador | Jorge Iván Montes-Monsalve | UNAL | 2 | Sistemas de adquisición de datos |
| Coinvestigador (entidad externa) | David Augusto Cárdenas | UTP, grupo de Automática | 2 | Estrategias de inferencia en el borde |
| Estudiante de pregrado 1 | (rol, sin nombre) | UNAL | 4 meses | — |
| Estudiante de pregrado 2 | (rol, sin nombre) | UNAL | 4 meses | — |
| Estudiante de maestría | (rol, sin nombre) | UNAL | 1 año | — |
| Estudiante de doctorado | (rol, sin nombre) | UNAL | duración del proyecto (12 meses) | — |

## Anexos obligatorios del TDR §8.6 (fuente: `insumos/tdr/Terminos-de-Referencia.pdf`)

1. Carta de la UAB/centro/instituto/sede del investigador principal, con las **horas de jornada docente** dedicadas.
2. Carta de aval de la facultad donde se ejecutarán los recursos.
3. **Aval de horas de jornada docente por cada docente participante**, firmado por el director de la UAB correspondiente.
4. Carta de compromiso del estudiante vinculado (Anexo 2 de la convocatoria).
5. Carta de compromiso del aporte de recursos adicionales (Anexo 3) — **ahora aplica**, porque la UTP entra como entidad externa (habilita los 5 pts de "Fuentes de Financiación Adicionales").

## Tasks

- [x] T1 Redactar de nuevo el bloque de especificación del árbol (≤3 causas/SP, ≤4 efectos) — 14→9 raíces, 7→4 efectos
- [x] T2 Regenerar `diag_arbol_problemas.tex` + bucle de figura — intento 1/4 FAIL (ramas borde contra borde) → intento 2/4 PASS tras separar offsets a ±1.9/±5.7 cm y `text width` 3.1 cm
- [x] T3 Rediseñar el mapa de estado del arte (armonía: filas alineadas, estructura) + bucle de figura — **hecho el 2026-09-30** con el pipeline determinista nuevo. `diag_estado_arte.tex` es ahora salida generada de `redaccion/specs/estado_arte.spec.json` (5 clústeres × 5 papers, 16 aristas internas, limitante por clúster). Medición antes → después: **17,0 × 31,3 cm → 17,78 × 28,54 cm**, PASS en 1,1 s. El operador eligió **dos figuras**: el mapa se entrega como `estado_arte_a` (grupos 1-3, 15,53 × 12,62 cm) y `estado_arte_b` (grupos 4-5 + cierre, 9,47 × 15,57 cm), ambas a tamaño natural y sin `resizebox`; `main.tex` tiene las dos entradas y §4 referencia ambas con `\Cref{fig:estado_arte_a,fig:estado_arte_b}`. Ver "Decisión del operador" en `odd/tasks/marco-tikz-pi-native.md`.
- [x] T4 Actualizar el encabezado de `main.tex` (IP, LIA, GCPDS, Semillero)
- [x] T5 Registrar el equipo en `artefactos/equipo.md` (fuente para §9 y para los anexos)
- [x] T6 Redactar los anexos del §8.6 en `artefactos/anexos/`
- [ ] T7 Crear la carpeta en Drive (`proyectos unal`) y subir los anexos
- [ ] T8 Recompilar `main.pdf` y presentar la ronda al usuario

## Evidence

- **T1**: `03_descripcion_problema.tex` spec block rewritten: 9 causes (3 per subproblem) and 4 effects; prose of §3 verified byte-identical (34 citation commands, 35 distinct keys untouched).
- **T2**: figure loop attempt 1/4 → `revisor-figuras` FAIL (the 4 effect boxes were border-to-border); `tikz-optimizer` applied `text width: 3.3→3.1 cm` and offsets `±1.7/±5.1 → ±1.9/±5.7 cm`; `OVERFULL: arbol_problemas 0 occurrence(s)` re-verified by the parent; attempt 2/4 → `revisor-figuras` **PASS**.
- **Drive recon**: no folder literally named "proyectos unal" or "convocatoria siun intersedes" exists as such. The project tree found is `Mi unidad / UNAL / GCPDS_main / Proyectos / {Formulación Proyectos, Proyectos Activos, Otros - Finalizados}`, with analogues `Proyectos Activos/proyectoUTP2026` (holds the UTP TDR) and `Proyectos Activos/951Geotermia_UTP_UNAL`. The previous SIUN-intersedes hours avales live in the shared folder `Fortalecimiento de alianzas interdiciplinares SIUN (2025-2027) / Ecosistemas Agentes - Andrés / DocumentosHermes / AvalesHoras_editables / editables` as `Agentes_Aval_Intersedes_Andrés Álvarez.docx` and `..._Germán Castellanos.docx` — reusable templates.
- **Subagent incident**: `revisor-figuras` failed twice with no final report at `high` thinking (same output-budget exhaustion as `grant-flow-auditor`); its profile was moved to `nan/glm5.3-flash@medium` and the next run completed.

- **T4** (verificado por lectura directa): `redaccion/main.tex` — bloque de título con `Andrés Marino Álvarez-Meza` y las tres líneas institucionales: Laboratorio de Inteligencia Artificial (LIA), Grupo de Control y Procesamiento Digital de Señales (GCPDS), Semillero de Ciencia de Datos e Inteligencia Artificial, Universidad Nacional de Colombia, Sede Manizales.
- **T5**: `artefactos/equipo.md` (96 líneas) — datos generales, tabla de roles con dedicación y aportes, marcas `[inferido]` y `⟨completar: ...⟩` para lo no confirmado por el operador.
- **T6**: `artefactos/anexos/` — 9 archivos (índice + 8 documentos, 673 líneas en total), todos en estado `borrador`, con la tabla de anexos obligatorios del §8.6, la coherencia documental con la decisión de vincular a la UTP y la lista de datos por completar antes de firmar.
- **T3** (ejecutado el 2026-09-30): el mapa se reconstruyó desde la spec determinista. Se corrigieron cuatro defectos estructurales que el bucle anterior no podía ver: (a) el ancho del estilo `paper` se calculaba con la fuente equivocada porque el estilo no fijaba `font=`; (b) las aristas que saltan nodos intermedios cruzaban las tarjetas intermedias y ahora hacen un desvío acotado en el margen derecho; (c) los enlaces entre clústeres de filas distintas envolvían la figura (+7,4 cm de ancho medidos) y ahora se dibujan solo entre vecinos de la misma fila, con la relación declarada en el `%` del `.tex` para que la prosa de §4 la conserve; (d) la frase de cierre se ancoraba a la última fila y su ancho fijo de 15 cm empujaba la caja envolvente fuera de la página. Resultado: 17,78 × 28,54 cm, PASS en 1,1 s. `main.tex` todavía lo escala con `\resizebox`; la decisión de página está en el blocker de `marco-tikz-pi-native.md`.

## Blocker

**Resuelto el 2026-09-30.** El operador habilitó el OAuth de Drive, Gmail, Docs y
Sheets; los cuatro servidores MCP respondieron autenticados como
`amalvarezme@unal.edu.co` en la verificación de esta sesión. T7 queda desbloqueado:
el destino real es `Mi unidad / UNAL / GCPDS_main / Proyectos Activos`
(`id 14mZMkr_F8Dch24PFTeMhSrgEeGnYMsAT`), donde ya conviven `proyectoUTP2026`,
`951Geotermia_UTP_UNAL`, `Orquídeas No. 112721-216-2025- Minciencias`,
`MATERNO_TERMOGRAFIA` y `Proyecto_Luker_UNAL_BIOS`.

Dos decisiones siguen abiertas para T7, antes de escribir en Drive: (a) nombre exacto
de la carpeta nueva y si se crea dentro de `Proyectos Activos` o como hermana; (b)
formato de subida — los anexos son borradores Markdown y el §8.6 exige PDF de máximo
2 MB por archivo.
