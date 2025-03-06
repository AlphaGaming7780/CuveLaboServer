from setuptools import setup, find_packages

NAME = 'TortankWebServer'
VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name=NAME, 
    version=VERSION,
    author="Triton Supreme",
    author_email="<youremail@email.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url='https://github.com/AlphaGaming7780/TortankWebServer',
    install_requires=[
        'Flask',
        'smbus2',
        'gpiozero'
    ],
    entry_points={
        'console_scripts': 
        [
            'TortankWebServer=TortankWebServer.__main__:main' 
        ] 
    },
    include_dirs=["static"],
)