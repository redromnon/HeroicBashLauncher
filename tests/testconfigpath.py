


import os
from subprocess import CompletedProcess
import subprocess
from unittest import TestCase
from unittest.mock import Mock

from func import configpath

def mock_subprocess_run_hgl(args, **kwargs):
    stdout = b"com.heroicgameslauncher.hgl\n" if args == ["flatpak", "list", "--columns=application"] else None
    returncode = 0
    return CompletedProcess(args, returncode, stdout)

def mock_subprocess_run_steam(args, **kwargs):
    stdout = b"com.valvesoftware.Steam\n" if args == ["flatpak", "list", "--columns=application"] else None
    returncode = 0
    return CompletedProcess(args, returncode, stdout)

class TestCheckBinary(TestCase):

    def setUp(self):
        subprocess.run = Mock(return_value=CompletedProcess([], returncode=0, stdout=b""))
        os.path.expanduser = Mock(side_effect=lambda path: path.replace('~', "/home/user"))
        os.path.exists = Mock(return_value=False)

    def test_is_flatpak_installed_nothing(self):
        """Tests that no flatpaks are installed when the output is empty"""
        assert configpath.is_flatpak_installed(configpath.HGL_FLATPAK_APPID) == False
        assert configpath.is_flatpak_installed(configpath.STEAM_FLATPAK_APPID) == False

    def test_is_flatpak_installed_non_zero_retcode(self):
        """Tests that is_flatpak_installed returns False when the flatpak command returns a non-zero status."""
        subprocess.run = Mock(return_value=CompletedProcess([], returncode=127, stdout=b""))
        assert configpath.is_flatpak_installed(configpath.HGL_FLATPAK_APPID) == False
        assert configpath.is_flatpak_installed(configpath.STEAM_FLATPAK_APPID) == False
    
    def test_is_flatpak_installed_only_config_exists(self):
        """Tests that is_flatpak_installed returns False when only the config folder exists"""
        os.path.exists.side_effect = lambda path: path == f"/home/user/.var/app/{configpath.HGL_FLATPAK_APPID}"
        assert configpath.is_flatpak_installed(configpath.HGL_FLATPAK_APPID) == False

    def test_is_flatpak_installed_hgl(self):
        """Tests that is_flatpak_installed returns True when Heroic Flatpak is installed and the config folder exists."""
        os.path.exists.side_effect = lambda path: path == f"/home/user/.var/app/{configpath.HGL_FLATPAK_APPID}"
        subprocess.run = Mock(side_effect=mock_subprocess_run_hgl)
        assert configpath.is_flatpak_installed(configpath.HGL_FLATPAK_APPID) == True

    def test_is_flatpak_installed_steam(self):
        """Tests that is_flatpak_installed returns True when Steam Flatpak is installed and the config folder exists."""
        os.path.exists.side_effect = lambda path: path == f"/home/user/.var/app/{configpath.STEAM_FLATPAK_APPID}"
        subprocess.run = Mock(side_effect=mock_subprocess_run_steam)
        assert configpath.is_flatpak_installed(configpath.STEAM_FLATPAK_APPID) == True
