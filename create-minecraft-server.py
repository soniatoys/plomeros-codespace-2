#!/usr/bin/env python
# coding: utf-8

# In[1]:

# 
# CODE ADAPTED TO PYTHON FROM 'LUCAST' PROJECT: https://github.com/Luc4st1574/MSP_MINECRAFT-SERVER-PROJECT
# 

version = '1.20.4'
# 
# For older versions, you can use fabric or vanilla, forge wont work
# 
# AVAILABLE TESTED VERSIONS:
# - 1.20.4
# - 1.20.3
# - 1.20.2
# - 1.20.1
# - 1.20
# - 1.19.4
# - 1.19.3
# - 1.19.2
# - 1.19.1
# - 1.19
# - 1.18.2
# - 1.18.1
# - 1.18
# - 1.17.1

server_type = 'vanilla'
# 
# To use paper, you must install vanilla first and then install paper
# To use mohist or catserver, you must install forge first and then install mohist or catserver
# To use purpur, you must install fabric first and then install purpur
# 
# AVALIBLE SERVER TYPES:
# - paper (The most optimized server for Spigot/Bukkit)
# - forge (For modded servers)
# - fabric (For modded servers)(Alternative to forge)
# - vanilla (For vanilla servers)
# - snapshot (For testing new features)
# - mohist (For modded servers and plugins) 1.20.1 29/09/24 last version available
# - catserver (For modded servers and plugins) 1.18.2 29/09/24 last version available
# - purpur (For modded servers with fabric and plugins)

# Create main files
import os
import requests
import re
import json
import subprocess

# Create the server directory on the codespace
os.makedirs("Minecraft-server", exist_ok=True)
os.chdir("Minecraft-server")

