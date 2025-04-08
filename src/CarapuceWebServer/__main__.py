from Common.WebServerBase import WebServerBase
from CarapuceWebServer.CarapuceLib.Carapuce import Carapuce

def main():
    carapuce : Carapuce = Carapuce()
    webServer : WebServerBase = WebServerBase(carapuce)
    webServer.Run()

if __name__ == "__main__":
    main()