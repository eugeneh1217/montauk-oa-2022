# Scraping + Search Engine

## Usage

1. Setup virtualenv and install requirements from requirements.txt
2. Start server with
```bash
flask run
```
3. Query with (expects server on port 5000)
```bash
python -m recieve
```

## Dev Log

1. inspect page while it loads to find where it gets its data from: https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/
2. scrape and store data
	- decided to go with sqlite for development speed (database can be better decided further into design process)
	- table design 1
		- company
			- ein (primary)
			- name (not null)
		- plan table
			- plan_id (primary)
			- plan (not null)
			- ein (foreign)
		- file location
			- file_id (primary)
			- file_name (not null)
			- location (not null)
			- plan_id (foreign)
	- table design 2
		- file locations
			- id PRIMARY KEY
			- ein
			- company_name
			- plan_name
			- file_location UNIQUE
3. surface with api
	- decided to do search and data organization entirely in sql for speed incase there is a large result from search query
