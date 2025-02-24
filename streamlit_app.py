import requests
from bs4 import BeautifulSoup4
from datetime import datetime

def get_dou_data(data_str):
    url = f"https://www.in.gov.br/leiturajornal?secao=dou1&data={data_str}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erro ao acessar o DOU")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar todas as matérias publicadas
    materias = soup.find_all('div', class_='texto-dou')
    
    resultado = []
    for materia in materias:
        titulo = materia.find_previous('h2').get_text(strip=True) if materia.find_previous('h2') else "Sem título"
        conteudo = materia.get_text(strip=True)
        resultado.append({"titulo": titulo, "conteudo": conteudo})
    
    return resultado

# Teste com a data de hoje
data_hoje = datetime.today().strftime('%d-%m-%Y')
materias = get_dou_data(data_hoje)

if materias:
    for i, mat in enumerate(materias[:5]):  # Mostra as 5 primeiras matérias
        print(f"{i+1}. {mat['titulo']}")
        print(mat['conteudo'][:500], "...")  # Mostra os primeiros 500 caracteres
        print("-" * 50)