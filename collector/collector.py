import requests, os, json, time
from datetime import datetime, timezone


API_KEY  = {"X-API-Key": "jobboerse-jobsuche"}

BUNDESLAENDER = [
    "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen",
    "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
    "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen",
    "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen",
]
 
KEYWORDS = [
    "IT Support", "Data Analyst", "Business Intelligence",
    "Softwareentwickler", "Systemadministrator", "ERP"
]

OUTPUT_DIR = "data/raw"


def fetch_IT_Jobs(keyword, region, angebotsart=1, page=1, size=100):
  params = {
        "was": keyword,
        "wo": region,
        "angebotsart": angebotsart,
        "page": page,
        "size": size,
    }
  URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
  resp = requests.get(URL, headers=API_KEY, params=params, timeout=10)
  resp.raise_for_status()
  return resp.json()


def save_raw(region, keyword, data):
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
  name = f"{region}_{keyword}".replace(" ", "_")
  path = f"{OUTPUT_DIR}/{name}_{ts}.json"
  with open(path, "w") as f:
    json.dump(data, f)


if __name__ == "__main__":
  for region in BUNDESLAENDER:
    for keyword in KEYWORDS:
      try:
        data = fetch_IT_Jobs(keyword, region)
        save_raw(region, keyword, data)
      except Exception as e:
        print(f"Failed for {region} _ {keyword} : {e}")
      time.sleep(1)
      
      





