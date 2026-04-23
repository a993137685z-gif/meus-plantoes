import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestor de Plantões", layout="wide")

st.title("🏥 Sincronizador de Plantões")

# Conectando à planilha
url = "https://docs.google.com/spreadsheets/d/1psqTs_ZdhGjruXIg9UPJ90_AnldAhrAzJ2UKrOpoDjo/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Carrega os dados da planilha
df = conn.read(spreadsheet=url)

# Se a planilha estiver vazia, cria a estrutura
if df.empty:
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
        
        # Junta o novo dado com os antigos e salva de volta no Google
        df_final = pd.concat([df, nova_linha], ignore_index=True)
        conn.update(spreadsheet=url, data=df_final)
        st.success("Sincronizado!")
        st.rerun()

# Mostra as métricas e a tabela
if not df.empty:
    st.metric("Total a Receber", f"R$ {df[df['Status'] != 'Pago']['Valor'].sum():,.2f}")
    st.dataframe(df, use_container_width=True)
