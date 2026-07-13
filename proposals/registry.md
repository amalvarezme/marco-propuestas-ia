# Registro de corridas de `/propuesta`

Tabla append-only mantenida por el dispatcher (`propuesta.md`, Fase 0). Cada
corrida agrega una fila al resolver su run-id; el dispatcher actualiza
`cerrada`/`estado`/`archivo` al archivar o eliminar la corrida. `archivo` es
siempre una **ruta local** (`proposals/<run-id>/`), nunca una URL de
GitHub: ese contenido está gitignored y no se sincroniza con el remoto. La
columna `commit` solo aplica a corridas de antes de esta política (cuando el
contenido sí se comiteaba); en corridas archivadas bajo la política actual
queda en `—`.

| run-id | creada | cerrada | estado | idea (breve) | archivo | commit |
|---|---|---|---|---|---|---|
| `pre-run-id` (corrida anterior al esquema de run-id) | 2026-06-25 | 2026-07-08 | eliminada | Ecosistema de agentes autónomos de IA para aprendizaje profundo (alianza intersedes SIUN) | — | `7886ff3` |
| `2026-07-agentes-autonomos-educacion` | 2026-07-09 | 2026-07-10 | eliminada (Fase 7 aprobada; PDF/DOCX generados antes del borrado) | Ecosistema de Agentes Autónomos de IA para el Aprendizaje Profundo en Ingeniería (alianza intersedes) | — | — |
| `2026-07-agentes-autonomos-aprendizaje-profundo` | 2026-07-11 | 2026-07-12 | eliminada (cancelada por el usuario durante Fase 1b, antes de G1b; sin PDF/DOCX generado) | Ecosistema de Agentes Autónomos de IA para Fortalecer el Aprendizaje Profundo en Estudiantes de Ingeniería (alianza SIUN Manizales/Orinoquía/La Paz) | — | — |
| `2026-07-ecosistema-agentes-ia-aprendizaje` | 2026-07-12 | 2026-07-13 | archivada | Ecosistema de Agentes Autónomos basados en IA para Fortalecer el Aprendizaje Profundo en Estudiantes de Ingeniería (equipo Manizales/Orinoquía/La Paz + BIOS) | `proposals/2026-07-ecosistema-agentes-ia-aprendizaje/` (local) | — |
