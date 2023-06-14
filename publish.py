import pathlib
from zipfile import ZipFile
import sys

argv = sys.argv

if len(sys.argv) != 2:
    print("Missing lua-debug publish path!")
    sys.exit(1)

ldbg_path = pathlib.Path(sys.argv[1])

def write_zip_folder(zip, src_path, dst_path):
    src_path = pathlib.Path(src_path)
    dst_path = pathlib.PurePath(dst_path)

    for p in src_path.rglob("*"):
        if p.is_file():
            rel_path = p.relative_to(src_path)
            zip.write(p, dst_path / rel_path)

with ZipFile('./publish/publish.zip', 'w') as zip_object:
    write_zip_folder(zip_object, "./helpers", "rawray_debug_tools/helpers/")
    write_zip_folder(zip_object, "./mod_getter", "rawray_debug_tools/mod_getter/")
    write_zip_folder(zip_object, "./unbundler", "rawray_debug_tools/unbundler/")

    write_zip_folder(zip_object, "./rawray", "rawray_debug_tools/rawray/")
    zip_object.write(str(ldbg_path / "runtime/win32-x64/luajit/luadebug.dll"), "rawray_debug_tools/rawray/addons/debugger/runtime/win32-x64/luajit/luadebug.dll")
    zip_object.write(str(ldbg_path / "runtime/win32-x64/luajit/luajit.dll"), "rawray_debug_tools/rawray/addons/debugger/runtime/win32-x64/luajit/luajit.dll")
    write_zip_folder(zip_object, str(ldbg_path / "script"), "rawray_debug_tools/rawray/addons/debugger/script")

    zip_object.write("./sourcemaps/.vscode/launch.json", "rawray_debug_tools/sourcemaps/.vscode/launch.json")
    zip_object.write("./sourcemaps/game/.gitkeep", "rawray_debug_tools/sourcemaps/game/.gitkeep")
    zip_object.write("./sourcemaps/repos/.gitkeep", "rawray_debug_tools/sourcemaps/repos/.gitkeep")

    zip_object.write("./__init__.py", "rawray_debug_tools/__init__.py")
    zip_object.write("./config.json", "rawray_debug_tools/config.json")
    zip_object.write("./toolset.py", "rawray_debug_tools/toolset.py")
    zip_object.write("./requirements.txt", "rawray_debug_tools/requirements.txt")

    zip_object.write("./README.md", "rawray_debug_tools/README.md")
    zip_object.write("./LICENSE", "rawray_debug_tools/LICENSE")
