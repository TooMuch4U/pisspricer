# pisspricer
New Zealand liquor price comparison website

# Scraper Setup
```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install < pricescraper/requirements.txt
```

# Running
Crawl using scraper `newworld` and output to items.json
```bash
cd pricescraper
scrapy crawl newworld -o items.json
```