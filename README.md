# unreal pip
pip wrapper to help installing modules / packages in unreal from pypi.

- uses the unreal python interpreter
- install to site packages folder in engine. 
  - site packages means separate from other default modules in libs
  - by default included in all project

instead of manually filling in all fields, and running a subprocess
`unreal_python_interpreter -m pip [options] modules --target="unreal_site_packages"`

you can simply do:
```python
import unreal_pip
unreal_pip.install(['pyside2'])
```
