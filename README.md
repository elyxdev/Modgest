# Modgest
Modgest is a mod manager that uses the Modrinth API to download one or multiple mods according to the specified version and modloader. The benefit of this is its speed and CLI support. Being able to download mods with just the name in seconds. Allows you to specify if you want mods for client, server or both.

# Usage
- Download the latest release and run it for your operating system.
- It will ask you for the initial data, the use is quite intuitive and easy. 
You can make a text file containing the name of the desired mods
Example (modlist.txt): 
```
securitycraft
canary
nuclearcraft
```
You can use the slug or project id to download a specific mod (Downloading one or more mods).
**(Note: If you have a folder named "mods", the downloaded mods will be there. Useful to put Modgest in your server root directory)**

# CLI
If you want to integrate this project with another using the executable, you can use the CLI arguments.
To view the CLI help from the terminal you can use this command
```
$ modgest -h
```
This will show you the available arguments.
If the `modgest_config.json` file isn't already created or configurated you must configure it from the CLI
> Configuring from the CLI
```
  -c                   Edit configuration file
  --key KEY            The key to config (user_version/loader/mod_type)
  --value VALUE        The value to config
```
If the configuration is ready, now you can download your mods.
> Downloading from the CLI
```
  -d                   Download a mod
  --name NAME          The mod name to download
  --filename FILENAME  The filename to extract mods names
  --mirror MIRROR      download from modrinth/curseforge/any
```
# As library
If you want to use Modgest in your Python code, you must import this functions.
```python
from mod_gest import modgest_config, reload_config, ask_modrinth
```
Example of usage:
```python
from mod_gest import modgest_config, reload_config, ask_modrinth, modrinth_from_file
modgest_config("user_version", "1.20.1")
modgest_config("mod_type", "client") # Only for client-sided mods
modgest_config("loader", "fabric")
reload_config() # Must be used after using modgest_config()
ask_modrinth("sodium") # Downloads sodium for Fabric 1.20.1
modrinth_from_file("modlist.txt") # Downloads mods contained in modlist.txt for Fabric 1.20.1
```
