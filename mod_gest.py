# Tal vez añadir curseforge
# Librerías
import requests, time, argparse, json
from mod_utils import *

# Variables globales (Sin config)
config = {"user_version": "1.20.1", "loader": "forge", "mod_type": "any"}
working_directory = os.getcwd()
config_file_route = os.path.join(working_directory, "modgest_config.json")
modgest_version = "1.0"
timeout_rate = 2
user_version = ""
mod_type = ""
loader = ""
def reload_config(save=False):
    global user_version, mod_type, loader, config
    if save:
        if not os.path.exists(config_file_route):
            with open(config_file_route, "w") as f:
                pass
        with open(config_file_route, 'w') as config_file:
            config_file.write(json.dumps(config))
        return
    if os.path.exists(config_file_route):
        with open(config_file_route, 'r') as config_file:
            config = json.load(config_file)
    else:
        with open(config_file_route, 'w') as config_file:
            jilog("This is a first time check... (This won't happen again)")
            config = {
                "user_version": winput("Enter your game version > ", torep="1.20.1"),
                "mod_type": winput("Search mods for (client/server/any) > ", torep="any").lower(),
                "loader": winput("Enter your modloader (forge/fabric/neoforge) > ", torep="forge").lower()
            }
            config_file.write(json.dumps(config))
    # Variables globales (usando config)
    user_version = config["user_version"] # MC Version
    mod_type = config["mod_type"] # server | client | any 
    loader = config["loader"] # forge | neoforge | fabric

def modgest_config(key:str, val:str):
    config[key] = val
    reload_config(save=True)

#### MODRINTH

def ask_modrinth(mod_name = "", itering=False): # Descargar un mod de Modrinth
    if __name__ == "__main__" and itering == False:
        cls()
    if mod_name == "":
        return
    mod_data = search_modrinth(mod_name)
    hits = modrinth_process(mod_data)
    if hits == None:
        return None
    for mod in hits[::-1]:
        header = f"[{mod['show_mod_id']}] {mod['name']}"
        data_t = remake_string(f"{mod['description']}")
        make_table(data_t, table_header=header, show=True)
    if __name__ == "__main__":
        if not itering:
            jilog("Enter to return...")
        print()
    if __name__ == "__main__":
        if not itering:
            tololoi = winput("Select a mod > ", torep="RETRN")
            if tololoi != 1:
                if not tololoi.isdigit():
                    return
        else:
            tololoi = 1
        
    else:
        tololoi = 1
    
    selected_mod = hits[int(tololoi) - 1]
    n_mod_id = selected_mod["external_mod_id"]
    download_modrinth(n_mod_id, user_version)

def search_modrinth(mod_name : str): # Buscar en modrinth
    url = f'https://api.modrinth.com/v2/search?query={mod_name}&facets=[["categories:{loader}"],["versions:{user_version}"]]'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def modrinth_process(mod_data : dict): # Procesar datos recibidos del search
    if mod_data == None:
        return None
    if mod_data["total_hits"] < 1:
        return None
    hits = mod_data["hits"]
    final_hits = []
    lasthit = 0
    for mod in hits:
        temporal_hit = {}
        # ====== Comprobaciones

        # Versión compatible
        if user_version not in mod["versions"]: 
            continue

        # Tipo compatible (compatible en servidor)
        # Si es requerido en cliente y es un servidor o no es any
        if mod["client_side"] == "required" and mod["server_side"] != "required" and (mod_type == "server" or mod_type != "any"):
            continue

        # Data
        lasthit += 1
        temporal_hit["name"] = mod["title"]
        temporal_hit["description"] = mod["description"]
        temporal_hit["author"] = mod["author"]
        temporal_hit["slug"] = mod["slug"]
        temporal_hit["internal_mod_id"] = hits.index(mod)
        temporal_hit["show_mod_id"] = lasthit
        temporal_hit["external_mod_id"] = mod["project_id"]

        # Enviar al hitlist final
        final_hits.append(temporal_hit)
    if len(final_hits) < 1:
        return None
    return final_hits

