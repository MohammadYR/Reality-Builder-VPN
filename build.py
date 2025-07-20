import PyInstaller.__main__

PyInstaller.__main__.run([
    'reality_builder/main.py',
    '--name=RealityBuilder',
    '--onefile',
    '--windowed',
    '--add-data=reality_builder/assets;assets',
])
