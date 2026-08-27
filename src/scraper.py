import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urlparse


# -----------------------------------
# SETTINGS
# -----------------------------------

sitemap_url = "https://www.gov.uk/sitemap.xml"

headers = {
    "User-Agent": "EducationalDataScraper/1.0"
}


# -----------------------------------
# GET MAIN SITEMAP
# -----------------------------------

response = requests.get(
    sitemap_url,
    headers=headers,
    timeout=10
)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "xml")

sitemap_links = [
    loc.text.strip()
    for loc in soup.find_all("loc")
]

print("Number of sitemaps:", len(sitemap_links))

for link in sitemap_links[:5]:
    print(link)


# -----------------------------------
# GET FIRST SITEMAP
# -----------------------------------

first_sitemap = sitemap_links[0]

response = requests.get(
    first_sitemap,
    headers=headers,
    timeout=10
)

print("\nSitemap Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "xml")

page_urls = [
    loc.text.strip()
    for loc in soup.find_all("loc")
]

print("Number of page URLs:", len(page_urls))

print("\nFirst 5 page URLs:")

for url in page_urls[:5]:
    print(url)


# -----------------------------------
# URL CATEGORY ANALYSIS
# -----------------------------------

paths = []

for url in page_urls:

    path = urlparse(url).path

    if path == "/":
        category = "/"
    else:
        parts = path.strip("/").split("/")
        category = "/" + parts[0] + "/"

    paths.append(category)


category_counts = Counter(paths)

print("\nTop URL categories:")

for category, count in category_counts.most_common(20):
    print(category, ":", count)


# -----------------------------------
# FILTER PUBLICATIONS
# -----------------------------------

publication_urls = [
    url for url in page_urls
    if url.startswith(
        "https://www.gov.uk/government/publications/"
    )
]

print("\nPublication URLs:", len(publication_urls))

print("\nFirst 10 publication URLs:")

for url in publication_urls[:10]:
    print(url)


import random
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

# -----------------------------------
# SETTINGS
# -----------------------------------

TARGET_RECORDS = 500
DELAY = 3

headers = {
    "User-Agent": "EducationalDataScraper/1.0"
}

# Remove duplicate URLs
publication_urls = list(set(publication_urls))

# Random but reproducible selection
random.seed(42)
selected_urls = random.sample(
    publication_urls,
    TARGET_RECORDS
)

print("Total publication URLs:", len(publication_urls))
print("Selected URLs:", len(selected_urls))


# -----------------------------------
# SCRAPING FUNCTION
# -----------------------------------

def scrape_page(url):

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find JSON-LD
        json_ld_tags = soup.find_all(
            "script",
            type="application/ld+json"
        )

        data = None

        for tag in json_ld_tags:

            try:
                temp = json.loads(tag.string)

                if isinstance(temp, dict) and "name" in temp:
                    data = temp
                    break

            except:
                continue

        if data is None:
            return None

        # Title
        title = data.get("name")

        # Description
        description = data.get("description")

        # Published date
        published_date = data.get("datePublished")

        # Updated date
        updated_date = data.get("dateModified")

        # Author / Organisation
        author = data.get("author")

        if isinstance(author, dict):
            author_organisation = author.get("name")
        else:
            author_organisation = None

        # Topic
        about = data.get("about")

        topic_url = None

        if isinstance(about, list):

            for item in about:

                if isinstance(item, dict):

                    same_as = item.get("sameAs")

                    if same_as:
                        topic_url = same_as
                        break

        # Return one record
        return {
            "title": title,
            "description": description,
            "url": url,
            "author_organisation": author_organisation,
            "published_date": published_date,
            "updated_date": updated_date,
            "topic_url": topic_url
        }

    except Exception as e:

        print("Error:", url)
        print(e)

        return None


# -----------------------------------
# SCRAPE 500 PAGES
# -----------------------------------

records = []

for i, url in enumerate(selected_urls, start=1):

    print(
        f"[{i}/{TARGET_RECORDS}] Scraping..."
    )

    record = scrape_page(url)

    if record is not None:

        records.append(record)

        print(
            "  ✓ Success:",
            record["title"][:70]
        )

    else:

        print("  ✗ Failed")

    # Rate limiting
    if i < TARGET_RECORDS:
        time.sleep(DELAY)


# -----------------------------------
# CREATE DATAFRAME
# -----------------------------------

df = pd.DataFrame(records)

print("\nScraping completed.")

print("Successful records:", len(df))

print("\nMissing values:")
print(df.isnull().sum())


# -----------------------------------
# REMOVE DUPLICATES
# -----------------------------------

df = df.drop_duplicates(
    subset=["url"]
)

print(
    "\nRecords after duplicate removal:",
    len(df)
)


# -----------------------------------
# SAVE CSV
# -----------------------------------

df.to_csv(
    "data/govuk_publications.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nCSV saved successfully:"
)

print(
    "data/govuk_publications.csv"
)