from Common.WebServerBase import WebServerBase
from TortankWebServer.Tortank import Tortank

def main():
    tortank : Tortank = Tortank()
    webServer : WebServerBase = WebServerBase(tortank)
    webServer.Run()

if __name__ == "__main__":
    main()