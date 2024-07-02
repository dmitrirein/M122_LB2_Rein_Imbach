import requests
from html_content import html_skript


#API_Key = "6cba7b191454e2da0f71bd1a674b32db"

#lat = 47.376888
#lon = 8.541694

URL = "https://api.openweathermap.org/data/2.5/forecast?lat=47.376888&lon=8.541694&appid=6cba7b191454e2da0f71bd1a674b32db"

response = requests.get(URL)

if response.status_code == 200:
    wetter_daten = response.json()
else:
    print ("Es gab leider einen Fehler!")


temperaturen = [round(elem["main"]["temp_max"] - 273.15, 1) for elem in wetter_daten["list"]]
daten = [elem["dt_txt"].split(" ")[0] for elem in wetter_daten["list"]]
daten = list(set(daten))
daten.sort()

# Maximaltemperaturen pro Tag sammeln
max_temp_pro_tag = {}
for datum in daten:
    tag_temperaturen = [round(elem["main"]["temp_max"] - 273.15, 1) for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    max_temp_pro_tag[datum] = max(tag_temperaturen)


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
with open("Temperatur.html", "w") as file:
    file.write(html_skript)

print("HTML-Datei wurde erfolgreich erstellt: Temperatur.html")