import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestor de Plantões", layout="wide")

st.title("🏥 Sincronizador de Plantões")

# URL da sua planilha (Certifique-se de que termina em /edit#gid=0 ou algo similar)
url = "https://docs.google.com/spreadsheets/d/1psqTs_ZdhGjruXIg9UPJ90_AnldAhrAzJ2UKrOpoDjo/edit?usp=sharing"

# Criando a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Lendo os dados
try:
    df = conn.read(spreadsheet=url, ttl="0") # ttl="0" força o app a buscar dados novos sempre
except:
    df = pd.DataFrame(columns=["Data", "Local", "Horas", "Valor", "Status"])

with st.sidebar:
    st.header("Novo Registro")
    data = st.date_input("Data", datetime.now())
    local = st.selectbox("Local", ["Hospital 1", "Hospital 2", "Clínica 3", "UPA 4", "Local 5"])
    horas = st.number_input("Horas", value=12)
    valor = st.number_input("Valor (R$)", value=1000.0)
    status = st.selectbox("Status", ["Agendado", "Realizado", "Pago"])
    
    if st.button("Salvar na Nuvem"):
        nova_linha = pd.DataFrame([{
            "Data": data.strftime('%d/%m/%Y'),
            "Local": local,
            "Horas": horas,
            "Valor": valor,
            "Status": status
        }])
        
        # O SEGREDO ESTÁ AQUI: 
        # Para evitar o erro de operação não suportada, vamos atualizar o DataFrame
        df_final = pd.concat([df, nova_linha], ignore_index=True)
        
        # Tentativa de salvar
        conn.update(spreadsheet=url, data=df_final)
        st.success("Sincronizado com sucesso!")
        st.cache_data.clear() # Limpa o cache para mostrar o novo dado na tela
        st.rerun()

# Exibição
if not df.empty:
    total = df[df['Status'] != 'Pago']['Valor'].sum()
    st.metric("Total a Receber", f"R$ {total:,.2f}")
    st.table(df) # Use table se o dataframe der erro de exibição
else:
    st.info("Nenhum dado encontrado ou planilha vazia.")
