import folium
import webbrowser
import urllib.parse
import urllib.request
import json
import ssl

uzytkownicy = [{"username": "admin", "password": "admin"}]

orkiestry = [
    {"id": 1, "name": "Orkiestra Warszawska", "latitude": 52.2296756, "longitude": 21.0122287}
]

klienci = [
    {"id": 1, "name": "Jan Kowalski", "latitude": 52.406374, "longitude": 16.9251681, "orchestra_id": 1}
]

pracownicy = [
    {"id": 1, "name": "Anna Nowak", "instrument": "Skrzypce", "latitude": 50.0646501, "longitude": 19.9449799, "orchestra_id": 1}
]

# Wyłączanie weryfikacji certyfikatu SSL
ssl._create_default_https_context = ssl._create_unverified_context

def get_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?{urllib.parse.urlencode({'q': city_name, 'format': 'json'})}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                print("Nie można znaleźć lokalizacji.")
                return None, None
    except Exception as e:
        print(f"Błąd podczas uzyskiwania współrzędnych: {e}")
        return None, None

# Funkcje logowania
def logowanie():
    while True:
        username = input("Podaj nazwę użytkownika: ")
        password = input("Podaj hasło: ")
        for user in uzytkownicy:
            if user["username"] == username and user["password"] == password:
                print("Logowanie zakończone sukcesem.")
                return True
        print("Błędna nazwa użytkownika lub hasło. Spróbuj ponownie.")

# Funkcje do zarządzania orkiestrami
def dodaj_orkiestre(name, city_name):
    latitude, longitude = get_coordinates(city_name)
    if latitude and longitude:
        new_id = max([o["id"] for o in orkiestry], default=0) + 1
        orkiestry.append({"id": new_id, "name": name, "latitude": latitude, "longitude": longitude})
        print("Orkiestra dodana.")

def aktualizuj_orkiestre(orchestra_id, name, city_name):
    latitude, longitude = get_coordinates(city_name)
    if latitude and longitude:
        for orkiestra in orkiestry:
            if orkiestra["id"] == orchestra_id:
                orkiestra["name"] = name
                orkiestra["latitude"] = latitude
                orkiestra["longitude"] = longitude
                print("Orkiestra zaktualizowana.")
                return
    print("Orkiestra nie znaleziona.")

def usun_orkiestre(orchestra_id):
    global orkiestry
    orkiestry = [o for o in orkiestry if o["id"] != orchestra_id]
    print("Orkiestra usunięta.")

def lista_orkiestr():
    for orkiestra in orkiestry:
        print(orkiestra)

# Funkcje do zarządzania klientami
def dodaj_klienta(name, city_name, orchestra_id):
    latitude, longitude = get_coordinates(city_name)
    if latitude and longitude:
        new_id = max([c["id"] for c in klienci], default=0) + 1
        klienci.append({"id": new_id, "name": name, "latitude": latitude, "longitude": longitude, "orchestra_id": orchestra_id})
        print("Klient dodany.")

def aktualizuj_klienta(client_id, name, city_name):
    latitude, longitude = get_coordinates(city_name)
    if latitude and longitude:
        for klient in klienci:
            if klient["id"] == client_id:
                klient["name"] = name
                klient["latitude"] = latitude
                klient["longitude"] = longitude
                print("Klient zaktualizowany.")
                return
    print("Klient nie znaleziony.")

def usun_klienta(client_id):
    global klienci
    klienci = [c for c in klienci if c["id"] != client_id]
    print("Klient usunięty.")

def lista_klientow():
    for klient in klienci:
        print(klient)

# Funkcje do zarządzania pracownikami
def dodaj_pracownika(name, instrument, city_name, orchestra_id):
    latitude, longitude = get_coordinates(city_name)
    if latitude and longitude:
        new_id = max([e["id"] for e in pracownicy], default=0) + 1
        pracownicy.append({"id": new_id, "name": name, "instrument": instrument, "latitude": latitude, "longitude": longitude, "orchestra_id": orchestra_id})
        print("Pracownik dodany.")

