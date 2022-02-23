# Scraper Spider
Web spider using the scrapy framework
### Setup
```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install < pricescraper/requirements.txt
```

### Environment Variables
```bash
pisspricer.name=api@pisspricer.co.nz
pisspricer.password=asjdlasjd
pisspricer.url=http://localhost:4941/api/v1/
```

### Running
Crawl using scraper `newworld`
```bash
scrapy crawl newworld
```

# ScrAPI
Basic NestJS api that serves the summary log files created by the scraper.
### Install
```bash
cd api
npm i
```

### Environment Variables
```bash
HTTP_BASIC_USER=myusername
HTTP_BASIC_PASS=password123
```

### Run
```bash
npm run start
```


