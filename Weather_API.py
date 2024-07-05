import requests
from html_content import html_skript
from collections import Counter
from fpdf import FPDF


load_dotenv()


API_Key = os.getenv("api_key")

#lat = 47.376888
#lon = 8.541694

URL = "https://api.openweathermap.org/data/2.5/forecast?lat=47.376888&lon=8.541694&appid=" + API_Key

response = requests.get(URL)

if response.status_code == 200:
    wetter_daten = response.json()
else:
    print ("Es gab leider einen Fehler!")
     return None




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
with open("Temperatur.html", "w", encoding="utf-8") as file:
    file.write(html_skript)

print("HTML-Datei wurde erfolgreich erstellt: Temperatur.html")

PDF_Infos = {}
for datum in daten:
    tag_info = {}

    max_tag_temperaturen = [round(elem["main"]["temp_max"] - 273.15, 1) for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    tag_info.update({"temp_max": max(max_tag_temperaturen)})

    min_tag_temperaturen = [round(elem["main"]["temp_min"] - 273.15, 1) for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    tag_info.update({"temp_min": min(min_tag_temperaturen)})

    Wetter = [elem["weather"][0]["main"] for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    Wetter = Counter(Wetter).most_common(1)[0][0]
    tag_info.update({"weather": Wetter})

    Wetter_Description = [elem["weather"][0]["description"] for elem in wetter_daten["list"] if elem["dt_txt"].split(" ")[0] == datum]
    Wetter_Description = Counter(Wetter_Description).most_common(1)[0][0]
    tag_info.update({"description": Wetter_Description})


    PDF_Infos[datum] = tag_info




def dict_to_pdf(data, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    
    for key, value in data.items():
        pdf.cell(200, 10, txt = f"{key}: {value}", ln = True)
    
    pdf.output(file_name)


dict_to_pdf(PDF_Infos, "Wetter.pdf")
