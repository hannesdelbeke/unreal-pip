# Never pip install in Unreal! 😱  
By default, `pip install numpy` from command prompt uses pip installed in `C:/Python37` (from your PATH) instead of the Unreal pip.  
Even if you added the unreal pip to the path, you still have issues.
It checks your site packages in local appdata instead of in the unreal folder.  
You likely use  `pip install numpy --target "C:/unreal_project/Content/Python"` to install to a folder.
This can result in duplicate Python packages installed, since pip doesn't check the unreal folders if the package is already installed.  

Unreal pip addresses these problems:  
- install location
- correct dependency management (avoid duplicate installs)
- use correct pip (python version)

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

## Install
simply copy the `unreal_pip` folder in your unreal site packages path.
