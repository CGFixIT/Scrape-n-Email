import mailer  

def main():
    rcpScraper.scrape()
    clistScraper.scrape()

if __name__ == "__main__":
    main()
    mailer.send_all()  


"""
from bs4 import BeautifulSoup
import requests, io, os
import drudgeScraper, rcpScraper, clistScraper

def main():
    #drudgeScraper.scrape()
    rcpScraper.scrape()
    clistScraper.scrape()

if __name__ == "__main__":
    main()
    os.system("email.bat")
    quit()
"""
