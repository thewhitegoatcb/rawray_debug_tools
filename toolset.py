from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

import shutil

app = typer.Typer(help="Debugger toolset")
debugger_app = typer.Typer()
app.add_typer(debugger_app, name="debugger", help="Installer helper")
sourcemap_app = typer.Typer()
app.add_typer(sourcemap_app, name="sourcemap", help="Sourcemap generation helper")

config = None
config_path = None

def configure_app(c):
    import json

    global config_path
    config_path = c

    with open(config_path, 'r') as file:
        global config
        config = json.load(file)

    typer.echo(f"Configuring toolset with config: {config_path}")

def get_game_path():
    global config
    if config and "game_path" in config and config["game_path"]:
        return Path(config["game_path"])
    
def get_rawray_path():
    game_path = get_game_path()
    return game_path / "rawray"

def check_game_install():
    game_path = get_game_path()
    
    if not game_path or not game_path.is_dir():
        typer.echo(f"Couldn't find game path {game_path}, check the config file")
        return False
    return True
    
def check_rawray_install():
    if not check_game_install():
        return False
    
    rawray_path = get_rawray_path()
    if not rawray_path or not rawray_path.is_dir():
        typer.echo(f"RawRay not installed?, run `toolset rawray install`")
        return False
    return True
    
@app.callback()
def main(config: Annotated[Optional[Path], typer.Option(exists=True, readable=True)] = Path("./config.json")):
    """
    Main command-line interface.
    """
    if config:
        configure_app(config)

@debugger_app.command("install", help="Install the debugger addon to RawRay")
def debugger_install():
    if not check_rawray_install():
        return
    
    rawray_path = get_rawray_path()
    
    shutil.copytree("./rawray", rawray_path, dirs_exist_ok=True)
    typer.echo(f"Installed debugger addon at {rawray_path} from ./rawray")

@debugger_app.command("inject", help="Replace the luajit VM with the debugger's luajit VM")
def debugger_inject():
    if not check_rawray_install():
        return

    import helpers.debugger_injector

    game_path = get_game_path()
    rawray_path = get_rawray_path()

    paths = (game_path / 'binaries/lua51.dll', game_path / 'binaries_dx12/lua51.dll')
    luajit2_path = rawray_path / 'addons/debugger/runtime/win32-x64/luajit/luajit.dll'

    for path in paths:
        helpers.debugger_injector.inject(path, luajit2_path)


@debugger_app.command("eject", help="Restore luajit to the original state")
def debugger_eject():
    if not check_rawray_install():
        return

    import helpers.debugger_injector

    game_path = get_game_path()

    paths = (game_path / 'binaries/lua51.dll', game_path / 'binaries_dx12/lua51.dll')
    for path in paths:
        helpers.debugger_injector.eject(path)


@sourcemap_app.command("game", help="Generate game sourcemaps from the bundle files")
def sourcemap_game():
    if not check_game_install():
        return
    
    game_path = get_game_path()

    bundle_path = game_path / "bundle"
    if not bundle_path.is_dir():
        typer.echo(f"No bundle folder found at {bundle_path}, wrong game_path config?")
        return
    
    global config
    sourcemap_path = Path(config["workspace_path"]) / "game"

    import unbundler.main

    unbundler_main = unbundler.main.Main()
    unbundler_main.setup_ljd(Path("./unbundler/ljd/main.py"))
    unbundler_main.parse_all_directory(bundle_path, sourcemap_path, ["^levels/", "^dialogues/generated/"], True)

@sourcemap_app.command("mods", help="Download mods that specified in the config and modifies launch.json in the workspace")
def sourcemap_mods():
    import mod_getter.mod_getter

    getter = mod_getter.mod_getter.ModGetter()
    getter.config_path = config_path
    getter._load_config()
    getter.load_repos()
    getter.load_gh_user_repos()
    getter.instrument_launch_json()

if __name__ == "__main__":
    app()