def aktualizuj_pracownika(employee_id, name, city_name):
    latitude, longitude = get_coordinates(city_name)
    if latitude and longitude:
        for pracownik in pracownicy:
            if pracownik["id"] == employee_id:
                pracownik["name"] = name
                pracownik["latitude"] = latitude
                pracownik["longitude"] = longitude
                print("Pracownik zaktualizowany.")
                return
    print("Pracownik nie znaleziony.")

def usun_pracownika(employee_id):
    global pracownicy
    pracownicy = [e for e in pracownicy if e["id"] != employee_id]
    print("Pracownik usunięty.")

def lista_pracownikow():
    for pracownik in pracownicy:
        print(pracownik)

# Funkcje do wyświetlania list klientów i pracowników wybranej orkiestry
def lista_klientow_orkiestry(orchestra_id):
    for klient in klienci:
        if klient["orchestra_id"] == orchestra_id:
            print(klient)

def lista_pracownikow_orkiestry(orchestra_id):
    for pracownik in pracownicy:
        if pracownik["orchestra_id"] == orchestra_id:
            print(pracownik)

# Funkcje do generowania map
def generuj_mape_klientow():
    mapa = folium.Map(location=[52.2296756, 21.0122287], zoom_start=6)
    for klient in klienci:
        folium.Marker(
            location=[klient["latitude"], klient["longitude"]],
            popup=klient["name"],
            icon=folium.Icon(color="blue")
        ).add_to(mapa)
    mapa.save("mapa_klientow.html")
    print("Mapa klientów wygenerowana.")
    folium_map_display("mapa_klientow.html")

def generuj_mape_orkiestr():
    mapa = folium.Map(location=[52.2296756, 21.0122287], zoom_start=6)
    for orkiestra in orkiestry:
        folium.Marker(
            location=[orkiestra["latitude"], orkiestra["longitude"]],
            popup=orkiestra["name"],
            icon=folium.Icon(color="green")
        ).add_to(mapa)
    mapa.save("mapa_orkiestr.html")
    print("Mapa orkiestr wygenerowana.")
    folium_map_display("mapa_orkiestr.html")

def generuj_mape_pracownikow():
    mapa = folium.Map(location=[52.2296756, 21.0122287], zoom_start=6)
    for pracownik in pracownicy:
        folium.Marker(
            location=[pracownik["latitude"], pracownik["longitude"]],
            popup=f"{pracownik['name']} ({pracownik['instrument']})",
            icon=folium.Icon(color="red")
        ).add_to(mapa)
    mapa.save("mapa_pracownikow.html")
    print("Mapa pracowników wygenerowana.")
    folium_map_display("mapa_pracownikow.html")

def generuj_mape_wszystkiego():
    mapa = folium.Map(location=[52.2296756, 21.0122287], zoom_start=6)

    for klient in klienci:
        folium.Marker(
            location=[klient["latitude"], klient["longitude"]],
            popup=klient["name"],
            icon=folium.Icon(color="blue")
        ).add_to(mapa)

    for orkiestra in orkiestry:
        folium.Marker(
            location=[orkiestra["latitude"], orkiestra["longitude"]],
            popup=orkiestra["name"],
            icon=folium.Icon(color="green")
        ).add_to(mapa)

    for pracownik in pracownicy:
        folium.Marker(
            location=[pracownik["latitude"], pracownik["longitude"]],
            popup=f"{pracownik['name']} ({pracownik['instrument']})",
            icon=folium.Icon(color="red")
        ).add_to(mapa)

    mapa.save("mapa_wszystkiego.html")
    print("Mapa wszystkiego wygenerowana.")
    folium_map_display("mapa_wszystkiego.html")

def folium_map_display(map_path):
    webbrowser.open(map_path)

