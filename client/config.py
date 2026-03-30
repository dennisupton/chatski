from pathlib import Path
import tomli_w
import tomllib

configFolderDir = Path("~/.config/chatski").expanduser()

username = None
serverIP = None
def checkConfig():
    global username, serverIP
    configDir = Path("~/.config/chatski/client.toml").expanduser()
    if configDir.exists():
        try:
            with open(configDir, "rb") as f:
                data = tomllib.load(f)
            
            username = data["client"]["username"]
            serverIP = (data["client"]["serverIP"] , int(data["client"]["serverPort"]))
            
        except FileNotFoundError:
            createNewConfig()
        except tomli.TOMLDecodeError:
            createNewConfig()
    else:
        createNewConfig()

def createNewConfig():
    print("\033[2J\033[H", end="", flush=True)
    print("Config not found")
    print("Creating new config : ")
    config = {
        "client": {
            "username": input("Username: "),
            "serverIP": input("Server IP: "),
            "serverPort": input("Server Port: ")
        }
    }
    configFolderDir.mkdir(parents=True, exist_ok=True)

    with open(configFolderDir/ "client.toml", "wb") as f:
        tomli_w.dump(config, f)

