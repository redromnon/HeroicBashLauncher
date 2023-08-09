#!/usr/bin/env python3
import copy
import os
import json
import shlex
import shutil
from io import StringIO
from unittest import main, mock, TestCase
from unittest.mock import Mock


from func import checkparameters

MOCK_APP_NAME = "TestGameId"

# Mock configpath values
MOCK_GAME_JSON_PATH = "/path/to/gameconfig.json"
MOCK_HEROIC_CONFIG_PATH = "/path/to/heroicconfig.json"
MOCK_STORE_CONFIG_PATH = "/path/to/storeconfig.json"
MOCK_RUNTIME_PATH = "/path/to/runtimes"
MOCK_GOG_INSTALLED_CONFIG_PATH = "/path/to/goginstalled.json"
# mock getbinary paths
MOCK_HEROIC_PATH = "/path/to/heroic"
MOCK_GOGDL_PATH = "/path/to/gog-dl"

# A dictionary to mock environmentOptions for ease of mapping to/from
MOCK_ENVIRONMENT = { "MY_TEST_ENV": "MY_TEST_VALUE" }

# The default heroic config.
MOCK_HEROIC_CONFIG_OBJ = {"defaultSettings": {
    "altLegendaryBin": "",
    "wineVersion": {
        "bin": "/path/to/bin/wine",
        "name": "Wine - Default",
        "type": "wine"
    }
}}

# A "minimal" working config with only the winePrefix populated.
MOCK_GAME_CONFIG_MIN_OBJ = {MOCK_APP_NAME: {"winePrefix": f"/path/to/{MOCK_APP_NAME}/pfx"}}

# A configuration with all value set/enabled (except preferSystemLibs and useSteamRuntime.)
MOCK_GAME_CONFIG_FULL_OBJ = {MOCK_APP_NAME: {
    "autoSyncSaves": True,
    "battlEyeRuntime": True,
    "DXVKFpsCap": 144,
    "eacRuntime": True,
    "enableDXVKFpsLimit": True,
    "enableEsync": True,
    "enableFSR": True,
    "enableFsync": True,
    "enviromentOptions": [
        {'key': env[0], 'value': env[1]} for env in MOCK_ENVIRONMENT.items()
    ],
    "language": "fr",
    "launcherArgs": "launcherArgsValue",
    "maxSharpness": 2,
    "nvidiaPrime": True,
    "offlineMode": True,
    "preferSystemLibs": False,
    "savesPath": "/path/to/saves",
    "showFps": True,
    "showMangohud": True,
    "targetExe": "/path/to/override/exe",
    "useGameMode": True,
    "useSteamRuntime": False,
    "winePrefix": f"/path/to/{MOCK_APP_NAME}/pfx",
    "wineVersion": {
        "bin": "/path/to/game/wine/bin/wine",
        "name": f"Wine - {MOCK_APP_NAME}",
        "type": "wine",
        "lib": "/path/to/game/wine/lib",
        "lib32": "/path/to/game/wine/lib32"
    },
    "wrapperOptions": [{
        "exe": "/my/test/wrapper",
        "args": "--my --test --args"
    }]
}}

# Override wineVersion with Proton.
MOCK_GAME_CONFIG_PROTON_OBJ = copy.deepcopy(MOCK_GAME_CONFIG_FULL_OBJ)
MOCK_GAME_CONFIG_PROTON_OBJ[MOCK_APP_NAME]['wineVersion'] = {
    'bin': "/path/to/proton",
    'name': f"Proton - {MOCK_APP_NAME}",
    'type': "proton"
}

# enable useSteamRuntime in a Proton config
MOCK_GAME_CONFIG_STEAM_RUNTIME_OBJ = copy.deepcopy(MOCK_GAME_CONFIG_PROTON_OBJ)
MOCK_GAME_CONFIG_STEAM_RUNTIME_OBJ[MOCK_APP_NAME]['useSteamRuntime'] = True

# A minimal store config to test the default language
MOCK_STORE_CONFIG_LANGUAGE_OBJ = {'language': 'en'}

