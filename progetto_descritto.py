# Importa la libreria requests, usata per fare richieste a siti/API su internet
import requests

# Importa pandas con il nome abbreviato pd
# Pandas serve per lavorare con tabelle e file CSV
import pandas as pd

# Importa matplotlib.pyplot con il nome plt
# Serve per creare grafici
import matplotlib.pyplot as plt

# Importa datetime dalla libreria datetime
# Serve per ottenere data e ora attuali
from datetime import datetime


# Salva la chiave API di OpenWeatherMap in una variabile
# Questa chiave serve per poter usare il servizio meteo
CHIAVE_API = "b4820b2abbe3d0764b71ed2dc1f38453"


# Definisce una funzione chiamata ottieni_meteo
# La funzione riceve il nome di una città
def ottieni_meteo(citta):

    # Costruisce l'URL per chiamare l'API meteo
    # Inserisce il nome della città e la chiave API
    # units=metric -> temperatura in gradi Celsius
    # lang=it -> descrizione meteo in italiano
    url = f"http://api.openweathermap.org/data/2.5/weather?q={citta}&appid={CHIAVE_API}&units=metric&lang=it"

    # Invia una richiesta GET all'API
    risposta = requests.get(url)

    # Converte la risposta ricevuta in formato JSON (dizionario Python)
    dati = risposta.json()

    # Controlla se il server ha risposto con errore
    # status_code 200 significa "tutto ok"
    if risposta.status_code != 200:

        # Se c'è un errore restituisce None
        return None

    # Prende la temperatura dal JSON ricevuto
    temperatura = dati["main"]["temp"]

    # Prende la descrizione del meteo dal JSON
    descrizione = dati["weather"][0]["description"]

    # Restituisce temperatura e descrizione
    return temperatura, descrizione


# Definisce una funzione per salvare i dati
# Riceve città e temperatura
def salva_dati(citta, temperatura):

    # Ottiene data e ora attuali
    tempo = datetime.now()

    # Crea una tabella pandas con una sola riga
    # Dentro ci sono città, tempo e temperatura
    dataframe = pd.DataFrame([[citta, tempo, temperatura]],

                             # Definisce i nomi delle colonne
                             columns=["citta", "tempo", "temperatura"])

    # Salva i dati nel file dati.csv
    # mode="a" -> aggiunge dati senza cancellare i precedenti
    # header=False -> non scrive i nomi delle colonne
    # index=False -> non salva i numeri delle righe
    dataframe.to_csv("dati.csv", mode="a", header=False, index=False)


# Definisce una funzione che mostra un grafico
# Riceve il nome della città
def mostra_grafico(citta):

    # Prova ad aprire il file dati.csv
    try:

        # Legge il file CSV e lo trasforma in un DataFrame
        dataframe = pd.read_csv("dati.csv", names=["citta", "tempo", "temperatura"])

    # Se succede un errore entra qui
    except:

        # Stampa un messaggio di errore
        print("Nessun dato salvato.")

        # Esce dalla funzione
        return

    # Filtra il DataFrame
    # Tiene solo le righe della città scelta
    dataframe = dataframe[dataframe["citta"] == citta]

    # Controlla se il DataFrame è vuoto
    if dataframe.empty:

        # Messaggio se non ci sono dati per quella città
        print("Nessun dato per questa città.")

        # Esce dalla funzione
        return

    # Disegna il grafico
    # Asse X = tempo
    # Asse Y = temperatura
    # marker="o" mette un pallino sui punti
    plt.plot(dataframe["tempo"], dataframe["temperatura"], marker="o")

    # Imposta il titolo del grafico
    plt.title(f"Andamento temperatura - {citta}")

    # Nome asse X
    plt.xlabel("Tempo")

    # Nome asse Y
    plt.ylabel("Temperatura (°C)")

    # Ruota le scritte sull'asse X di 45 gradi
    plt.xticks(rotation=45)

    # Mostra la griglia nel grafico
    # linestyle='--' -> linea tratteggiata
    # alpha=0.5 -> trasparenza
    plt.grid(True,linestyle='--', alpha=0.5)

    # Sistema automaticamente gli spazi del grafico
    plt.tight_layout()

    # Salva il grafico come immagine PNG
    plt.savefig("aura.png")


# MENU PRINCIPALE
# Ciclo infinito che continua finché l'utente non sceglie di uscire
while True:

    # Stampa le opzioni del menu
    print("\n1. Cerca meteo")
    print("2. Mostra grafico")
    print("3. Esci")

    # Chiede all'utente di inserire una scelta
    scelta = input("Scelta: ")

    # Se l'utente sceglie 1
    if scelta == "1":

        # Chiede il nome della città
        citta = input("Inserisci città: ")

        # Chiama la funzione ottieni_meteo
        risultato = ottieni_meteo(citta)

        # Controlla se il risultato è None
        if risultato is None:

            # Messaggio di errore
            print("Città non trovata.")

        # Se invece la città esiste
        else:

            # Divide il risultato in temperatura e descrizione
            temperatura, descrizione = risultato

            # Stampa il nome della città
            print(f"\nCittà: {citta}")

            # Stampa la temperatura
            print(f"Temperatura: {temperatura}°C")

            # Stampa la descrizione meteo
            print(f"Meteo: {descrizione}")

            # Salva i dati nel file CSV
            salva_dati(citta, temperatura)

    # Se l'utente sceglie 2
    elif scelta == "2":

        # Chiede per quale città mostrare il grafico
        citta = input("Inserisci città per grafico: ")

        # Chiama la funzione che crea il grafico
        mostra_grafico(citta)

    # Se l'utente sceglie 3
    elif scelta == "3":

        # Interrompe il ciclo e chiude il programma
        break

    # Se l'utente inserisce altro
    else:

        # Messaggio di errore
        print("Scelta non valida.")