import requests
import json

url = 'http://localhost:5000/graphql'
headers = {'Content-Type': 'application/json'}
query = {
    'query': '{ predictBenefit(bancarizado:"SI", discapacidad:"NO", etnia:"NINGUNO", nivelEscolaridad:"NINGUNO", genero:"Mujer", tipoPoblacion:"SISBEN", cantidadDeBeneficiarios:2, rangoEdad:57.5) }'
}

response = requests.post(url, headers=headers, data=json.dumps(query))
print(response.json())