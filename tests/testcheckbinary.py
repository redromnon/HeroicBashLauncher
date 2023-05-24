#!/usr/bin/env python3
import os
import json
import shutil
from io import StringIO
from unittest import main, mock, TestCase
from unittest.mock import Mock

from func import checkbinary

mock_config_null = json.dumps({ "defaultSettings": { "altLegendaryBin": "" } })

mock_config_obj = {"defaultSettings": {"altLegendaryBin": "/config/path/to/legendary"}}
mock_config_str = json.dumps(mock_config_obj)

class TestCheckBinary(TestCase):

    def setUp(self):
        # By default which will return nothing (no heroic on PATH)
        shutil.which = Mock()
        shutil.which.return_value = None

        # Initialize other mocks
        os.getcwd = Mock()
        os.path.exists = Mock()
        os.path.realpath = Mock()

        # By default we won't test the flatpak path.
        checkbinary.configpath = Mock() 
        checkbinary.configpath.is_flatpak = False

        checkbinary.args.silent = True

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_opt(self):
        """Tests getting the path to legendary from the system /opt/Heroic path."""
        expected_base_path = "/opt/Heroic"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary")
        os.path.exists.side_effect = lambda x: expected_base_path in x

        actual_return_path = checkbinary.getbinary("epic")
        os.path.exists.assert_any_call(expected_base_path)
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_str)), create=True)
    def test_getbinary_epic_from_config(self):
        expected_return_path = mock_config_obj["defaultSettings"]["altLegendaryBin"]
        expected_base_path = os.path.dirname(expected_return_path)
        os.path.exists.side_effect = lambda x: expected_base_path in x

        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_is_flatpak(self):
        """Tests getting the Flatpak path to legendary based on configpath setting."""
        checkbinary.configpath.is_flatpak = True

        expected_base_path = "/app/bin/heroic"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary")
        # Path does not exist on host when using flatpak
        os.path.exists.return_value = False

        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_app(self):
        """Tests getting legendary from the system-wide /app/bin/heroic path"""
        expected_base_path = "/app/bin/heroic"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary")
        os.path.exists.side_effect = lambda x: x == expected_base_path or x == os.path.join(expected_base_path, checkbinary.resources_bin_path)

        actual_return_path = checkbinary.getbinary("epic")
        os.path.exists.assert_any_call(expected_base_path)
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_appimage_gamefiles(self):
        """Tests the AppImage path for getting legendary when running from the GameFiles folder."""
        expected_base_path = "/home/user/Games/Heroic/HeroicBashLauncher"
        os.getcwd.return_value = os.path.join(expected_base_path, "GameFiles")
        os.path.exists.side_effect = lambda x: expected_base_path in x

        expected_return_path = os.path.join(expected_base_path, "binaries/legendary")
        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_appimage(self):
        """Tests the AppImage path for getting legendary when running from the HeroicBashLauncher folder."""
        expected_base_path = "/home/user/Games/Heroic/HeroicBashLauncher"
        os.getcwd.return_value = os.path.join(expected_base_path)
        os.path.exists.side_effect = lambda x: x == expected_base_path or x == os.path.join(expected_base_path, "binaries")

        expected_return_path = os.path.join(expected_base_path, "binaries/legendary")
        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path
    
    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_on_path(self):
        """Tests finding the legendary binary when heroic exists on the user's PATH"""
        shutil.which.side_effect = lambda x: "/usr/lib64/heroic-games-launcher-bin/heroic" if x == "heroic" else None
        os.path.realpath.side_effect = lambda x: "/usr/lib64/heroic-games-launcher-bin/heroic" if x == "/usr/lib64/heroic-games-launcher-bin/heroic" else x
        expected_base_path = "/usr/lib64/heroic-games-launcher-bin"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary")
        os.path.exists.side_effect = lambda x: expected_base_path in x

        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_is_flatpak_and_on_path(self):
        """When Heroic is installed on the system and on Flatpak, we should perfer the Flatpak."""
        checkbinary.configpath.is_flatpak = True
        shutil.which.side_effect = lambda x: "/usr/lib64/heroic-games-launcher-bin/heroic" if x == "heroic" else None
        os.path.realpath.side_effect = lambda x: "/usr/lib64/heroic-games-launcher-bin/heroic" if x == "/usr/lib64/heroic-games-launcher-bin/heroic" else x


        expected_base_path = "/app/bin/heroic"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary")

        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path

if __name__ == '__main__':
    main()
