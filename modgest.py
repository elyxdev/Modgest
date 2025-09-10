import requests, time, argparse, json
from urllib.parse import unquote
from modgest_utils import *
from glob import glob

# Variables globales (Sin config)
config = {"user_version": "1.20.1", "loader": "forge", "mod_type": "ambos"}
working_directory = os.getcwd()
config_file_route = os.path.join(working_directory, "modgest_config.json")
modgest_version = "1.3.3"
user_version = ""
mod_type = ""
loader = ""
mf = ""

# Funciones de configuración

def reload_config(save=False): # Recargar la configuración
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
            config = {
                "user_version": winput("Ingresa la versión de tu juego > ", torep="1.20.1"),
                "mod_type": winput("Buscar mods para (cliente/servidor/ambos) > ", torep="any").lower(),
                "loader": winput("Ingresa tu modloader (forge/fabric/neoforge) > ", torep="forge").lower()
            }
            config_file.write(json.dumps(config))
    # Variables globales (usando config)
    user_version = config["user_version"] # MC Version
    mod_type = config["mod_type"] # server | client | any 
    loader = config["loader"] # forge | neoforge | fabric

def modgest_config(key:str, val:str): # Cambiar la configuración
    config[key] = val
    reload_config(save=True)

# Funciones de mods

def ask_modrinth(mod_name = "", itering=False): # Descargar un mod de Modrinth
    if __name__ == "__main__" and itering == False:
        cls()
    if mod_name == "":
        return
    hits = search_modrinth(mod_name)
    if hits == None or len(hits) < 1:
        return None
    for mod in hits[::-1]:
        header = f"[{mod['show_mod_id']}] {mod['name']}"
        data_t = remake_string(f"{mod['description']}")
        make_table(data_t, table_header=header, show=True)
    if __name__ == "__main__":
        if not itering:
            jilog("Enter para volver...")
        print()
    if __name__ == "__main__":
        if not itering:
            tololoi = winput("Selecciona un mod > ", torep="RETRN")
            if tololoi != 1:
                if not tololoi.isdigit():
                    return
        else:
            tololoi = 1
        
    else:
        tololoi = 1
    
    selected_mod = hits[int(tololoi) - 1]
    mod_slug = selected_mod["slug"]
    jilog(get_modrinth(mod_slug))
    time.sleep(3)
    return True

def check_comp(mod_data:object, search_result=False): # Verificar la compatibilidad del mod
    try:
        if not search_result:
            if not user_version in mod_data["game_versions"]:
                return False
        else:
            if not user_version in mod_data["versions"]:
                return False
    except Exception as e:
        jilog(f"Error: {e}")
        return False
        
    es_cliente = mod_data["client_side"] 
    es_servidor = mod_data["server_side"]
    if mod_type == "cliente":
        if (es_cliente == "optional") or (es_cliente == "required"):
            return True
        else:
            return False
    elif mod_type == "servidor":
        if (es_servidor == "optional") or (es_servidor == "required"):
            return True
        else:
            return False
    else:
        return True

def search_modrinth(mod_name : str): # Buscar en modrinth
    url = f'https://api.modrinth.com/v2/search?query={mod_name}&facets=[["categories:{loader}"],["versions:{user_version}"]]'
    response = requests.get(url)

    if response.status_code == 200: # Verifica el resultado del request
        mod_data = response.json()
    else:
        return None
    
    if mod_data["total_hits"] < 1: # Si no hay hits
        return None
    
    hits = mod_data["hits"]
    final_hits = []
    lasthit = 0
    for mod in hits:
        temporal_hit = {}
        # ====== Comprobaciones
        if not check_comp(mod, search_result=True):
            continue

        # Data
        lasthit += 1
        temporal_hit["name"] = mod["title"]
        temporal_hit["description"] = mod["description"]
        temporal_hit["author"] = mod["author"]
        temporal_hit["slug"] = mod["slug"]
        temporal_hit["client_side"] = mod["client_side"]
        temporal_hit["server_side"] = mod["server_side"]
        temporal_hit["game_versions"] = mod["versions"]
        temporal_hit["internal_mod_id"] = hits.index(mod)
        temporal_hit["show_mod_id"] = lasthit
        temporal_hit["external_mod_id"] = mod["project_id"]

        # Enviar al hitlist final
        final_hits.append(temporal_hit)
    if len(final_hits) < 1:
        return None
    return final_hits

