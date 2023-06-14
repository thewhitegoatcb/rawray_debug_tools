import git
import pathlib
import sys
import jstyleson as json

class LaunchHelper:
    def __init__(self, workspace_path, mods) -> None:
        self.workspace_path = workspace_path
        self.mods = mods

    def _filter_sourcemaps(self, source_maps):
        to_remove = []
        for i, source_map in enumerate(source_maps):
            if len(source_map) != 2:
                print(f"Sourcemap at launch.json is invalid, has length of {len(source_map)} when should be 2, idx: {i}")
                continue

            src_path = source_map[0]
            dst_path = source_map[1]
            if not src_path.endswith('*') or not src_path.endswith('*'):
                # complex pattern or no pattern, skip
                continue

            src_path = pathlib.PurePath(src_path.replace('*', ''))
            dst_path = dst_path.replace("${workspaceFolder}", str(self.workspace_path))
            dst_path = pathlib.Path(dst_path.replace('*', ''))

            if not src_path.is_relative_to('scripts/mods'):
                continue
            
            mod_name = src_path.name
            if mod_name not in self.mods:
                continue

            mod_path = self.mods[mod_name]

            if not dst_path.is_dir():
                print(f"Sourcemap at {i} has invalid path {dst_path}, removing")
                to_remove.append(source_map)
                continue

            if mod_path != dst_path:
                print(f"Warning, Sourcemap at {i} with path {dst_path} has different path than repo {mod_path}")

            del self.mods[mod_name]
        
        source_maps[:] = list(filter(lambda m: m not in to_remove, source_maps)) # remove from source maps
    
    def _add_mods_to_sourcemaps(self, source_maps):
        for name, path in self.mods.items():
            src_path = f"scripts/mods/{name}/*"

            dst_path = str(path)
            if path.is_relative_to(self.workspace_path):
                dst_path = dst_path.replace(str(self.workspace_path), "${workspaceFolder}")
            dst_path = dst_path.replace('\\', '/')
            dst_path += "/*"
            source_maps.insert(0, [src_path, dst_path])

    def instrument_launch_json(self):
        launch_json_path = self.workspace_path / ".vscode" / "launch.json"
        if not launch_json_path.is_file():
            print(f"Couldn't find launch.json at {launch_json_path}, wrong path or forgot to generate game source maps?")
            return False
        
        with open(launch_json_path, 'r') as file:
            data = file.read()
            launch = json.loads(data)
            if not launch:
                return False
        
        configurations = "configurations" in launch and launch["configurations"]

        if not configurations:
            print("No confiurations?")
            return False
        
        if len(configurations) > 1:
            print("Supporting exactly one configuration!, using first")

        configuration = configurations[0]

        source_maps = configuration and "sourceMaps" in configuration and configuration["sourceMaps"]
        if not source_maps:
            configuration["sourceMaps"] = {}

        source_maps = configuration["sourceMaps"]
        self._filter_sourcemaps(source_maps)
        self._add_mods_to_sourcemaps(source_maps)
        
        with open(launch_json_path, 'w') as file:
            json.dump(launch, file, indent=4)
        
        return True
