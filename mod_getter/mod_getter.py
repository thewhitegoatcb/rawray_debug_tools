import git
import pathlib
import sys
import json

class ModGetter:
    GITHUB_API_URL = 'https://api.github.com/users/{0}/repos?per_page={1}'

    def __init__(self) -> None:
        self.config_path = None
        self.config = None

    def _load_config(self):
        with open(self.config_path, 'r') as file:
            self.config = json.loads(file.read())
    
    def _get_repo_path(self, repo_name):
        return pathlib.Path(self.config["local_repos_path"]) / repo_name

    def _make_repos_path(self):
        repos_path = pathlib.Path(self.config["local_repos_path"])
        repos_path.mkdir(parents=True, exist_ok=True)

    def _find_all_script_mod_folders(self):
        repos_path = pathlib.Path(self.config["local_repos_path"])

        found_mods = {}

        for path in repos_path.glob('**/*.mod'):
            mod_name = path.stem

            mod_path = path.parent / "scripts" / "mods" / mod_name
            if not mod_path.is_dir():
                # probably just a bundle packaging leftover, skip
                continue

            if mod_name in found_mods:
                print(f"Mod {mod_name} already exists at {found_mods[mod_name]}, found at {path.parent} Skipping...")
                continue
            
            found_mods[mod_name] = mod_path.absolute()
            print(f"Mod {mod_name} at {mod_path}, found at {path.parent}")

        return found_mods

    def _clone_or_pull(self, clone_url, repo_name):
        repo_path = self._get_repo_path(repo_name).absolute()
        r = None
        try:
            if repo_path.is_dir():
                r = git.Repo(repo_path)
        except git.exc.NoSuchPathError:
            pass

        if r:
            return True
        
        try:
            r = git.Repo.clone_from(clone_url, repo_path)
        except Exception as e:
            print(f"Unexpected error while cloning:{clone_url} to {repo_path} ", sys.exc_info()[0])
                
        if r.is_dirty():
            if self.config["force_pull"]:
                print(f"{repo_name} Needed a force pull because it's dirty!, all changes will be gone")
                r.git.reset('--hard')
                r.remotes.origin.pull()
            else:
                print(f"Skipping pull for: {repo_name} because it's dirty! delete or undo changes to local repo or set \"force_pull\" to true in the config")
                return False
        else:
            print(f"Pulling {repo_name}")
            info = r.remotes.origin.pull()
        return True
    
    def load_gh_user_repos(self):
        from urllib.request import urlopen

        if "github_users" not in self.config:
            return

        self._make_repos_path()
    
        for user, props in self.config["github_users"].items():
            url = ModGetter.GITHUB_API_URL.format(user, self.config["github_max_items"])
            skip_repos = "skip_repos" in props and props["skip_repos"]
            response = urlopen(url)
            data_json = json.loads(response.read())
            
            if not isinstance(data_json, list):
                return
            for repo_data in data_json:
                #updated_at = repo_data['updated_at']
                name = repo_data['name']
                clone_url = repo_data['clone_url']

                if skip_repos and name in skip_repos:
                    print(f"Skipping {name} because it's in skip_repos")
                    continue
                self._clone_or_pull(clone_url, name)

    def load_repos(self):
        if "repos" not in self.config:
            return
        
        self._make_repos_path()

        repos = self.config["repos"]
        for name, repo_url in repos.items():
            self._clone_or_pull(repo_url, name)
    
    def instrument_launch_json(self):
        import mod_getter.launch_helper

        mods = self._find_all_script_mod_folders()
        if not mods:
            path = self.config["local_repos_path"]
            print(f"No mods found at {path}!")
            return
        
        workspace_path = pathlib.Path(self.config["workspace_path"]).absolute()
        if not workspace_path.is_dir():
            print(f"Workspace path at {workspace_path} doesn't exist or not a folder")
            return False
        
        helper = mod_getter.launch_helper.LaunchHelper(workspace_path, mods)
        helper.instrument_launch_json()

    def main(self):
        import argparse

        parser = argparse.ArgumentParser(description='Downloads mod sources')
        parser.add_argument('-c', metavar='--config', type=pathlib.Path, dest="config_path", nargs='?', required=True, help='input config.json file')
        parser.add_argument('-u', dest="update", action='store_true', help='update(pull) mods or clone if do not exist')
        parser.add_argument('-l', dest="instrument", action='store_true', help='look for mod paths in the repo directory and update the launch.json in the workspace directory')

        opts = parser.parse_args()

        self.config_path = opts.config_path
        self._load_config()

        if opts.update:
            self.load_gh_user_repos()
            self.load_repos()
        
        if opts.instrument:
            self.instrument_launch_json()

if __name__ == "__main__":
    getter = ModGetter()
    getter.main()