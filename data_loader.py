
import requests
from bs4 import BeautifulSoup
from sqlalchemy import exists
from sqlite_db import Regions, Provinces, session

class DataLoader:

    __DEFAULT_SOURCE = "https://en.wikipedia.org/wiki/Provinces_of_the_Philippines"

    def __init__(self, source=__DEFAULT_SOURCE):
        self.DATA_SOURCE = source

    '''
        Data gathered based on this XPATH:
        //*[@id="mw-content-text"]/div[1]/table[4]
    '''
    def __download_info(self):

        url = self.DATA_SOURCE
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        content_div = soup.find("div", {"id": "mw-content-text"})

        first_div = content_div.find("div")

        tables = first_div.find_all("table")

        target_table = tables[3]

        row_data = []

        for row in target_table.find_all("tr"):
            cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
            row_data.append(cells)
        
        return row_data
    
    def check_data(self):
        # Data present in the database, skip loading
        has_data_reg = session.query(exists().where(Regions.id != None)).scalar()
        has_data_prov = session.query(exists().where(Provinces.id != None)).scalar()
        return has_data_reg and has_data_prov

    def load_data(self):
        region_downloaded = self.__download_info()
        header_vals = region_downloaded[0]

        regions_proc = [prov[9] for prov in region_downloaded[2:-2]]
        provinces_proc = [(prov[1],prov[9]) for prov in region_downloaded[2:-2]]
        
        distinct_regions = list(set(regions_proc))
        distinct_regions.sort()

        # Save regions and provinces
        if self.__save_regions(distinct_regions):
            self.__save_provinces(provinces_proc)

    def __save_regions(self,regions: list):
        
        for region in regions:
            rg = Regions(region_name=region)
            session.add(rg)
        
        session.commit()

        return True

    def __save_provinces(self,provinces: list):
        
        for province in provinces:
            province_name = province[0]
            province_region = province[1]
            region_info = session.query(Regions).filter_by(region_name=province_region).first()
            # print(province_name, region_info.id)
            prv = Provinces(province_name=province_name,region_id=region_info.id)
            session.add(prv)
        
        session.commit()

if __name__ == "__main__":
     dl = DataLoader()
     if not dl.check_data:
         dl.load_data()