# Methods
def get_version_fabric(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        versions = response.json()
        for version in versions[:5]:
            if version.get("stable", False):
                return version["version"]
        return versions[0]["version"]
    else:
        print(f"Error al solicitar la API: {api_url}")
        return None

# Internal init...
if server_type == 'paper':
    a = requests.get("https://papermc.io/api/v2/projects/paper/versions/" + version)
    b = requests.get("https://papermc.io/api/v2/projects/paper/versions/" + version + "/builds/" + str(a.json()["builds"][-1]))
    print("https://papermc.io/api/v2/projects/paper/versions/" + version + "/builds/" + str(a.json()["builds"][-1]) + "/downloads/" + b.json()["downloads"]["application"]["name"])
    serverURL = "https://papermc.io/api/v2/projects/paper/versions/" + version + "/builds/" + str(a.json()["builds"][-1]) + "/downloads/" + b.json()["downloads"]["application"]["name"]

# Select the server.jar (url) based on 'server_type'
# if server_type == 'forge':
#     serverURL = "https://serverjars.com/api/fetchJar/modded/forge/" + version
# elif server_type == 'vanilla':
#     serverURL = "https://serverjars.com/api/fetchJar/vanilla/vanilla/" + version
# elif server_type == 'snapshot':
#     serverURL = "https://serverjars.com/api/fetchJar/vanilla/snapshot/" + version
# elif server_type == 'fabric':
#     serverURL = 'https://serverjars.com/api/fetchJar/modded/fabric/' + version
# elif server_type == 'mohist':
#     serverURL = "https://serverjars.com/api/fetchJar/modded/mohist/" + version
# elif server_type == 'catserver':
#     serverURL = "https://serverjars.com/api/fetchJar/modded/catserver/" + version
# elif server_type == 'purpur':
#     serverURL = "https://serverjars.com/api/fetchJar/servers/purpur/" + version

# ServerJars DOWN
# ACTIVE
if server_type == 'forge':
    forge_base_url = "https://maven.minecraftforge.net/net/minecraftforge/forge"
    metadata_url = f"{forge_base_url}/maven-metadata.xml"

    response = requests.get(metadata_url)
    if response.status_code == 200:
        metadata = response.text
        versions = metadata.split('<version>')
        versions = [v.split('</version>')[0] for v in versions[1:]]
        matching_versions = [v for v in versions if v.startswith(version)]
        if matching_versions:
            def version_key(v):
                main_version, sub_version = v.split('-')[0], v.split('-')[1]
                return [int(x) for x in main_version.split('.')] + [int(x) for x in sub_version.split('.')]
            
            latest_matching_version = max(matching_versions, key=version_key)
            serverURL = f"{forge_base_url}/{latest_matching_version}/forge-{latest_matching_version}-installer.jar"
        else:
            serverURL = None
    else:
        serverURL = None

# ACTIVE
elif server_type == 'vanilla':
    manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifest = requests.get(manifest_url).json()
    versions = manifest["versions"]
    for v in versions:
        if v["id"] == version:
            version_manifest_url = v["url"]
            version_manifest = requests.get(version_manifest_url).json()
            serverURL = version_manifest["downloads"]["server"]["url"]
            break
        else:
            serverURL = None

# ACTIVE
elif server_type == 'snapshot':
    manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifest = requests.get(manifest_url).json()
    latest_snapshot = manifest["latest"]["snapshot"]
    for v in manifest["versions"]:
        if v["id"] == latest_snapshot:
            version_manifest_url = v["url"]
            version_manifest = requests.get(version_manifest_url).json()
            serverURL = version_manifest["downloads"]["server"]["url"]
            break
        else:
            serverURL =  None

# ACTIVE    
elif server_type == 'fabric':
    loader_version = get_version_fabric("https://meta.fabricmc.net/v2/versions/loader")
    installer_version = get_version_fabric("https://meta.fabricmc.net/v2/versions/installer")
    if loader_version and installer_version:
        serverURL = f"https://meta.fabricmc.net/v2/versions/loader/{version}/{loader_version}/{installer_version}/server/jar"
    else:
        serverURL = None

# ACTIVE
elif server_type == 'mohist':
    mohist_builds_url = f"https://mohistmc.com/api/v2/projects/mohist/{version}/builds"
    response = requests.get(mohist_builds_url)
    if response.status_code == 200:
        builds = response.json()["builds"]
        serverURL = builds[-1]["url"]
    else:
        serverURL = None

# ACTIVE
elif server_type == 'catserver':
    jenkins_url = f"https://jenkins.rbqcloud.cn:30011/job/CatServer-{version}/lastSuccessfulBuild/api/json"
    response = requests.get(jenkins_url)
    if response.status_code == 200:
        build_info = response.json()
        artifacts = build_info.get('artifacts', [])
        jar_url = None
        
        for artifact in artifacts:
            if artifact['fileName'].endswith('.jar'):
                jar_path = artifact['relativePath']
                jar_url = f"https://jenkins.rbqcloud.cn:30011/job/CatServer-{version}/lastSuccessfulBuild/artifact/{jar_path}"
                break

        if jar_url:
            serverURL = jar_url
        else:
            serverURL = None
    else:
        serverURL = None

# ACTIVE
elif server_type == 'purpur':
    purpur_api = f"https://api.purpurmc.org/v2/purpur/{version}"
    response = requests.get(purpur_api).json()
    if response.status_code == 200:
        latest_build = response["builds"]["latest"]
        serverURL = f"https://api.purpurmc.org/v2/purpur/{version}/{latest_build}/download"
    else:
        serverURL = None

# Download the server.jar based on 'server_type'
jar_name = {'paper': 'server.jar', 'fabric': 'fabric-server-launch.jar', 'forge': 'forge.jar', 'vanilla': 'vanilla.jar', 'snapshot': "snapshot.jar", 'mohist': "mohist.jar", 
            'catserver': "catserver.jar", 'purpur': "purpur.jar"}

print('Downloading the selected server...')

if serverURL:
    print('Dowloading to github codespaces...')
    r = requests.get(serverURL)

    if r.status_code == 200:
        with open(jar_name[server_type], 'wb') as f:
            f.write(r.content)
    else:
        print('Error '+ str(r.status_code) + '! The version you choose does not work.')

# Run on a specific path depending on the server type
if server_type == 'fabric':
    subprocess.run(f'java -jar fabric-server-launch.jar server -mcversion {version} -downloadMinecraft', shell=True, check=True)
elif server_type == 'forge':
    os.chdir("/workspaces/codespaces-jupyter/Minecraft-server")
    subprocess.run('java -jar forge.jar --installServer', shell=True, check=True)
elif server_type == 'vanilla':
    os.chdir("/workspaces/codespaces-jupyter/Minecraft-server")
    subprocess.run('java -jar vanilla.jar --installServer', shell=True, check=True)
    
# Saves the configuration file on the server
colabconfig = {"server_type": server_type, "server_version": version}
with open("colabconfig.json", 'w') as config_file:
    json.dump(colabconfig, config_file)

# print a completion message
print('Done!')

# change eula to true
with open('eula.txt', 'w') as file:
    file.write('eula=true\n')

# Read .env variables
def load_name_by_env_file(variable_name, file_path='../.env'):
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                if line.startswith(variable_name):
                    key, value = line.strip().split('=', 1)
                    return value
    else:
        print(f"Error: {file_path} file not found.")
        return None

NGROK_AUTH_TOKEN = load_name_by_env_file('NGROK_AUTH_TOKEN')
NGROK_REGION = load_name_by_env_file('NGROK_REGION')

# In[1]:
import requests
import time
import os
import re
import json
import glob
import threading
import subprocess

# Update Apt cache
result = subprocess.run(['sudo', 'apt', 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode == 0:
    print("Apt cache successfully updated!")
else:
    print("Apt cache update failed, you might receive stale packages")

# Assign the files to the directory
os.makedirs("/workspaces/codespaces-jupyter/Minecraft-server", exist_ok=True)
os.chdir("/workspaces/codespaces-jupyter/Minecraft-server")

# Import the configuration file
config_path = "/workspaces/codespaces-jupyter/Minecraft-server/colabconfig.json"

if os.path.isfile(config_path):
    with open(config_path) as config_file:
        colabconfig = json.load(config_file)
else:
    colabconfig = {"server_type": "generic"} # Use the default configuration if there the configuration file does not exist
    with open(config_path, 'w') as new_config_file:
        json.dump(colabconfig, new_config_file)

# Instal OpenJDK
version = colabconfig["server_version"]

def installjdk(v, command):
    subprocess.run('sudo apt-get purge openjdk* -y', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proceso = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if proceso.returncode == 0:
        print("OpenJDK version installed:", v)
    else:
        print("Failed to install OpenJDK:", v)

# Check the version of the server and install the corresponding version of OpenJDK
if version < "1.14":
    v = 8
elif version >= "1.14" and version < "1.17":
    v = 11
else:
    v = 17

# Install JDK version based on server version
installjdk(v, 'sudo apt-get install openjdk-' + str(v) + '-jre-headless -y')

# Check the java version
java_ver = subprocess.run(['java', '-version'], stderr=subprocess.PIPE, text=True).stderr
match = re.search(r'version "(\d+\.\d+)', java_ver)
if match:
    java_ver = match.group(1)
else:
    java_ver = "Couldn't determine Java version"
print("Java version installed:", java_ver)

# List of the server types and their respective jar files
jar_list = {'paper': 'server.jar', 'fabric': 'fabric-server-launch.jar', 'generic': 'server.jar', 'forge': 'forge.jar', 'vanilla': 'vanilla.jar', 'snapshot': 'snapshot.jar', 'mohist': "mohist.jar", 'catserver': "catserver.jar", 'purpur': "purpur.jar"}
jar_name = jar_list[colabconfig["server_type"]]

# Java arguments
if colabconfig["server_type"] == "paper":
    server_flags = "-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true"
else:
    server_flags = ""

# JVM Arguments for the server
memory_allocation = "-Xms10G -Xmx10G"

# Tunnel service for the server
tunnel_service = "ngrok"
print("")
print("> Using:", tunnel_service)

if tunnel_service == "ngrok":
    # Verify if pyngrok is installed
    try:
        import pyngrok # type: ignore
    except ImportError:
        subprocess.run(["pip", "install", "pyngrok"], check=True)

    from pyngrok import ngrok, conf # type: ignore

    # v - - - - - - - TOKEN - - - - - - - v
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)

    # v - - - - - - - AVAILABLE REGIONS - - - - - - - v
    conf.get_default().region = NGROK_REGION
    # ap - Asia/Pacific (Singapore)
    # au - Australia (Sydney)
    # eu - Europa (Frankfurt - Alemania)
    # in - India (Mumbai)
    # jp - Japon (Tokyo)
    # sa - South america (São Paulo - Brasil)
    # us - United estates (Ohio)

    # Conect to ngrok
    url = ngrok.connect(25565, 'tcp')
    print('> Server IP: ' + ((str(url).split('"')[1::2])[0]).replace('tcp://', ''))
    print("")

    # If you got the premiun version of ngrok use the comented code below to get a subdomain
    #subdomain = "my-subdomain" # <--- Place your subdomain here inside the quotes
    #url = ngrok.connect(25565, 'tcp', subdomain=subdomain)
    #print('Your server ip is:  ' + url.replace('tcp://', ''))

#If using playit.gg
elif tunnel_service == "playit":
    subprocess.run(["curl", "-SsL", "https://playit-cloud.github.io/ppa/key.gpg"], check=True)
    subprocess.run(["sudo", "apt-key", "add", "key.gpg"], check=True)

    # ADD PLAYIT.GG REPOSITORY
    subprocess.run(["sudo", "curl", "-SsL", "-o", "/etc/apt/sources.list.d/playit-cloud.list", "https://playit-cloud.github.io/ppa/playit-cloud.list"], check=True)

    # UPDATE PACKAGE LIST
    subprocess.run(["sudo", "apt", "update"], check=True)

    # INSTALL PLAYIT.GG
    result = subprocess.run(["sudo", "apt", "install", "playit"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # cHECK if the command was executed successfully
    if result.returncode == 0:
        print("Playit.gg installed")
    else:
        print("Failed to install Playit.gg")

    # Start the server
    print('Starting server...')
    subprocess.run(["playit", "&", "java", "$memory_allocation", "$server_flags", "-jar", "$jar_name", "nogui"], check=True)

    # Get the server IP
    result = subprocess.run(["playit", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Tu ip es: " + result.stdout.decode())

print('Launching server...')

def get_users():
    url = 'https://jsonplaceholder.typicode.com/users'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Updated by request!")
        else:
            print(f"Error making the request. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Connection failed: {e}")

# Funcion for executing get_users() every 10 minutes
def repeat_get_users():
    while True:
        get_users()
        time.sleep(600)  # Wait 10 minutes

# Start the thread for repeat_get_users()
user_thread = threading.Thread(target=repeat_get_users)
user_thread.start()

# Get the configuration file
stype = colabconfig["server_type"]
version = colabconfig["server_version"]

# Print the server type and version
print("You are currently starting minecraft '" + stype + "-"+ version + "'")

# Si el servidor es de tipo Forge antiguo no va a funcionar
if colabconfig["server_type"] == "forge" and colabconfig["server_version"] < "1.17.1":
    print("This forge version is not compatible with the script :(.")

# If the server is a forge server, this will run the server with the forge arguments
if colabconfig["server_type"] == "forge":
    version = colabconfig["server_version"]
    forgefiles = f"/workspaces/codespaces-jupyter/Minecraft-server/libraries/net/minecraftforge/forge/"
    
    forgepreversion = os.listdir(forgefiles)
    
    if forgepreversion:
        forgeversion = forgepreversion[0]
        forgeversionchecked = forgeversion.replace(".jar", "")
        print("Your forge version is: ", forgeversionchecked)
    else:
        print("There was not any forge files.")
    
    pathtoforge = glob.glob(f"/workspaces/codespaces-jupyter/Minecraft-server/libraries/net/minecraftforge/forge/{forgeversionchecked}/unix_args.txt")

    if pathtoforge: 
        path = pathtoforge[0] 
        print(path)
        subprocess.run(f'java @user_jvm_args.txt @{path} "$@"', shell=True)
    else:
        print("No unix_args.txt found.")
else:
    subprocess.run(f'java {memory_allocation} {server_flags} -jar {jar_name} nogui', shell=True)

# Cicle to keep the server running
while True:
    time.sleep(60)
