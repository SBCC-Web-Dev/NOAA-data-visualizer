import requests
import json
import time
from bs4 import BeautifulSoup

class Page:
    def __init__(self, base_url: str, rel_url: str, crawl_deeper=True, visited=None, delay=1.0):
        self.base_url = base_url
        self.rel_url = rel_url
        self.errors: list[str] = []
        self.children: list[Page] = []
        self.delay = delay

        if visited is None:
            visited = set()
        self.visited = visited

        full_url = self.base_url + self.rel_url
        if full_url in self.visited:
            print(f"Skipping already visited URL: {full_url}")
            return
        self.visited.add(full_url)

        print(f"Starting request for: {full_url}")
        try:
            time.sleep(self.delay)
            response = requests.get(full_url)
            soup = BeautifulSoup(response.content, "html.parser")
            self.link_elements = soup.select("a[href]")
            print(f"Successfully fetched: {full_url} ({len(self.link_elements)} links found)")
        except Exception as e:
            self.errors.append(f"Error fetching or parsing {full_url}.\n{e}")
            print(f"Error fetching: {full_url} - {e}")
            self.link_elements = []

        self.num_files = self._countFiles()
        self.num_folders = self._countFolders()
        self.ext_data = self._countFileExtensions()

        self._printErrors()

        if crawl_deeper:
            self.crawlFolders()

    def _countFiles(self) -> int:
        image_count = 0
        for element in self.link_elements:
            try:
                if element.attrs["href"].endswith((".jpg", ".gif", ".mp4")):
                    image_count += 1
            except Exception as e:
                self.errors.append(f"Error in element: {element} in CountFiles().\n{e}")
        print(f"Files found: {image_count}")
        return image_count

    def _countFolders(self) -> int:
        folder_count = 0
        for element in self.link_elements:
            try:
                link = element.attrs["href"]
                if link.endswith("/") and link != "../":
                    folder_count += 1
            except Exception as e:
                self.errors.append(f"Error in element: {element} in CountFolders().\n{e}")
        print(f"Folders found: {folder_count}")
        return folder_count

    def _countFileExtensions(self) -> dict[str, int]:
        extensions: dict[str, int] = dict()
        for element in self.link_elements:
            try:
                if element.attrs["href"].endswith("/"):
                    continue
                hrefSplit = element.attrs["href"].split(".")
                extension = hrefSplit[1]
                if extension not in extensions:
                    extensions[extension] = 1
                else:
                    extensions[extension] += 1
            except Exception as e:
                self.errors.append(f"Error on element: {element} in CountFileExtensions().\n{e}")
        print(f"File extensions found: {extensions}")
        return extensions

    def crawlFolders(self):
        print(f"Crawling folders for: {self.base_url + self.rel_url}")
        for element in self.link_elements:
            link = element.attrs["href"]
            if link.endswith("/") and link != "../":
                full_url = self.base_url + self.rel_url + link
                if full_url not in self.visited:
                    print(f"Descending into folder: {full_url}")
                    time.sleep(self.delay)
                    new_page = Page(self.base_url + self.rel_url, link, crawl_deeper=True, visited=self.visited, delay=self.delay)
                    self.children.append(new_page)

    def getData(self):
        return {
            "baseURL": self.base_url,
            "relURL": self.rel_url,
            "files": self.num_files,
            "folders": self.num_folders,
            "extensions": self.ext_data,
            "children": [
                { (child.base_url + child.rel_url): child.getData() } for child in self.children
            ],
        }

    def writeToJSON(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(
                    {
                        (self.base_url + self.rel_url): self.getData()
                    }, f, indent=4)
            print(f"Data written to {filename}")
        except Exception as e:
            self.errors.append(f"Error in writeToJSON().\n{e}")
            print(f"Error writing to JSON file: {filename} - {e}")

    def _printErrors(self):
        if len(self.errors) != 0:
            print(f"Errors for page: {self.rel_url}")
            for error in self.errors:
                print(error)
