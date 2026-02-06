import requests
import threading

BASE_URL = "http://universities.hipolabs.com/search?country="

countries = [
    "Poland", "Germany", "France", "Spain", "Italy",
    "Norway", "Sweden", "Finland", "Denmark", "Netherlands",
    "Belgium", "Austria", "Czech Republic", "Slovakia",
    "Hungary", "Portugal", "Ireland", "Greece",
    "Switzerland", "Croatia"
]

results = {}
lock = threading.Lock()


def fetch_universities(country):
    response = requests.get(BASE_URL + country)
    data = response.json()

    universities = [uni["name"] for uni in data]

    with lock:
        results[country] = universities


threads = []

for country in countries:
    thread = threading.Thread(
        target=fetch_universities,
        args=(country,)
    )
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

for country, universities in results.items():
    print(f"{country}: {universities}")
