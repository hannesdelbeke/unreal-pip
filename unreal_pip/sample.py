import unreal_pip

required = {'pyside2'}
unreal_pip.install(required)

raise Exception("This is an exception")
