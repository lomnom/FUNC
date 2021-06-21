## Installation:
### MACOS/LINUX:
most projects need this:
```
pip3 install pyyaml
pip3 install json
```
projects that need networking need this
```
pip3 install urllib
pip3 install ndg-httpsclient
pip3 install pyopenssl
pip3 install pyasn1
```
this is basic installation
```
PYPATH=$(python3 -c "import os;print(os.__file__.replace('os.py',''))")
curl https://raw.githubusercontent.com/lomnom/FUNC/main/FUNC.py > "$PYPATH"FUNC.py
```
## Uninstallation:
### MACOS/LINUX:
```
PYPATH=$(python3 -c "import os;print(os.__file__.replace('os.py',''))")
rm "$PYPATH"FUNC.py
```
## how to figure out what anything does
```python
import FUNC as f
help(f)
```
