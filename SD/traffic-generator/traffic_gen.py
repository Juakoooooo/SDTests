#import requests
#import csv
#import random
#import time
#
#def generate_traffic(api_url, dataset_path):
#    # Leer todos los dominios del dataset en una lista
#    with open(dataset_path, 'r') as file:
#        reader = csv.reader(file)
#        domains = [row[0].strip() for row in reader]
#
#    if not domains:
#        print("No domains found in the dataset.")
#        return
#
#    # Inicializar el índice para recorrer los dominios secuencialmente
#    index = 0
#    current_step = 0
#    steps = random.randint(1, 100000)  # Generar el primer número de pasos aleatorio
#    print(f"Starting with {steps} steps.")
#
#    while True:
#        # Seleccionar el dominio actual basado en el índice
#        domain = domains[index]
#        print(f"Selected domain: {domain} (Step {current_step + 1} of {steps})")
#
#        # Realizar la solicitud a la API
#        try:
#            response = requests.get(f"{api_url}/resolve", params={"domain": domain})
#            if response.status_code == 200:
#                print(f"Resolved {domain}: {response.json()}")
#            else:
#                print(f"Failed to resolve {domain}: {response.status_code}")
#        except Exception as e:
#            print(f"Error sending request for {domain}: {e}")
#
#        # Incrementar el contador de pasos y el índice del dominio
#        current_step += 1
#        index = (index + 1) % len(domains)  # Volver al principio si se llega al final de la lista
#
#        # Si se alcanzó el número de pasos, generar un nuevo número de pasos, restablecer el contador y el índice
#        if current_step >= steps:
#            current_step = 0
#            index = 0  # Restablecer el índice para comenzar desde el primer dominio
#            steps = random.randint(1, 5)  # Generar un nuevo número de pasos aleatorio
#            print(f"Generated new random step count: {steps}")
#
#        # Esperar un momento antes de la siguiente solicitud
#        time.sleep(0.01)  # Ajusta este tiempo según la intensidad de tráfico que desees
#
#if __name__ == "__main__":
#    api_url = "http://dns-api:5000"
#    dataset_path = "/app/data/dataset.csv"
#    generate_traffic(api_url, dataset_path)


import requests
import csv
import random
import time

def generate_traffic(api_url, dataset_path):
    # Leer todos los dominios del dataset en una lista
    with open(dataset_path, 'r') as file:
        reader = csv.reader(file)
        domains = [row[0].strip() for row in reader]

    if not domains:
        print("No domains found in the dataset.")
        return

    # Inicializar el índice para recorrer los dominios secuencialmente
    index = random.randint(0, len(domains) - 1)  # Comenzar desde un índice aleatorio
    current_step = 0
    steps = random.randint(1, 20)  # Cambia el rango para un número más grande de pasos
    print(f"Starting with {steps} steps.")

    while True:
        # Seleccionar el dominio actual basado en el índice
        domain = domains[index]
        print(f"Selected domain: {domain} (Step {current_step + 1} of {steps})")

        # Realizar la solicitud a la API
        try:
            response = requests.get(f"{api_url}/resolve", params={"domain": domain})
            if response.status_code == 200:
                print(f"Resolved {domain}: {response.json()}")
            else:
                print(f"Failed to resolve {domain}: {response.status_code}")
        except Exception as e:
            print(f"Error sending request for {domain}: {e}")

        # Incrementar el contador de pasos y el índice del dominio
        current_step += 1
        index = (index + 1) % len(domains)  # Volver al principio si se llega al final de la lista

        # Si se alcanzó el número de pasos, generar un nuevo número de pasos y un nuevo índice aleatorio
        if current_step >= steps:
            current_step = 0
            index = random.randint(0, len(domains) - 1)  # Generar un nuevo índice aleatorio
            steps = random.randint(1, 20)  # Generar un nuevo número aleatorio de pasos
            print(f"Generated new random step count: {steps} and starting index: {index}")

        # Esperar un momento antes de la siguiente solicitud
        time.sleep(0.01)  # Tiempo de espera muy pequeño para alta frecuencia de tráfico

if __name__ == "__main__":
    api_url = "http://dns-api:5000"
    dataset_path = "/app/data/dataset.csv"
    generate_traffic(api_url, dataset_path)
