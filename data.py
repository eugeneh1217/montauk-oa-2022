import requests
import sqlite3

DB_PATH = "data.db"

class SqliteDB:
	def _initialize_tables(self):
		self._exec
			"CREATE TABLE IF NOT EXISTS COMPANIES (\n"
			"	EIN INT PRIMARY KEY,\n"
			"	NAME TEXT NOT NULL\n"
			");"
		)
		self._exec(
			"CREATE TABLE IF NOT EXISTS PLANS (\n"
			"	ID INT PRIMARY KEY,\n"
			"	NAME TEXT NOT NULL,\n"
			"	COMPANY_EIN INT NOT NULL,\n"
			"	FOREIGN KEY (COMPANY_EIN) REFERENCES COMPANIES(EIN)\n"
			");"
		)
		self._exec(
			"CREATE TABLE IF NOT EXISTS NETWORK_PRICING_FILE_LOCATIONS (\n"
			"	ID INT PRIMARY KEY,\n"
			"	FILE_LOCATION TEXT NOT NULL,\n"
			"	PLAN_ID INT NOT NULL,\n"
			"	FOREIGN KEY (PLAN_ID) REFERENCES PLANS(ID)\n"
			");"
		)

	def _insert_company(self, name, ein):
		self._exec(f"INSERT OR IGNORE INTO COMPANEIS (EIN, NAME) VALUES ({ein}, {name});")

	def _insert_plan(self, name, company, ein):
		

	def insert_file_location(self, ein, plan, locations):
		pass

	def __init__(self):
		self._conn = sqlite3.connect(DB_PATH)
		self._initialize_tables()

	def _exec(self, query):
		return self._conn.execute(query)

if __name__ == "__main__":
	db = SqliteDB()


