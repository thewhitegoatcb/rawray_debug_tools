
# RawRay Debugger Toolset

This toolset provides a collection of useful tools for debugging and sourcemap generation in the Stingray game engine.

## Prerequisites

Before using this toolset, make sure you have the following prerequisites installed:

- Python (3.9 or higher): [Official Python Website](https://www.python.org/downloads/)
- Supported Game with RawRay plugin installed: [RawRay](https://github.com/thewhitegoatcb/rawray#installation)
- Lua Debug Extension for Visual Studio Code: [Lua Debug](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug)
- Git: [Download Link](https://git-scm.com/downloads)
## Installation

To install the toolset, unpack [Installation Files](https://github.com/thewhitegoatcb/rawray_debug_tools/releases/)
And install requirments in the unpacked directory by running:
```shell
pip install -r requirements.txt
```

Configure your game's path in `config.json` specified in `game_path`. The default is: `C:/Program Files (x86)/Steam/steamapps/common/Warhammer Vermintide 2`

**Make sure that you use forward slashes**
## Typical Usage

Generate game sourcemaps and download mod sources. The output would be to `{workspace_path}/game` and `{local_repos_path}` configured in `config.json`:
```shell
python toolset.py sourcemap game
python toolset.py sourcemap mods
```
Add the `sourcemap` folder to VSCode Workspace by drag&drop or via `File->Add Folder To Workspace`

<br>

**Make sure the game is NOT running**<br>
Install debugger addon in RawRay:
```shell
python toolset.py debugger install
```

### Starting the game and debugging

1. Run the game in **Modded Realm**, You should see the game pause at a black screen waiting for the debugger.
2. Open VSCode and go to [Run and Debug](https://code.visualstudio.com/docs/editor/debugging),
Select `Stingray Attach (sourcemaps)` from the `RUN AND DEBUG` drop down menu and attach (F5) or click the <span style="color:green">green play button</span> 
3. VSCode should attach to the game and pause

## Debugger

The debugger option allows you to install/remove the addon and manipulate the luajit VM used in RawRay for debugging purposes.

> ### Install
>> The `install` command installs the debugger addon to RawRay.
>> - Usage: `python toolset.py debugger install`

> ### Remove
>> The `remove` command removes the debugger addon from RawRay.
>> - Usage: `python toolset.py debugger remove`

> ### Inject
>>The `inject` command replaces the luajit VM with the debugger's luajit VM. **Not recommended if you want a stable game. This will make the game only playble in modded realm, use `eject` to restore to original state.**
>> - Usage: `python toolset.py debugger inject`

> ### Eject
>> The `eject` command restores the luajit VM to its original state.
>> - Usage: `python toolset.py debugger eject`

## Sourcemap

The sourcemap option enables you to generate game sourcemaps from the bundle files and download mods specified in the config.

> ### Game
>> The `game` command generates game sourcemaps from the bundle files, **needs to be done every game update or on first run**.
>> - Usage: `python toolset.py sourcemap game`

> ### Mods
>> The `mods` command downloads mods specified in the config and modifies the `launch.json` to include the sourcemaps, needs to be done on mod updates and first run.
>> - Usage: `python toolset.py sourcemap mods`

## Supported Games
* Warhammer: Vermintide 2 (Modded Realm only)

## Caveats
* Official Realm will not work if `toolset.py debugger inject` was run, use `toolset.py debugger eject` to restore state
* LJD decompilation isn't perfect. breakpoints might not trigger perfectly or at all if the line info doesn't perfectly match on the function
## Known Issues
* Some asserts and other rare cases can cause the game to pause execution, can be temporarly solved by reattaching the debugger using `Ctrl+Shift+F5`
* Exception catching currenlty disabled in compatibility mode(when not running `inject`) due to some bug that causes to stop execution when they are disabled in VSCode

## Troubleshooting
* Game doesn't pause, check `rawray/rawray.log` at game's path for debugger addon initialization, make sure `debugger.enable = true` at `rawray/config.lua`
## Acknowledgments
* The team at [lua-debug](https://github.com/actboy168/lua-debug), especially [@fesily](https://github.com/fesily) for adding support for luajit and working closely with me to address issues
* [@Manny](https://github.com/ManuelBlanc) from Fatshark studios for being an awesome game dev that's active in the community, also for his PoC [Line Number Adjustment](https://github.com/ManuelBlanc/ljd/tree/feature-match-line-numbers)
* Vermintide Modders Discord Community for all the awesome mods and tools they made over the years
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.