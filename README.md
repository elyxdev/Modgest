# Modgest
Modgest es un administrador de mods que utiliza la API de Modrinth para descargar uno o varios mods según la versión y el modloader especificados. El beneficio de esto es su velocidad y compatibilidad con CLI. Pudiendo descargar mods con solo el nombre en cuestión segundos. Le permite especificar si desea mods para el cliente, el servidor o ambos.

# Modo de uso
- Descargue la última versión y ejecútela para su sistema operativo.
- Te pedirá los datos iniciales, el uso es bastante intuitivo y fácil.
Puedes crear un archivo de texto que contenga el nombre de los mods deseados.
Ejemplo (modlist.txt): 
```txt
securitycraft
canary
nuclearcraft
```
Puedes usar el slug o la identificación del proyecto para descargar un mod específico (Descargar uno o más mods).
**(Nota: si tiene una carpeta llamada "mods", los mods descargados estarán allí. Es útil colocar Modgest en el directorio raíz de su servidor)**

# CLI
Si desea integrar este proyecto con otro usando el ejecutable, puede usar los argumentos CLI.
Para ver la ayuda CLI desde la terminal, puede usar este comando
```
$ modgest -h
```
Esto le mostrará los argumentos disponibles en este proyecto con otro usando el ejecutable, puede usar los argumentos CLI.
Si el archivo `modgest_config.json` aún no está creado o configurado, debe configurarlo desde la CLI
> Configurar desde la CLI
```
  -c                     Configurar
  --key <llave>          Valor a configurar
  --value <valor>        Valor configurado
```
Si la configuración está lista, ahora puedes descargar tus mods.
> Descarga desde la CLI
```
  -d                   Descarga un mod
  --name NAME          El nombre del mod a descargar (Un solo mod)
  --filename FILENAME  El nombre del archivo que contiene los nombres de mods (Varios mods)
```
# As library
Si desea utilizar Modgest en su código Python, debe importar estas funciones.
```python
from modgest import modgest_config, reload_config, ask_modrinth
```
Ejemplo de uso:
```python
from modgest import modgest_config, reload_config, ask_modrinth, modrinth_from_file
modgest_config("user_version", "1.20.1")
modgest_config("mod_type", "client") # Sólo para mods del lado del cliente
modgest_config("loader", "fabric")
reload_config() # Debe usarse después de usar modgest_config()
ask_modrinth("sodium") # Descarga sodium para Fabric 1.20.1
modrinth_from_file("modlist.txt") # Descargas mods contenidos en modlist.txt para Fabric 1.20.1
```