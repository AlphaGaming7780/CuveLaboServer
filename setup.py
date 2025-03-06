from distutils.core import setup

setup(
    name="TortankWebServer",
    version="0.1.0",
    description="An example package for showing how to pip install from a git repo",
    license='MIT',
    author="Triton Supreme",
    authoer_email="matias.codesal@gmail.com",
    url='https://github.com/AlphaGaming7780/TortankWebServer',
    install_requires=[
        'Flask',
        'smbus2',
        'gpiozero'
    ],
    packages=['TortankWebServer'],
    entry_points={ 'console_scripts': ['TortankWebServer = TortankWebServer.__main__' ] }
)