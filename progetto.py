import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

CHIAVE_API = "b4820b2abbe3d0764b71ed2dc1f38453"


def ottieni_meteo(citta):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={citta}&appid={CHIAVE_API}&units=metric&lang=it"
    risposta = requests.get(url)
    dati = risposta.json()

    if risposta.status_code != 200:
        return None

    temperatura = dati["main"]["temp"]
    descrizione = dati["weather"][0]["description"]

    return temperatura, descrizione


def salva_dati(citta, temperatura):
    tempo = datetime.now()

    dataframe = pd.DataFrame([[citta, tempo, temperatura]],
                             columns=["citta", "tempo", "temperatura"])

    dataframe.to_csv("dati.csv", mode="a", header=False, index=False)


def mostra_grafico(citta):
    try:
        dataframe = pd.read_csv("dati.csv", names=["citta", "tempo", "temperatura"])
    except:
        print("Nessun dato salvato.")
        return

    dataframe = dataframe[dataframe["citta"] == citta]

    if dataframe.empty:
        print("Nessun dato per questa città.")
        return

    plt.plot(dataframe["tempo"], dataframe["temperatura"], marker="o")
    plt.title(f"Andamento temperatura - {citta}")
    plt.xlabel("Tempo")
    plt.ylabel("Temperatura (°C)")
    plt.xticks(rotation=45)
    plt.grid(True,linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("aura.png")


# MENU PRINCIPALE
while True:
    print("\n1. Cerca meteo")
    print("2. Mostra grafico")
    print("3. Esci")

    scelta = input("Scelta: ")

    if scelta == "1":
        citta = input("Inserisci città: ")

        risultato = ottieni_meteo(citta)

        if risultato is None:
            print("Città non trovata.")
        else:
            temperatura, descrizione = risultato

            print(f"\nCittà: {citta}")
            print(f"Temperatura: {temperatura}°C")
            print(f"Meteo: {descrizione}")

            salva_dati(citta, temperatura)

    elif scelta == "2":
        citta = input("Inserisci città per grafico: ")
        mostra_grafico(citta)

    elif scelta == "3":
        break

    else:
        print("Scelta non valida.")