def get_modrinth(slug : str, modfolder = ""): # Obtener y descargar mediante id/slug
    api_base_route = f"https://api.modrinth.com/v2/project/{slug}"
    base = requests.get(api_base_route).json()
    if not check_comp(base):
        return f"Error, ese mod no es compatible"
    
    api_files_route = f"https://api.modrinth.com/v2/project/{slug}/version?loaders=[\"{loader}\"]&game_versions=[\"{user_version}\"]" # Ruta API
    mod = requests.get(api_files_route).json()
    
    if mod == None or len(mod) < 1:
        return "Mod no disponible"
    
    mod = mod[0] # Actualización más reciente
    file_name = mod["files"][0]["filename"]

    # Descarga el mod
    file_url = mod["files"][0]["url"]


    # Verifica carpeta de mods
    if not os.path.exists(os.path.join(working_directory, "mods")):
        os.mkdir(os.path.join(working_directory, "mods"))

    # Verifica subcarpeta del mod
    if modfolder != "":
        file_folder = os.path.join(working_directory, "mods", modfolder)
    else:
        file_folder = os.path.join(working_directory, "mods")

    # Crear carpeta correspondiente en caso de que no exista
    if not os.path.exists(file_folder):
        os.mkdir(file_folder)

    # Establecer ruta del nuevo archivo
    file_path = os.path.join(file_folder, file_name)
    
    nombre = unquote(file_url.split('/')[-1])
    contenidos = glob(f"{os.path.join(working_directory, "mods")}{os.sep}*.*")
    found = any(nombre in path for path in contenidos)

    if found:
        return f"Mod ya existente: {nombre}"
    else:
        respuesta = requests.get(file_url, stream=True).content

        with open(file_path, "wb") as f:
            f.write(respuesta)

    # Descargar las dependencias
    if len(mod["dependencies"]) > 0:
        jilog(f"Descargando dependencias de {file_name}")
        for dependency in mod["dependencies"]:
            if dependency["dependency_type"] == 'optional':
                continue
            jilog(get_modrinth(dependency["project_id"], modfolder=modfolder))

    return f"{file_name} descargado!" 


# Funciones generales

def modrinth_from_file(filename:str, precise=False): # Descargar con un archivo
    global mf
    if not os.path.exists(filename):
        if not os.path.exists(f"{filename}.txt"):
            print(f"Archivo no encontrado: {filename}")
            time.sleep(3)
            return
        else:
            filename = f"{filename}.txt"
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() == "":
                continue
            if line.startswith("--"):
                mf = line.replace("-- ", "").strip()
                continue
            if precise == False:
                jilog(f"---\nDescargando: {line}")
                ask_modrinth(line, itering=True)
                jilog("---")
            else:
                jilog(f"---\nDescargando: {line}")
                get_modrinth(line.strip(), modfolder=mf)
                jilog("---")
    mf = ""

# Funciones visuales y principales

def visual_main(): # Función visual principal
    cls()
    jilog(f"""[ {loader.capitalize()} {user_version} ]  [ {mod_type.capitalize()} ]
          
[1] Buscar y descargar un mod
[2] Descargar con un nombre preciso
[3] Usar un archivo con nombres de mods
[4] Usar un archivo con nombres precisos
[5] Configuración
[x] Salir
""")
    
    opt = winput("Opción > ")
    if opt == "1": # Preguntar a modrinth
        cls()
        nombre_mod = winput("Ingresa el nombre del mod > ")
        if nombre_mod == "":
            return
        elif ask_modrinth(nombre_mod) == None:
            cls()
            jilog("No se encontraron/seleccionaron mods.")
            time.sleep(3)
    elif opt == "2": # Descargar con un nombre preciso
        cls()
        jilog(get_modrinth(winput("Ingresa el slug/id > ")))
        time.sleep(3)
        cls()
    elif opt == "3": # Archivo con nombres de mods
        cls()
        modrinth_from_file(winput("Ingresa la ruta del archivo > "))
    elif opt == "4": # Archivo con nombres precisos
        cls()
        modrinth_from_file(winput("Ingresa la ruta del archivo > "), precise=True)
        ###
    elif opt == "5": # Configuración
        cls()
        modgest_config("user_version", winput("Ingresa la versión de tu juego > "))
        modgest_config("mod_type", winput("Buscar mods para (cliente/servidor/ambos) > ").lower())
        modgest_config("loader", winput("Ingresa tu modloader (forge/fabric/neoforge) > ").lower())
        reload_config()
        jilog("Configuración modificada.")
        time.sleep(3)
    elif opt == "x":
        cls()
        jilog("Gracias por usar Modgest!")
        os._exit(0)
    else:
        print("Opción inválida.")
        time.sleep(3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Usa la API de Modrinth para descargar archivos más rápido.')
    # Descarga switch
    parser.add_argument('-d', action='store_true', help='Descarga un mod')
    # Especificar modname
    parser.add_argument('--name', type=str, help='El nombre del mod a descargar')
    # Especificar filename
    parser.add_argument('--filename', type=str, help='El nombre del archivo que contiene los nombres de mods') 
    # Config switch
    parser.add_argument('-c', action='store_true', help='Configurar')
    # Especificar key
    parser.add_argument('--key', type=str, help='Valor a configurar')
    # Especificar value
    parser.add_argument('--value', type=str, help='Valor configurado')

    args = parser.parse_args()
    if os.name == "nt":
        os.system(f"title Modgest {modgest_version}")
    if args.c == True: # Sí config
        if args.key == None or args.value == None: # Si ambos están vacíos
            os._exit(0)
        modgest_config(args.key, args.value)
        jilog("Configuración modificada.")
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
    jilog(f"ModGest {modgest_version}")
    time.sleep(1)
    while True:
        visual_main()