# Funkcja wyświetlająca menu
def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Dodaj orkiestrę")
        print("2. Aktualizuj orkiestrę")
        print("3. Usuń orkiestrę")
        print("4. Wyświetl listę orkiestr")
        print("5. Dodaj klienta")
        print("6. Aktualizuj klienta")
        print("7. Usuń klienta")
        print("8. Wyświetl listę klientów")
        print("9. Dodaj pracownika")
        print("10. Aktualizuj pracownika")
        print("11. Usuń pracownika")
        print("12. Wyświetl listę pracowników")
        print("13. Wyświetl listę klientów wybranej orkiestry")
        print("14. Wyświetl listę pracowników wybranej orkiestry")
        print("15. Generuj mapę klientów")
        print("16. Generuj mapę orkiestr")
        print("17. Generuj mapę pracowników")
        print("18. Generuj mapę wszystkiego")
        print("0. Koniec programu")
        wybor = input("Wybierz opcję: ")

        if wybor == "0":
            print("Zakończono program.")
            break
        elif wybor == "1":
            name = input("Podaj nazwę orkiestry: ")
            city_name = input("Podaj nazwę miejscowości: ")
            dodaj_orkiestre(name, city_name)
        elif wybor == "2":
            orchestra_id = int(input("Podaj ID orkiestry: "))
            name = input("Podaj nową nazwę orkiestry: ")
            city_name = input("Podaj nazwę miejscowości: ")
            aktualizuj_orkiestre(orchestra_id, name, city_name)
        elif wybor == "3":
            orchestra_id = int(input("Podaj ID orkiestry do usunięcia: "))
            usun_orkiestre(orchestra_id)
        elif wybor == "4":
            lista_orkiestr()
        elif wybor == "5":
            name = input("Podaj nazwę klienta: ")
            city_name = input("Podaj nazwę miejscowości: ")
            orchestra_id = int(input("Podaj ID orkiestry: "))
            dodaj_klienta(name, city_name, orchestra_id)
        elif wybor == "6":
            client_id = int(input("Podaj ID klienta: "))
            name = input("Podaj nową nazwę klienta: ")
            city_name = input("Podaj nazwę miejscowości: ")
            aktualizuj_klienta(client_id, name, city_name)
        elif wybor == "7":
            client_id = int(input("Podaj ID klienta do usunięcia: "))
            usun_klienta(client_id)
        elif wybor == "8":
            lista_klientow()
        elif wybor == "9":
            name = input("Podaj nazwę pracownika: ")
            instrument = input("Podaj instrument: ")
            city_name = input("Podaj nazwę miejscowości: ")
            orchestra_id = int(input("Podaj ID orkiestry: "))
            dodaj_pracownika(name, instrument, city_name, orchestra_id)
        elif wybor == "10":
            employee_id = int(input("Podaj ID pracownika: "))
            name = input("Podaj nową nazwę pracownika: ")
            city_name = input("Podaj nazwę miejscowości: ")
            aktualizuj_pracownika(employee_id, name, city_name)
        elif wybor == "11":
            employee_id = int(input("Podaj ID pracownika do usunięcia: "))
            usun_pracownika(employee_id)
        elif wybor == "12":
            lista_pracownikow()
        elif wybor == "13":
            orchestra_id = int(input("Podaj ID orkiestry: "))
            lista_klientow_orkiestry(orchestra_id)
        elif wybor == "14":
            orchestra_id = int(input("Podaj ID orkiestry: "))
            lista_pracownikow_orkiestry(orchestra_id)
        elif wybor == "15":
            generuj_mape_klientow()
        elif wybor == "16":
            generuj_mape_orkiestr()
        elif wybor == "17":
            generuj_mape_pracownikow()
        elif wybor == "18":
            generuj_mape_wszystkiego()
        else:
            print("Nieprawidłowa opcja, spróbuj ponownie.")

# Przykładowe użycie
if __name__ == "__main__":
    # Logowanie do systemu
    if logowanie():
        # Uruchomienie menu
        menu()
