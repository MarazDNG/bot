from conf.spots import *
import os
import yaml


def check_file(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file {path} not found.")


class ConfigManager:
    _config_dir = None
    _profiles = None
    _config_pool = {}

    @classmethod
    def init(cls, config_dir):
        cls._config_dir = config_dir
        cls._profiles = cls._load_profiles()

    @classmethod
    def config_for_player(cls, player_name: str):
        if player_name not in cls._config_pool:
            cls._load_config(player_name)
        return cls._config_pool[player_name]

    @classmethod
    def modify(cls, change: str):
        """
        Modify config file.
        Change is command ie. Consumer:stats:str = r6"
        """
        # change config file
        player_and_keys, value = change.split("=")
        player_and_keys = player_and_keys.strip()
        player_name, unsplitted_keys = player_and_keys.split(":", 1)
        keys = unsplitted_keys.split(":")

        config_file_path = cls._get_config_path(player_name)
        check_file(config_file_path)
        with open(config_file_path, "r") as f:
            config_file = yaml.safe_load(f)

        last_index = len(keys) - 1
        current_dict = config_file
        for i, key in enumerate(keys):
            if i == last_index:
                if isinstance(current_dict[key], dict):
                    raise ValueError("Cannot set value to dict.")
                current_dict[key] = value
            else:
                current_dict = current_dict[key]

        with open(config_file_path, "w") as f:
            yaml.safe_dump(config_file, f)

        # load config file
        cls._load_config(player_name)

    @classmethod
    def _get_config_path(cls, player_name: str):
        return os.path.join(cls._config_dir, f"{player_name}.yaml")

    @classmethod
    def _load_profiles(cls):
        profile_file = os.path.join(cls._config_dir, "profiles.yaml")
        with open(profile_file, "r") as f:
            profiles_yaml = yaml.safe_load(f)
        return profiles_yaml

    @classmethod
    def _get_leveling_profile(cls, profile_name: str):
        return cls._profiles["leveling_profile"][profile_name]

    @classmethod
    def _get_stat_profile(cls, profile_name: str):
        return cls._profiles["stat_profile"][profile_name]

    @classmethod
    def _load_config(cls, player_name: str):
        """Read and load config to _config_pool file and convert spots."""
        config_file_path = cls._get_config_path(player_name)
        check_file(config_file_path)
        with open(config_file_path, "r") as f:
            player_config = yaml.safe_load(f)
        if "leveling_profile" in player_config:
            leveling_profile = player_config["leveling_profile"]
            leveling_plan_yaml: list = cls._get_leveling_profile(leveling_profile)
        else:
            leveling_plan_yaml = player_config["leveling_plan"]
        if "stat_profile" in player_config:
            stat_profile = player_config["stat_profile"]
            stats = cls._get_stat_profile(stat_profile)
            player_config["stats"] = stats

        # insert starting spot to the beginning of the list
        starting_warp = player_config["starting_warp"]
        if starting_warp == "lorencia":
            leveling_plan_yaml.insert(0, "n_BUDGE_DRAGONS")
        elif starting_warp == "elbeland":
            leveling_plan_yaml.insert(0, "n_STRANGE_RABBITS")

        leveling_plan = [globals()[item] for item in leveling_plan_yaml]
        player_config["leveling_plan"] = leveling_plan
        if player_name not in cls._config_pool:
            cls._config_pool[player_name] = player_config
            return
        for k, _ in cls._config_pool[player_name].items():
            cls._config_pool[player_name][k] = player_config[k]
