# my_package/main.py
from .TortankWebServer.server import main

def start():
    print("__main__")
    main()

if __name__ == "__main__":
    start()