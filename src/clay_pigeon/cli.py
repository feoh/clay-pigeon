from pathlib import Path
import tomllib

import atproto
import tomli_w
from cyclopts import App
from rich import print
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.console import Group
from rich.table import Table
from rich.panel import Panel

app = App()


@app.command
def display_profile():
    detailed_profile: atproto.models.AppBskyActorDefs.ProfileViewDetailed = get_profile()
    grid = Table.grid(expand=True)
    grid.add_column(style="red", justify="left")
    grid.add_column(justify="full")

    grid.add_row("Display Name", detailed_profile.display_name)
    grid.add_row("Handle", detailed_profile.handle)
    grid.add_row("Description", detailed_profile.description)
    print(Panel(grid, title="User Profile Information"))
    


def get_client():
    client: atproto.Client = atproto.Client()
    return client


def get_config_file_path() -> str:
    config_dir = Path.home() / ".config" / "clay-pigeon"
    config_file_path = str(config_dir / "config.toml")
    return config_file_path


def get_config() -> dict[str, str]:
    config_file_path = get_config_file_path()
    try:
        with open(config_file_path, "rb") as cf:
            config_dict = tomllib.load(cf)
            return config_dict
    except FileNotFoundError:
        print("[red]No configuration found. Run `clay-pigeon configure` first.[/red]")
        raise


def get_profile():
    client = get_client()
    config_dict = get_config()
    bluesky_username = config_dict["username"]
    bluesky_password = config_dict["password"]
    profile = client.login(bluesky_username, bluesky_password)

    return profile


"""
configure: Write clay-pigeon configuration file

Note: Since users are explicitly asking for this, we overwrite existing configurations.
"""


@app.command
def configure():

    config_dir = Path.home() / ".config" / "clay-pigeon"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = str(config_dir / "config.toml")

    bluesky_username = Prompt.ask("[blue]Bluesky Username[/blue]")
    bluesky_password = Prompt.ask("[red]Bluesky Password[/red]", password=True)

    claypigeon_config = {"username": bluesky_username, "password": bluesky_password}

    try:
        with open(config_file, "wb") as f:
            tomli_w.dump(claypigeon_config, f)
    except OSError as error:
        print(f"[red]Unable to write configuration: {error}[/red]")
        raise


"""
timeline: Diaplay user's timeline
"""


def main() -> None:

    app()


if __name__ == "__main__":
    main()
