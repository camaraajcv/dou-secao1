import requests
from bs4 import BeautifulSoup
from datetime import datetime
import streamlit as st

def get_dou_data(data_str):
    url = f"https://www.in.gov.br/leiturajornal?secao=dou1&data={data_str}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, response.status_code, ""
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Exibir um trecho do HTML para depuração
    html_sample = soup.prettify()[:2000]  # Pegamos os primeiros 2000 caracteres do HTML
    
    # Encontrar todas as matérias publicadas
    materias = soup.find_all('div', class_='texto-dou')
    
    resultado = []
    for materia in materias:
        titulo = materia.find_previous('h2').get_text(strip=True) if materia.find_previous('h2') else "Sem título"
        conteudo = materia.get_text(strip=True)
        resultado.append({"titulo": titulo, "conteudo": conteudo})
    
    return resultado, response.status_code, html_sample

# Streamlit App
st.title("Consulta ao Diário Oficial da União - Seção 1")

data_hoje = datetime.today().strftime('%d-%m-%Y')
st.write(f"Buscando DOU de {data_hoje}...")

materias, status_code, html_sample = get_dou_data(data_hoje)

if materias:
    for i, mat in enumerate(materias[:5]):  # Mostra as 5 primeiras matérias
        st.subheader(f"{i+1}. {mat['titulo']}")
        st.write(mat['conteudo'][:500] + "...")  # Mostra os primeiros 500 caracteres
        st.write("---")
elif status_code:
    st.error(f"Erro ao carregar dados do DOU. Código HTTP: {status_code}")
    st.text_area("Trecho do HTML recebido:", html_sample, height=300)
else:
    st.error("Erro ao carregar dados do DOU. Nenhuma matéria encontrada.")