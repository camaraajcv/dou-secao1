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
    
    # Encontrar a estrutura correta dentro de <div id="hierarchy_content">
    hierarchy_content = soup.find("div", id="hierarchy_content")
    if not hierarchy_content:
        return None, response.status_code, html_sample
    
    sumarios = hierarchy_content.find_all('li', class_='folder level1')
    
    resultado = []
    for item in sumarios:
        titulo = item.find('span', class_='titulo').get_text(strip=True) if item.find('span', class_='titulo') else "Sem título"
        link = item.find('a')['href'] if item.find('a') else "#"
        resultado.append({"titulo": titulo, "link": link})
    
    return resultado, response.status_code, html_sample

# Streamlit App
st.title("Consulta ao Diário Oficial da União - Seção 1")

data_hoje = datetime.today().strftime('%d-%m-%Y')
st.write(f"Buscando DOU de {data_hoje}...")

materias, status_code, html_sample = get_dou_data(data_hoje)

if materias:
    for i, mat in enumerate(materias[:10]):  # Mostra os 10 primeiros itens
        st.subheader(f"{i+1}. {mat['titulo']}")
        st.markdown(f"[Leia mais]({mat['link']})")  # Adiciona link para a matéria completa
        st.write("---")
elif status_code:
    st.error(f"Erro ao carregar dados do DOU. Código HTTP: {status_code}")
    st.text_area("Trecho do HTML recebido:", html_sample, height=300)
else:
    st.error("Erro ao carregar dados do DOU. Nenhuma matéria encontrada.")
