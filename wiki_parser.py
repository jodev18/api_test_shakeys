
import requests
from bs4 import BeautifulSoup

class DataLoader:

    __DEFAULT_SOURCE = "https://en.wikipedia.org/wiki/Provinces_of_the_Philippines"

    def __init__(self, source=__DEFAULT_SOURCE):
        self.DATA_SOURCE = source

    '''
        Data gathered based on this XPATH
    '''
    def _download_info(self):

        url = self.DATA_SOURCE
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        content_div = soup.find("div", {"id": "mw-content-text"})

        first_div = content_div.find("div")

        tables = first_div.find_all("table")

        # Get the 4th table (index 3)
        target_table = tables[3]

        row_data = []

        # Example: Extract all rows
        for row in target_table.find_all("tr"):
            cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
            row_data.append(cells)
        
        return row_data

    def 
