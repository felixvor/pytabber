import sys
from cx_Freeze import setup, Executable

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Pytabber",               # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]pytabber.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),

    ("Start Menu",             # Shortcut
     "StartMenuFolder",        # Directory_
     "Pytabber",              # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]pytabber.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),

    ("Run On Windows Startup", # Shortcut
     "StartupFolder",        # Directory_
     "AutoStart Pytabber",         # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]pytabber.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
]


options = {"build_exe":
                {
                    # "packages": ["win32gui", "win32com.client", "keyboard", "threading", "pystray", "screeninfo", "PIL"],
                    "include_files":"./tab-key.ico" ,
                    "optimize": 2
                },
            "bdist_msi":{
                    "data":{
                        "Shortcut": shortcut_table
                    }
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
            icon=r".\tab-key.ico"
            )
        ],
)

# create exe file:
# python setup.py build

# create msi installer:
# python setup.py bdist_msi