def download_modrinth(mod_id:str, version_id:str): # Obtener url y realizar get (Modrinth)
    url = f'https://api.modrinth.com/v2/project/{mod_id}/version?loaders=["{loader}"]&game_versions=["{version_id}"]'
    response = requests.get(url).json()
    selected = response[0]
    if version_id not in selected["game_versions"]:
        return
    if loader not in selected["loaders"]:
        return
    file_url = selected["files"][0]["url"]
    file_name = selected["files"][0]["filename"]
    if os.path.exists(os.path.join(working_directory, "mods/")):
        file_name = "mods/" + file_name
    file_response = requests.get(file_url)
    if file_response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(file_response.content)
        jilog(f"{file_name} downloaded successfully.")
        time.sleep(timeout_rate)
    else:
        print(f"Error downloading file [{file_response.status_code}]")

def modrinth_from_file(filename:str):
    if not os.path.exists(filename):
        if not os.path.exists(f"{filename}.txt"):
            print(f"File not found: {filename}")
            time.sleep(3)
            return
        else:
            filename = f"{filename}.txt"
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(f"Downloading: {line}")
            ask_modrinth(line, itering=True)

#### MAIN

def visual_main(): # Función visual principal
    cls()
    jilog("""
[1] Search and download mod
[2] Download mods from file
[3] Change options
[4] Exit
""")
    
    opt = winput("Option > ")
    if opt.isdigit():
        opt = int(opt)
        if opt == 1:
            cls()
            ask_modrinth(winput("Enter the name of the mod: "))
        elif opt == 2:
            cls()
            modrinth_from_file(winput("Enter the path of the file: "))
        elif opt == 3:
            cls()
            modgest_config("user_version", winput("Enter your game version > "))
            modgest_config("mod_type", winput("Search mods for (client/server/any) > ").lower())
            modgest_config("loader", winput("Enter your modloader (forge/fabric/neoforge) > ").lower())
            reload_config()
            jilog("Options changed successfully.")
            time.sleep(3)
        elif opt == 4:
            os._exit(0)
        else:
            print("Invalid option.")
            time.sleep(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Use the Modrinth API to download mods faster.')
    # Descarga switch
    parser.add_argument('-d', action='store_true', help='Download a mod')
    # Especificar modname
    parser.add_argument('--name', type=str, help='The mod name to download')
    # Especificar filename
    parser.add_argument('--filename', type=str, help='The filename to extract mods names') 
    # Especificar mirror
    parser.add_argument('--mirror', type=str, help='download from modrinth/curseforge/any')
    
    # Config switch
    parser.add_argument('-c', action='store_true', help='Edit configuration file')
    # Especificar key
    parser.add_argument('--key', type=str, help='The key to config')
    # Especificar value
    parser.add_argument('--value', type=str, help='The value to config')

    args = parser.parse_args()
    if args.c == True: # Sí config
        if args.key == None or args.value == None: # Si ambos están vacíos
            os._exit(0)
        modgest_config(args.key, args.value)
        jilog("Configuration updated successfully.")
        os._exit(0)

    if args.d == True: # Sí download
        reload_config()
        if args.name == None and args.filename == None: # Si ambos están vacíos
            os._exit(0)
        if args.name != None:
            ask_modrinth(args.name,itering=True)
        if args.filename != None:
            modrinth_from_file(args.filename)
        os._exit(0)
    # Non-CLI
    reload_config()
    cls()
    jilog(f"ModGest {modgest_version}: Loaded")
    jilog(f"Modloader: {loader.capitalize()}")
    jilog(f"Mod type: {mod_type.capitalize()}")
    jilog(f"MC Version: {user_version}")
    
    time.sleep(1)
    while True:
        visual_main()