#Build HeroicBashLauncher executable using Pyinstaller
cd func && pyinstaller HeroicBashLauncher.py --onefile --strip
cp dist/HeroicBashLauncher ~/Games/Heroic/HeroicBashLauncher