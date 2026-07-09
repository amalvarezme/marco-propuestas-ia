# Registro de corridas de `/propuesta`

Tabla append-only mantenida por el dispatcher (`propuesta.md`, Fase 0). Cada
corrida agrega una fila al resolver su run-id; el dispatcher actualiza
`cerrada`/`estado`/`archivo`/`commit` al archivar o eliminar la corrida.

| run-id | creada | cerrada | estado | idea (breve) | archivo | commit |
|---|---|---|---|---|---|---|
| `pre-run-id` (corrida anterior al esquema de run-id) | 2026-06-25 | 2026-07-08 | eliminada | Ecosistema de agentes autónomos de IA para aprendizaje profundo (alianza intersedes SIUN) | — | `7886ff3` |
