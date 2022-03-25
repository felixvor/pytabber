# pytabber

Windows will only show the ALT-TAB window on the main monitor. If you use multiple displays this can be very annoying.

Run this program in the background and press ALT+q anytime to show program-selection-window on every screen.

#### Installation

[Download latest msi release](https://github.com/DieseKartoffel/pytabber/releases) and install on Windows.

#### Build from Source:

Make sure to run setup.py in a clean (conda) environment, or expect slow and large builds

```
pip install -r requirements.txt
```

- Create an .exe file:
```
python setup.py build
```

- Create an .msi installer for windows:
```
python setup.py build
```
