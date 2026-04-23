import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestor de Plantões", layout="wide")

# Lista dos seus locais de trabalho (Você pode mudar os nomes aqui)
LOCAIS = ["Hospital 1", "Hospital 2", "Clínica 3", "UPA 4", "Local 5"]

if 'plantoes' not in st.session_state:
    st.session_state.plantoes = pd.DataFrame(columns=["Data", "Local", "Horas", "Valor", "Status"])

st.title("🏥 Gestão de Plantões")

with st.sidebar:
    st.header("Novo Registro")
    data = st.date_input("Data", datetime.now())
    local = st.selectbox("Onde foi o plantão?", LOCAIS)
    horas = st.number_input("Carga Horária", value=12)
    valor = st.number_input("Valor a receber (R$)", value=1000.0)
    status = st.selectbox("Status", ["Agendado", "Realizado", "Pago"])
    
    if st.button("Adicionar"):
        novo = pd.DataFrame([[data, local, horas, valor, status]], columns=st.session_state.plantoes.columns)
        st.session_state.plantoes = pd.concat([st.session_state.plantoes, novo], ignore_index=True)
        st.success("Adicionado!")

df = st.session_state.plantoes
if not df.empty:
    c1, c2 = st.columns(2)
    c1.metric("Total a Receber", f"R$ {df[df['Status'] != 'Pago']['Valor'].sum():,.2f}")
    c2.metric("Total de Plantões", len(df))
    
    st.dataframe(df, use_container_width=True)
    
    # IMPORTANTE: Botão para você não perder seus dados
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Excel (Salvar Dados)", csv, "meus_plantoes.csv", "text/csv")
else:
    st.info("Adicione seu primeiro plantão na barra lateral!")
