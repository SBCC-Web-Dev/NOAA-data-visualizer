from .page import Page

URL_BASE = "https://cdn.star.nesdis.noaa.gov/GOES16/"
PAGE = ""
DELAY = 1
OUT_FILE = "output.json"

if __name__ == "__main__":
    root_page = Page(URL_BASE, PAGE, delay=DELAY)
    root_page.writeToJSON(OUT_FILE)