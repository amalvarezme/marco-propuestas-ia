# Registro de corridas de `/propuesta`

Tabla append-only mantenida por el dispatcher (`propuesta.md`, Fase 0). Cada
corrida agrega una fila al resolver su run-id; el dispatcher actualiza
`cerrada`/`estado`/`archivo`/`commit` al archivar o eliminar la corrida.

| run-id | creada | cerrada | estado | idea (breve) | archivo | commit |
|---|---|---|---|---|---|---|
