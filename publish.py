import pathlib
from zipfile import ZipFile
import sys

argv = sys.argv

if len(sys.argv) != 3:
    print("<lua-debug/publish> <lua-debug-compat/publish>")
    sys.exit(1)

ldbg_modded_path = pathlib.Path(sys.argv[1])
ldbg_compat_path = pathlib.Path(sys.argv[2])

def write_zip_folder(zip, src_path, dst_path):
    src_path = pathlib.Path(src_path)
    dst_path = pathlib.PurePath(dst_path)

    for p in src_path.rglob("*"):
        if p.is_file() and p.suffix != ".pyc":
            rel_path = p.relative_to(src_path)
            zip.write(p, dst_path / rel_path)

with ZipFile('./publish/RawRay_Debug_Tools_.zip', 'w') as zip_object:
    write_zip_folder(zip_object, "./helpers", "rawray_debug_tools/helpers/")
    write_zip_folder(zip_object, "./mod_getter", "rawray_debug_tools/mod_getter/")
    write_zip_folder(zip_object, "./unbundler", "rawray_debug_tools/unbundler/")

    write_zip_folder(zip_object, "./rawray", "rawray_debug_tools/rawray/")

    zip_object.write(str(ldbg_modded_path / "runtime/win32-x64/luajit/luadebug.dll"), "rawray_debug_tools/rawray/addons/debugger/dbg_modded/runtime/win32-x64/luajit/luadebug.dll")
    zip_object.write(str(ldbg_modded_path / "runtime/win32-x64/luajit/luajit.dll"), "rawray_debug_tools/rawray/addons/debugger/dbg_modded/runtime/win32-x64/luajit/luajit.dll")
    write_zip_folder(zip_object, str(ldbg_modded_path / "script"), "rawray_debug_tools/rawray/addons/debugger/dbg_modded/script")

    zip_object.write(str(ldbg_compat_path / "runtime/win32-x64/luajit/luadebug.dll"), "rawray_debug_tools/rawray/addons/debugger/dbg_compat/runtime/win32-x64/luajit/luadebug.dll")
    write_zip_folder(zip_object, str(ldbg_compat_path / "script"), "rawray_debug_tools/rawray/addons/debugger/dbg_compat/script")

    zip_object.write("./sourcemaps/.vscode/launch.json", "rawray_debug_tools/sourcemaps/.vscode/launch.json")
    zip_object.mkdir("rawray_debug_tools/sourcemaps/game/")
    zip_object.mkdir("rawray_debug_tools/sourcemaps/repos/")

    zip_object.write("./__init__.py", "rawray_debug_tools/__init__.py")
    zip_object.write("./config.json", "rawray_debug_tools/config.json")
    zip_object.write("./toolset.py", "rawray_debug_tools/toolset.py")
    zip_object.write("./requirements.txt", "rawray_debug_tools/requirements.txt")

    zip_object.write("./README.md", "rawray_debug_tools/README.md")
    zip_object.write("./LICENSE", "rawray_debug_tools/LICENSE")
