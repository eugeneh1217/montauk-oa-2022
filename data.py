from dataclasses import dataclass
import requests
import sqlite3
import time

DB_PATH = "time-benchmark.db"
TIC_BLOB_DOWNLOAD_URL = ("https://transparency-in-coverage.uhc.com"
                         "/api/v1/uhc/blobs/")

@dataclass
class FileLocation:
    ein: int
    comp: str
    plan: str
    loc: str

class FileLocationDB:
    def __init__(self, **connection_args):
        raise NotImplementedError()
    
    def insert_file_location(self, data: FileLocation):
        raise NotImplementedError()

    def search(self, ein=None, comp=None):
        raise NotImplementedError()

    def exit(self):
        raise NotImplementedError()

class SqliteDB(FileLocationDB):
    def _initialize_tables(self):
        self._exec(
            "CREATE TABLE IF NOT EXISTS FILE_LOCATIONS(\n"
            "	FILE_LOC_ID INT PRIMARY KEY,\n"
            "	EIN INT,\n"
            "   COMPANY TEXT,\n"
            "   PLAN TEXT,\n"
            "   FILE_LOC TEXT\n"
            ");"
        )

    def __init__(self, **connection_args):
        self._conn = sqlite3.connect(DB_PATH, **connection_args)
        self._initialize_tables()

    def _exec(self, query):
        return self._conn.execute(query)
    
    def _commit(self):
        return self._conn.commit()
    
    def insert_file_location(self, data: FileLocation):
        self._exec(
            "INSERT INTO FILE_LOCATIONS "
            "(EIN, COMPANY, PLAN, FILE_LOC) "
            f'VALUES ("{data.ein}", "{data.comp}", "{data.plan}", "{data.loc}")'
        )
        self._commit()

    def _search_by(self, key, value):
        return self._exec(
            'SELECT PLAN AS PLAN_NAME, '
            '"{" || GROUP_CONCAT(FILE_LOC, ", ") || "}" AS LOCATION '
            f'FROM FILE_LOCATIONS WHERE {key} = "{value}" '
            "GROUP BY PLAN"
        )

    def search(self, ein: int=None, comp: str=None):
        if ein is None == comp is None:
            return None
        if comp is None:
            res_cur = self._search_by("EIN", ein)
        else:
            res_cur = self._search_by("COMPANY", comp)
        res = res_cur.fetchall()
        res = {comp: locs for comp, locs in res}
        return res
            

    def exit(self):
        self._conn.close()

class DataDownloader:
    def __init__(self, db: FileLocationDB):
        raise NotImplementedError()
    
    def download(self):
        raise NotImplementedError()

class TICDownloader(DataDownloader):
    def __init__(self, db: FileLocationDB):
        self._db = db
        
    def download(self):
        blobs = requests.get(TIC_BLOB_DOWNLOAD_URL)
        blobs.raise_for_status()
        blobs = blobs.json()["blobs"]
        blobs = [blob for blob in blobs if blob["name"].endswith("index.json")]
        for blob in blobs:
            resp = requests.get(blob["downloadUrl"])
            resp.raise_for_status()
            data = resp.json()
            report = data["reporting_structure"][0]["reporting_plans"]
            ein = report[0]["plan_id"]
            comp = data["reporting_entity_name"]
            plan = report["plan_name"]
            for nw_file in data["reporting_structure"][0]["in_network_files"]:
                entry = FileLocation(ein, comp, plan, nw_file["location"])
                self._db.insert_file_location(entry)

if __name__ == "__main__":
    print("initializing db connection...")
    db = SqliteDB()
    downloader = TICDownloader(db)
    print("donwloading data...")
    start = time.time()
    downloader.download()
    end = time.time()
    print("done")
    elapsed_sec = time.gmtime(end - start)
    print(f"time elapsed: {time.strftime('%H:%M:%S', elapsed_sec)}s")
    db.exit()
