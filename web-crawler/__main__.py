from .page import Page

URL_BASE = "https://cdn.star.nesdis.noaa.gov/GOES16/"
PAGE = ""

# conda info --envs

if __name__ == "__main__":
    root_page = Page(URL_BASE, PAGE, crawl_deeper=True, delay=2.0)
    root_page.writeToJSON("output.json")