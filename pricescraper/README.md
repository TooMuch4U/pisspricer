# Scraper Setup
```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install < pricescraper/requirements.txt
```

# Environment Variables
```bash
pisspricer.name=api@pisspricer.co.nz
pisspricer.password=asjdlasjd
pisspricer.url=http://localhost:4941/api/v1/
```

# Running
Crawl using scraper `newworld`
```bash
scrapy crawl newworld
```
