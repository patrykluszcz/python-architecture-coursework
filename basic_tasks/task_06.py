import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from statistics import mean
import matplotlib.pyplot as plt

def fetch_weather_data():
    url = "https://danepubliczne.imgw.pl/api/data/meteo/format/xml"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_weather_data(xml_content):
    try:
        root = ET.fromstring(xml_content)        
        station_winds = defaultdict(list)
        
        for item in root.findall('.//item'):
            station_name = item.find('nazwa_stacji')
            wind_speed = item.find('wiatr_srednia_predkosc')
            
            if station_name is not None and wind_speed is not None and wind_speed.text:
                name = station_name.text
                try:
                    speed = float(wind_speed.text)
                    if speed < 200:  # Filtrowanie błędnych odczytów (np. 999.9)
                        station_winds[name].append(speed)
                except (ValueError, TypeError):
                    continue
        
        return station_winds
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

def create_wind_speed_chart(station_winds):
    if not station_winds:
        return
    
    station_averages = {}
    for station, speeds in station_winds.items():
        if speeds:
            station_averages[station] = mean(speeds)
    
    sorted_stations = sorted(station_averages.items(), key=lambda x: x[1], reverse=True)[:15]
    
    if not sorted_stations:
        return
    
    stations = [s[0] for s in sorted_stations]
    speeds = [s[1] for s in sorted_stations]
    
    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(stations)), speeds, color='steelblue', edgecolor='navy', alpha=0.7)
    
    for i, (bar, speed) in enumerate(zip(bars, speeds)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{speed:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.xlabel('Stacja meteorologiczna', fontsize=12, fontweight='bold')
    plt.ylabel('Średnia prędkość wiatru (m/s)', fontsize=12, fontweight='bold')
    plt.title('Top 15 stacji z najwyższą średnią prędkością wiatru', fontsize=14, fontweight='bold')
    plt.xticks(range(len(stations)), stations, rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()    
    plt.show()

def main():
    xml_data = fetch_weather_data()
    
    if xml_data:
        station_winds = parse_weather_data(xml_data)
        
        if station_winds:
            create_wind_speed_chart(station_winds)
        else:
            print("Nie udało się przetworzyć danych pogodowych")
    else:
        print("Nie udało się pobrać danych pogodowych")

if __name__ == "__main__":
    main()
