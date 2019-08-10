import setuptools

setuptools.setup(
    name='QuackTest',
    version='1.0',
    description='Easy testing for Rubber Ducky Scripts',
    author='Trevor Taubitz',
    author_email='terrabitz@protonmail.com',
    packages=['QuackTest'],
    scripts=['bin/quacktest.py', 'bin/quacktest-gui.py'],
    url='https://github.com/terrabitz/QuackTest',
    install_requires=['image', 'pyautogui']
)
