import pandas as pd
import matplotlib.pyplot as plt
import math
from urllib.request import urlopen

print("Grafische Darstellung von Infektionsdaten")
print("-----------------------------------------\n")
print("Dieses Programm erzeugt ein Diagramm mit aktuellen Meldedaten\nder letzten Tage. Geben Sie an, welche Bundesländer im Diagramm\nberücksichtigt werden sollen\n")
print("Verwenden Sie die folgenden Kürzel:\n")

bundeslaender = {
    "SH": "Schleswig Holstein",
    "HH": "Hamburg",
    "NI": "Niedersachsen",
    "HB": "Bremen",
    "NW": "Nordrhein-Westfalen",
    "HE": "Hessen",
    "RP": "Rheinland-Pfalz",
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "SL": "Saarland",
    "BB": "Brandenburg",
    "MV": "Mecklenburg-Vorpommern",
    "SN": "Sachsen",
    "ST": "Sachen-Anhalt",
    "TH": "Thüringen",
    "BE": "Berlin"
}
# print("SH - Schleswig Holstein\nHH - Hamburg\nNI - Niedersachsen\nHB - Bremen\nNW - Nordrhein-Westfalen\nHE - Hessen\nRP - Rheinland-Pfalz\nBW - Baden-Württemberg\n"
#       "BY - Bayern\nSL - Saarland\nBB - Brandenburg\nMV - Mecklenburg-Vorpommern\nSN - Sachsen\nST - Sachen-Anhalt\nTH - Thüringen\nBE - Berlin\n")
for i in bundeslaender:
    print(i, "-", bundeslaender[i])

bundeslaender_auswahl = None
input_nicht_korrekt = True

while input_nicht_korrekt:
    bundeslaender_auswahl = \
        input("\nGeben Sie die Kürzel der darzustellenden Bundesländer mit Leerzeichen\ngetrennt ein: ")
    bundeslaender_auswahl = bundeslaender_auswahl.upper().split(" ")
    input_nicht_korrekt = False

    bundeslaender_auswahl = list(filter(None, bundeslaender_auswahl))

    for bundesland in bundeslaender_auswahl:
        if bundesland not in bundeslaender.keys():
            print('{} ist kein Kürzel für ein Bundesland!'.format(bundesland))
            input_nicht_korrekt = True
            break
        else:
            print(bundesland, bundeslaender[bundesland], '✓')

url = "https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-state.csv"
with open("file.csv", "wb") as file:
    file.write(urlopen(url).read())
print("\nCSV-Datei wurde heruntergeladen und gespeichert.")

daten_df = pd.read_csv("file.csv")
daten_df.columns = [header.replace("DE-", "") for header in daten_df.columns]

benoetigte_daten_df = daten_df[bundeslaender_auswahl]

datumsangaben = daten_df.iloc[:, 0].tolist()
datumsangaben = [datum[:10] for datum in datumsangaben]
x_werte = [i for i in range(len(datumsangaben))]

ticks = 6
anzahl_werte = len(x_werte)
werte_bis_tick = math.floor(anzahl_werte / ticks)

for bundesland in range(len(bundeslaender_auswahl)):
    plt.plot(x_werte,
             benoetigte_daten_df[bundeslaender_auswahl[bundesland]].tolist(),
             label=bundeslaender[bundeslaender_auswahl[bundesland]])

    plt.xticks(x_werte[::werte_bis_tick], datumsangaben[::werte_bis_tick])

plt.title("Aktuelle Covid-19-Fallzahlen")
plt.xlabel("Datum")
plt.ylabel("Anzahl")
plt.legend(loc='upper left')
plt.savefig("plot.pdf")

print("\nPlot erstellt und gespeichert.")

plt.show()
