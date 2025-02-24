import requests
from bs4 import BeautifulSoup
from datetime import datetime
import streamlit as st

def get_dou_data(data_str):
    url = f"https://www.in.gov.br/leiturajornal?secao=dou1&data={data_str}"
    response = requests.get(url)
    if response.status_code != 200:
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

# Streamlit App
st.title("Consulta ao Diário Oficial da União - Seção 1")

data_hoje = datetime.today().strftime('%d-%m-%Y')
st.write(f"Buscando DOU de {data_hoje}...")

materias = get_dou_data(data_hoje)

if materias:
    for i, mat in enumerate(materias[:5]):  # Mostra as 5 primeiras matérias
        st.subheader(f"{i+1}. {mat['titulo']}")
        st.write(mat['conteudo'][:500] + "...")  # Mostra os primeiros 500 caracteres
        st.write("---")
else:
    st.error("Erro ao carregar dados do DOU. Tente novamente mais tarde.")