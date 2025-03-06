from distutils.core import setup

setup(name="Tortank WebServer",
    version="0.1.0",
    description="An example package for showing how to pip install from a git repo",
    license='MIT',
    author="Matias Codesal",
    authoer_email="matias.codesal@gmail.com",
    url='https://github.com/matiascodesal/git-for-pip-example',
    install_requires=[
        'Flask',
        'threading',
        # 'enum',
        'smbus2',
        'gpiozero'
        # Add other dependencies here
    ]
    # packages=find_packages()
)