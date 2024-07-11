import requests
from html_content import html_skript
from collections import Counter
from fpdf import FPDF

# Breitengrad und Längengrad für Zürich, Schweiz
lat = 47.376888
lon = 8.541694

# URL für die OpenWeatherMap API mit den angegebenen Koordinaten und API-Schlüssel
URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=6cba7b191454e2da0f71bd1a674b32db"

# Anfrage an die API senden
response = requests.get(URL)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    wetter_daten = response.json()  # JSON-Daten der Antwort extrahieren
else:
    print("Es gab leider einen Fehler!")  # Fehlernachricht ausgeben

# Temperaturen in Celsius umwandeln und abrunden
temperaturen = [round(elem["main"]["temp_max"] - 273.15, 1) for elem in wetter_daten["list"]]

# Datum extrahieren und sortieren
daten = [elem["dt_txt"].split(" ")[0] for elem in wetter_daten["list"]]
daten = list(set(daten))
daten.sort()

# Maximaltemperaturen pro Tag sammeln
max_temp_pro_tag = {}
for datum in daten:
    tag_temperaturen = [round(elem["main"]["temp_max"] - 273.15, 1) for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    max_temp_pro_tag[datum] = max(tag_temperaturen)

# HTML-Skript mit den Daten füllen
for datum, temp in max_temp_pro_tag.items():
    html_skript += f"""
        <tr>
            <td>{datum}</td>
            <td>{temp}</td>
        </tr>
    """

html_skript += """
    </table>
</body>
</html>
"""

# HTML-Datei speichern
with open("Temperatur.html", "w", encoding="utf-8") as file:
    file.write(html_skript)

print("HTML-Datei wurde erfolgreich erstellt: Temperatur.html")

# Informationen für die PDF-Datei sammeln
PDF_Infos = {}
for datum in daten:
    tag_info = {}

    # Maximal- und Minimaltemperaturen des Tages sammeln
    max_tag_temperaturen = [round(elem["main"]["temp_max"] - 273.15, 1) for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    tag_info.update({"temp_max": max(max_tag_temperaturen)})

    min_tag_temperaturen = [round(elem["main"]["temp_min"] - 273.15, 1) for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    tag_info.update({"temp_min": min(min_tag_temperaturen)})

    # Häufigste Wetterkonditionen des Tages sammeln
    Wetter = [elem["weather"][0]["main"] for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    Wetter = Counter(Wetter).most_common(1)[0][0]
    tag_info.update({"weather": Wetter})

    # Beschreibung der häufigsten Wetterkonditionen des Tages sammeln
    Wetter_Description = [elem["weather"][0]["description"] for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    Wetter_Description = Counter(Wetter_Description).most_common(1)[0][0]
    tag_info.update({"description": Wetter_Description})

    PDF_Infos[datum] = tag_info

# Funktion, um ein Dictionary in eine PDF-Datei zu schreiben
def dict_to_pdf(data, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    pdf.output(file_name)

# PDF-Datei erstellen
dict_to_pdf(PDF_Infos, "Wetter.pdf")