MOCK_GOG_INSTALLED_OBJ = {"installed": [{
    "appName": MOCK_APP_NAME,
    "install_path": "/path/to/gog/game"
    }]}
MOCK_GOG_INSTALLED_STR = json.dumps(MOCK_GOG_INSTALLED_OBJ)

def get_mocked_config(filename: str, game_config_obj=MOCK_GAME_CONFIG_MIN_OBJ, heroic_config_obj=MOCK_HEROIC_CONFIG_OBJ, store_config_obj=MOCK_STORE_CONFIG_LANGUAGE_OBJ, gog_installed_obj=MOCK_GOG_INSTALLED_OBJ):
    if filename == MOCK_GAME_JSON_PATH:
        return json.dumps(game_config_obj)
    elif filename == MOCK_HEROIC_CONFIG_PATH:
        return json.dumps(heroic_config_obj)
    elif filename == MOCK_STORE_CONFIG_PATH:
        return json.dumps(store_config_obj)
    elif filename == MOCK_GOG_INSTALLED_CONFIG_PATH:
        return json.dumps(gog_installed_obj)
    else:
        return "{}"

default_mock_open = Mock(side_effect=lambda filename, *args, **
                 kwargs: StringIO(get_mocked_config(filename)))


class TestCheckBinary(TestCase):

    def setUp(self):
        # By default which will return nothing (no heroic on PATH)
        shutil.which = Mock()
        shutil.which.return_value = None

        # Initialize other mocks
        os.path.expanduser = Mock(side_effect=lambda path: path.replace('~', "/home/user"))
        # Treat os.environ like an empty dictionary for testing (no existing values)
        os.environ = {}

        # By default we won't test the flatpak path.
        checkparameters.configpath = Mock()
        checkparameters.configpath.is_flatpak = False
        checkparameters.configpath.is_steam_flatpak = False
        checkparameters.configpath.heroicconfigpath = MOCK_HEROIC_CONFIG_PATH
        checkparameters.configpath.runtimepath = MOCK_RUNTIME_PATH
        checkparameters.configpath.storejsonpath = MOCK_STORE_CONFIG_PATH
        checkparameters.configpath.goginstalledpath = MOCK_GOG_INSTALLED_CONFIG_PATH
        
        # Mock getbinary for epic and gog-dl
        checkparameters.getbinary = Mock(
            side_effect=lambda gametype: MOCK_HEROIC_PATH if gametype == "epic" else MOCK_GOGDL_PATH)

        # Disable zenity and logging output during testing.
        checkparameters.settings.args.silent = True
        checkparameters.logging.disable(checkparameters.logging.CRITICAL)

    @mock.patch("builtins.open", default_mock_open, create=True)
    def test_getparameters_epic_wine_no_args(self):
        """Tests an Epic + Wine game config and store config with "minimal" settings and options selected."""
        expected_environment = {'LD_PRELOAD': ''}
        expected_arguments = [
            MOCK_HEROIC_PATH, 'launch', MOCK_APP_NAME,
            # default language
            "--language", MOCK_STORE_CONFIG_LANGUAGE_OBJ["language"],
            # default winePrefix
            '--wine-prefix', f'\"{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]["winePrefix"]}\"',
            # default wineVersion.bin
            '--wine',  MOCK_HEROIC_CONFIG_OBJ["defaultSettings"]["wineVersion"]["bin"],
        ]
        expected_cloudsync = ''

        actual_environment, actual_arguments, actual_cloudsync = checkparameters.checkparameters(
            MOCK_APP_NAME, MOCK_GAME_JSON_PATH, "epic")
        assert expected_environment == actual_environment
        assert expected_arguments == actual_arguments
        assert expected_cloudsync == actual_cloudsync    
    
    @mock.patch("builtins.open", Mock(side_effect=lambda filename, *args, **kwargs: StringIO(get_mocked_config(filename, game_config_obj=MOCK_GAME_CONFIG_PROTON_OBJ))), create=True)
    def test_getparameters_epic_proton_all_options(self):
        """"Tests an Epic + Wine game using a wineVersion with type 'proton' and all options populated."""
        expected_environment = {
            # showHud
            'DVXK_HUD': 'fps',
            # enableDXVKFpsLimit
            'DXVK_FRAME_RATE': str(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['DXVKFpsCap']),
            # enableFSR
            'WINE_FULLSCREEN_FSR': '1',
            # maxSharpness
            'WINE_FULLSCREEN_FSR_STRENGTH': str(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['maxSharpness']),
            # eacRuntime
            'PROTON_EAC_RUNTIME': f"{MOCK_RUNTIME_PATH}/eac_runtime",
            # battlEyeRuntime
            'PROTON_BATTLEYE_RUNTIME': f"{MOCK_RUNTIME_PATH}/battleye_runtime",
            # nvidiaPrime
            'DRI_PRIME': '1',
            '__NV_PRIME_RENDER_OFFLOAD': '1',
            '__GLX_VENDOR_LIBRARY_NAME': 'nvidia',
            'LD_PRELOAD': '',
            # proton variables
            'STEAM_COMPAT_CLIENT_INSTALL_PATH': '/home/user/.steam/steam',
            'STEAM_COMPAT_DATA_PATH': f'\"{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]["winePrefix"]}\"',
            'STEAM_COMPAT_APP_ID': '0',
            'SteamAppId': '0',
            # MangoHUD config path
            'MANGOHUD_CONFIGFILE': '/home/user/.config/MangoHud/MangoHud.conf'
            }
        # enviromentOptions
        expected_environment = expected_environment | MOCK_ENVIRONMENT
        expected_arguments = [
            # eacRuntime
            #'eac_runtime',
            # battlEyeRuntime
            #'battleye_runtime',
            # wrapperOptions
            MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['wrapperOptions'][0]['exe'],
            # unpack list of wrapper args
            *shlex.split(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['wrapperOptions'][0]['args']),
            # showMangohud
            'mangohud', '--dlsym',
            # useGameMode
            'gamemoderun',
            MOCK_HEROIC_PATH, 'launch', MOCK_APP_NAME,
            # targetExe
            '--override-exe', f"\"{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['targetExe']}\"",
            # offlineMode
            '--offline',
            # language
            '--language', MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]["language"],
            # wineVersion.type == Proton
            "--no-wine",
            '--wrapper "', f"\'{MOCK_GAME_CONFIG_PROTON_OBJ[MOCK_APP_NAME]['wineVersion']['bin']}\'",
            'run"',
            # launcherArgs
            MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['launcherArgs']
        ]
        expected_cloudsync = "/path/to/heroic sync-saves --save-path \"/path/to/saves\" TestGameId -y"
        actual_environment, actual_arguments, actual_cloudsync = checkparameters.checkparameters(
            MOCK_APP_NAME, MOCK_GAME_JSON_PATH, "epic")
        assert expected_environment == actual_environment
        assert expected_arguments == actual_arguments
        assert expected_cloudsync == actual_cloudsync

    @mock.patch("builtins.open", Mock(side_effect=lambda filename, *args, **kwargs: StringIO(get_mocked_config(filename, game_config_obj=MOCK_GAME_CONFIG_STEAM_RUNTIME_OBJ))), create=True)
    def test_getparameters_epic_proton_steam_runtime_all_options(self):
        """Tests an Epic + Proton game config with useSteamRuntime and all options populated."""
        expected_environment = {
            # showHud
            'DVXK_HUD': 'fps',
            # enableDXVKFpsLimit
            'DXVK_FRAME_RATE': str(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['DXVKFpsCap']),
            # enableFSR
            'WINE_FULLSCREEN_FSR': '1',
            # maxSharpness
            'WINE_FULLSCREEN_FSR_STRENGTH': str(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['maxSharpness']),
            # eacRuntime
            'PROTON_EAC_RUNTIME': f"{MOCK_RUNTIME_PATH}/eac_runtime",
            # battlEyeRuntime
            'PROTON_BATTLEYE_RUNTIME': f"{MOCK_RUNTIME_PATH}/battleye_runtime",
            # nvidiaPrime
            'DRI_PRIME': '1',
            '__NV_PRIME_RENDER_OFFLOAD': '1',
            '__GLX_VENDOR_LIBRARY_NAME': 'nvidia',
            'LD_PRELOAD': '',
            # proton variables
            'STEAM_COMPAT_CLIENT_INSTALL_PATH': '/home/user/.steam/steam',
            'STEAM_COMPAT_DATA_PATH': f'\"{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]["winePrefix"]}\"',
            'STEAM_COMPAT_APP_ID': '0',
            'SteamAppId': '0',
            # MangoHUD config path
            'MANGOHUD_CONFIGFILE': '/home/user/.config/MangoHud/MangoHud.conf'
            }
        # enviromentOptions
        expected_environment = expected_environment | MOCK_ENVIRONMENT
        expected_arguments = [
            # eacRuntime
            #'eac_runtime',
            # battlEyeRuntime
            #'battleye_runtime',
            # wrapperOptions
            MOCK_GAME_CONFIG_PROTON_OBJ[MOCK_APP_NAME]['wrapperOptions'][0]['exe'],
            # unpack list of wrapper args
            *shlex.split(MOCK_GAME_CONFIG_PROTON_OBJ[MOCK_APP_NAME]['wrapperOptions'][0]['args']),
            # showMangohud
            'mangohud', '--dlsym',
            # useGameMode
            'gamemoderun',
            MOCK_HEROIC_PATH, 'launch', MOCK_APP_NAME,
            # targetExe
            '--override-exe', f"\"{MOCK_GAME_CONFIG_PROTON_OBJ[MOCK_APP_NAME]['targetExe']}\"",
            # offlineMode
            '--offline',
            # language
            '--language', MOCK_GAME_CONFIG_PROTON_OBJ[MOCK_APP_NAME]["language"],
            # wineVersion.type == Proton + useSteamRuntime
            '--no-wine',
            '--wrapper "', '/home/user/.steam/root/steamapps/common/SteamLinuxRuntime_soldier/run', '--',
            f"\'{MOCK_GAME_CONFIG_PROTON_OBJ[MOCK_APP_NAME]['wineVersion']['bin']}\'", 
            'waitforexitandrun"',
            # launcherArgs
            MOCK_GAME_CONFIG_PROTON_OBJ[MOCK_APP_NAME]['launcherArgs']
        ]
        # autoSyncSaves + savePath
        expected_cloudsync = '/path/to/heroic sync-saves --save-path "/path/to/saves" TestGameId -y'

        actual_environment, actual_arguments, actual_cloudsync = checkparameters.checkparameters(MOCK_APP_NAME, MOCK_GAME_JSON_PATH, "epic")
        assert expected_environment == actual_environment
        assert expected_arguments == actual_arguments
        assert expected_cloudsync == actual_cloudsync
    
    @mock.patch("builtins.open", Mock(side_effect=lambda filename, *args, **kwargs: StringIO(get_mocked_config(filename, game_config_obj=MOCK_GAME_CONFIG_FULL_OBJ))), create=True)
    def test_checkparameters_gog_linux(self):
        """Tests a GOG Linux game with all configuration options enabled."""
        expected_environment = {
            # showHud
            'DVXK_HUD': 'fps',
            # enableDXVKFpsLimit
            'DXVK_FRAME_RATE': str(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['DXVKFpsCap']),
            # enableFSR
            'WINE_FULLSCREEN_FSR': '1',
            # maxSharpness
            'WINE_FULLSCREEN_FSR_STRENGTH': str(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['maxSharpness']),
            # eacRuntime
            'PROTON_EAC_RUNTIME': f"{MOCK_RUNTIME_PATH}/eac_runtime",
            # battlEyeRuntime
            'PROTON_BATTLEYE_RUNTIME': f"{MOCK_RUNTIME_PATH}/battleye_runtime",
            # nvidiaPrime
            'DRI_PRIME': '1',
            '__NV_PRIME_RENDER_OFFLOAD': '1',
            '__GLX_VENDOR_LIBRARY_NAME': 'nvidia',
            'LD_PRELOAD': '',
            # MangoHUD config path
            'MANGOHUD_CONFIGFILE': '/home/user/.config/MangoHud/MangoHud.conf'
        }
        # environmentOptions
        expected_environment = expected_environment | MOCK_ENVIRONMENT
        expected_arguments = ['/my/test/wrapper', '--my', '--test', '--args', 'mangohud', '--dlsym', 'gamemoderun', '/path/to/gog-dl', 'launch', '"/path/to/gog/game"', 'TestGameId', '--override-exe', '"/path/to/override/exe"', '--offline', '--platform=linux', 'launcherArgsValue']
        expected_cloudsync = "/path/to/gog-dl sync-saves --save-path \"/path/to/saves\" TestGameId -y"
        actual_environment, actual_arguments, actual_cloudsync = checkparameters.checkparameters(
            MOCK_APP_NAME, MOCK_GAME_JSON_PATH, "gog-linux")
        assert expected_environment == actual_environment
        assert expected_arguments == actual_arguments
        assert expected_cloudsync == actual_cloudsync

    @mock.patch("builtins.open", Mock(side_effect=lambda filename, *args, **kwargs: StringIO(get_mocked_config(filename, game_config_obj=MOCK_GAME_CONFIG_FULL_OBJ))), create=True)
    def test_checkparameters_epic_wine_custom_libs(self):
        """Tests that an Epic + Wine game with useSystemLibs = False returns the expected values."""
        expected_environment = {
            # showHud
            'DVXK_HUD': 'fps',
            # enableDXVKFpsLimit
            'DXVK_FRAME_RATE': str(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['DXVKFpsCap']),
            # enableFSR
            'WINE_FULLSCREEN_FSR': '1',
            # maxSharpness
            'WINE_FULLSCREEN_FSR_STRENGTH': str(MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['maxSharpness']),
            # enableEsync
            'WINEESYNC': '1', 
            # enableFsync
            'WINEFSYNC': '1',
            # eacRuntime
            'PROTON_EAC_RUNTIME': f"{MOCK_RUNTIME_PATH}/eac_runtime",
            # battlEyeRuntime
            'PROTON_BATTLEYE_RUNTIME': f"{MOCK_RUNTIME_PATH}/battleye_runtime",
            # nvidiaPrime
            'DRI_PRIME': '1',
            '__NV_PRIME_RENDER_OFFLOAD': '1',
            '__GLX_VENDOR_LIBRARY_NAME': 'nvidia',
            'LD_PRELOAD': '',
            'ORIG_LD_LIBRARY_PATH': '',
            'LD_LIBRARY_PATH': f"{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['wineVersion']['lib']}:{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['wineVersion']['lib32']}",
            'GST_PLUGIN_SYSTEM_PATH_1_0': f"{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['wineVersion']['lib']}/gstreamer-1.0:{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['wineVersion']['lib32']}/gstreamer-1.0",
            'WINEDLLPATH': f"{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['wineVersion']['lib']}/wine:{MOCK_GAME_CONFIG_FULL_OBJ[MOCK_APP_NAME]['wineVersion']['lib32']}/wine",
            # MangoHUD config path
            'MANGOHUD_CONFIGFILE': '/home/user/.config/MangoHud/MangoHud.conf'
        }
        # environmentOptions
        expected_environment = expected_environment | MOCK_ENVIRONMENT
        expected_arguments = ['/my/test/wrapper', '--my', '--test', '--args', 'mangohud', '--dlsym', 'gamemoderun', '/path/to/heroic', 'launch', 'TestGameId', '--override-exe', '"/path/to/override/exe"', '--offline', '--language', 'fr', '--wine-prefix', '"/path/to/TestGameId/pfx"', '--wine', '/path/to/game/wine/bin/wine', 'launcherArgsValue']
        expected_cloudsync = "/path/to/heroic sync-saves --save-path \"/path/to/saves\" TestGameId -y"
        actual_environment, actual_arguments, actual_cloudsync = checkparameters.checkparameters(
        MOCK_APP_NAME, MOCK_GAME_JSON_PATH, "epic")
        assert expected_environment == actual_environment
        assert expected_arguments == actual_arguments
        assert expected_cloudsync == actual_cloudsync
if __name__ == '__main__':
    main()
