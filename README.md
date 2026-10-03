# Calendario Bàsquet Alella A – FCBQ

Proyecto para obtener automáticamente el calendario del Bàsquet Alella A desde FCBQ y publicarlo con GitHub Pages.

- Actualización semanal: domingo 06:17, hora de Madrid.
- Ejecución manual desde Actions.
- Publicación automática mediante GitHub Pages.
- El archivo público es `basquet-alella-a.ics`.

## Configuración

1. Crea un repositorio público en GitHub.
2. Sube todos los archivos y carpetas, incluida `.github/workflows/`.
3. Ve a **Settings → Pages** y en **Build and deployment → Source** selecciona **GitHub Actions**.
4. Ve a **Actions → Actualizar y publicar calendario FCBQ → Run workflow**.
5. Cuando termine correctamente, el calendario estará en:

`https://TU_USUARIO.github.io/NOMBRE_REPOSITORIO/basquet-alella-a.ics`

## iPhone

**Ajustes → Calendario → Cuentas → Añadir cuenta → Otra → Añadir calendario suscrito** y pega la URL anterior.

La FCBQ proporciona la hora de inicio; el archivo estima 2 horas de duración para cada partido. La frecuencia de actualización de un calendario suscrito la decide iOS.

Fuente: https://www.basquetcatala.cat/partits/calendari_equip_global/129/89394
