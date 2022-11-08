#!/usr/bin/env python3
import os
import shutil
from io import StringIO
from unittest import main, mock, TestCase
from unittest.mock import Mock

from func import configpath
from func.settings import args
from func import checkbinary

args = Mock()
args.silent = True

mock_config_null = "{\"defaultSettings\": {\"altLegendaryBin\": \"\"}}"

mock_config = "{\"defaultSettings\": {\"altLegendaryBin\": \"/config/path/to/legendary\"}}"

class TestCheckBinary(TestCase):

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_opt(self):
        shutil.which = Mock()
        shutil.which.return_value = None

        os.path.exists = Mock()
        expected_base_path = "/opt/Heroic"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary ")
        os.path.exists.side_effect = lambda x: expected_base_path in x

        actual_return_path = checkbinary.getbinary("epic")
        os.path.exists.assert_any_call(expected_base_path)
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config)), create=True)
    def test_getbinary_epic_from_config(self):
        shutil.which = Mock()
        shutil.which.return_value = None

        os.path.exists = Mock()
        expected_base_path = "/config/path/to"
        expected_return_path = os.path.join(expected_base_path, "legendary ")
        os.path.exists.side_effect = lambda x: expected_base_path in x

        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_is_flatpak(self):
        shutil.which = Mock()
        shutil.which.return_value = None

        configpath.is_flatpak = Mock()
        configpath.is_flatpak = True
        os.path.exists = Mock()
        expected_base_path = "/app/bin/heroic"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary ")
        os.path.exists.side_effect = lambda x: expected_base_path in x

        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_app(self):
        shutil.which = Mock()
        shutil.which.return_value = None

        configpath.is_flatpak = Mock()
        configpath.is_flatpak = False
        os.path.exists = Mock()
        expected_base_path = "/app/bin/heroic"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary ")
        os.path.exists.side_effect = lambda x: x == expected_base_path or x == os.path.join(expected_base_path, checkbinary.resources_bin_path)

        actual_return_path = checkbinary.getbinary("epic")
        os.path.exists.assert_any_call(expected_base_path)
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_appimage_gamefiles(self):
        shutil.which = Mock()
        shutil.which.return_value = None

        expected_base_path = "/home/user/Games/Heroic/HeroicBashLauncher"
        os.getcwd = Mock()
        os.getcwd.return_value = os.path.join(expected_base_path, "GameFiles")
        configpath.is_flatpak = Mock()
        configpath.is_flatpak = False
        os.path.exists = Mock()
        os.path.exists.side_effect = lambda x: expected_base_path in x

        expected_return_path = os.path.join(expected_base_path, "binaries/legendary ")
        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path

    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_appimage(self):
        shutil.which = Mock()
        shutil.which.return_value = None
        
        expected_base_path = "/home/user/Games/Heroic/HeroicBashLauncher"
        os.getcwd = Mock()
        os.getcwd.return_value = os.path.join(expected_base_path)
        configpath.is_flatpak = Mock()
        configpath.is_flatpak = False
        os.path.exists = Mock()
        os.path.exists.side_effect = lambda x: x == expected_base_path or x == os.path.join(expected_base_path, "binaries")

        expected_return_path = os.path.join(expected_base_path, "binaries/legendary ")
        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path
    
    @mock.patch("builtins.open", Mock(return_value=StringIO(mock_config_null)), create=True)
    def test_getbinary_epic_on_path(self):
        shutil.which = Mock()
        shutil.which.side_effect = lambda x: "/usr/lib64/heroic-games-launcher-bin/heroic" if x == "heroic" else None

        os.path.realpath = Mock()
        os.path.realpath.side_effect = lambda x: "/usr/lib64/heroic-games-launcher-bin/heroic" if x == "/usr/lib64/heroic-games-launcher-bin/heroic" else x

        os.path.exists = Mock()
        expected_base_path = "/usr/lib64/heroic-games-launcher-bin"
        expected_return_path = os.path.join(expected_base_path, checkbinary.resources_bin_path, "legendary ")
        os.path.exists.side_effect = lambda x: expected_base_path in x

        actual_return_path = checkbinary.getbinary("epic")
        assert expected_return_path == actual_return_path


if __name__ == '__main__':
    main()
