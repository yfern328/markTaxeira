import settings.settings as settings
import webdriver.webdriver as webdriver
import analysis.analysis as analysis

def run():
    webdriver.autodrive();
    analysis.write_JSON_to_CSV();

if __name__ == "__main__":
    run()
