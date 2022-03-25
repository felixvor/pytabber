import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
options = {"build_exe":
                {
                    # "packages": ["win32gui", "win32com.client", "keyboard", "threading", "pystray", "screeninfo", "PIL"],
                    "include_files":"./tab-key.ico" ,
                    "optimize": 2
                }
            }


setup(
    name="Pytabber",
    version="0.0.1",
    description="Use ALT+Q to show an app selection window on every monitor",
    options=options,
    executables=[
        Executable("pytabber.py", 
            base="Win32GUI",
            icon=r".\tab-key.ico",
            shortcut_name="PyTabber",
            shortcut_dir="DesktopFolder"
            )
        ],
)

# create exe file:
# python setup.py build

# create msi installer:
# python setup.py bdist_msi