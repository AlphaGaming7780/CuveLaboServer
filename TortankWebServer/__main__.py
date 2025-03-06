# my_package/main.py
from .server import main

def start():
    main()

if __name__ == "__main__":
    print("__main__")
    start()