import pathlib
import shutil

def _is_fatshark_binary(path):
    partial_sign_text = b"Fatshark "
    with open(path, 'rb') as file:
        data = file.read()
        return data.find(partial_sign_text) != -1

def _backup(path):
    new_path = path.with_stem(path.stem + "_OG")
    shutil.move(path, new_path)

def eject(path):
    import os
    if _is_fatshark_binary(path):
        print(f"Already restored {path}")
        return
    
    og_path = path.with_stem(path.stem + "_OG")
    if not og_path.is_file():
        print(f"Missing backup at {og_path}")
        return
    
    os.remove(path)
    shutil.move(og_path, path)
    print(f"Restored original luajit at {path}")

def inject(path, luajit2_path):
    if not pathlib.Path(luajit2_path).is_file():
        print(f"Couldn't find debugger's luajit at {luajit2_path}")
        return
    
    if _is_fatshark_binary(path):
        _backup(path)
        print(f"Backed up {path}")

    shutil.copy(luajit2_path, path)
    print(f"Installed debugger's luajit at {path} from {luajit2_path}")

