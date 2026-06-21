import atproto
from rich.prompt import Prompt
from rich import print
from pathlib import Path
import tomllib
import tomli_w
from cyclopts import App

app = App()

@app.default
def hello(
            configure: str,
         ):
    print("Hello from clay-pigeon!")



config_dir = Path.home() / ".config" / "clay-pigeon"
config_dir.mkdir(parents=True, exist_ok=True)
config_file_path = config_dir / "config.toml"
config_file = str(config_file_path)


def get_client():
    client: atproto.Client = atproto.Client()
    return client

def get_config() -> dict[str,str]:
    with open(config_file,"rb") as cf:
        config_dict = tomllib.load(cf)
        return config_dict


def get_profile():
    client = get_client()
    config_dict = get_config()
    bluesky_username = config_dict['username']
    bluesky_password = config_dict['password']
    profile = client.login(bluesky_username, bluesky_password)
    return profile
    


"""
configure: Write clay-pigeon configuration file

Note: Since users are explicitly asking for this, we overwrite existing configurations.
"""
@app.command
def configure():
    bluesky_username = Prompt.ask("[blue]Bluesky Username[/blue]")
    bluesky_password = Prompt.ask("[red]Bluesky Password[/red]", password=True)

    claypigeon_config = { "username": bluesky_username, "password": bluesky_password }

    with open(config_file, "wb") as f:
        tomli_w.dump(claypigeon_config, f)


"""
timeline: Diaplay user's timeline
"""
@app.command
def timeline():
    client = get_client()
    profile = get_profile()
    # Temporary! Actual logic to print posts coming soon!
    print(profile)

app()
