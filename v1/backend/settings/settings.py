import dotenv

def greeting():
    print("Import settings.py to auto-load ENV variables!")

def autoLoadSettings():
    dotenv.load_dotenv()
    print("Loaded settings from settings.py!");

#when this is imported it automatically runs autoLoadSettings
if __name__ == "__main__":
    greeting()
else:
    autoLoadSettings()
