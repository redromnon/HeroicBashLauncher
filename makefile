
flatpack_dir:=~/.var/app/com.heroicgameslauncher.hgl/config/heroic/
ifneq ("$(wildcard $(flatpack_dir))","")
    launcher_dir:=GameFiles
else
    launcher_dir:=.
endif

all: ${launcher_dir}/HeroicBashLauncher

debug:
	@echo "flatpack dir: $(wildcard $(flatpack_dir))"
	@echo "launcher_dir: ${launcher_dir}"

${launcher_dir}/HeroicBashLauncher: func/*.py
	cd func && pyinstaller HeroicBashLauncher.py --onefile -p $${PWD}
	mv func/dist/HeroicBashLauncher ${launcher_dir}

clean:
	rm -f ${launcher_dir}/HeroicBashLauncher
	rm -f ${launcher_dir}/*.sh
	rm -rf func/build func/dist func/*.spec

