

# %%

import streamlit as st 
import pandas as pd 
import sqlalchemy
import datetime
import json
from gen_ia import generate
import os
import dotenv
import codecs


dotenv.load_dotenv()


engine = sqlalchemy.create_engine("sqlite:///database.db")


with open("query_inteligente.sql") as query_file:
    query = query_file.read()

with open("promtp_template.md", encoding="utf-8") as prompt_file:
    prompt = prompt_file.read()


with open("resposta_template.json") as resposta_file:
    resposta = json.load(resposta_file)


def processa_nf(prompt, resposta_template, produtos, img_file ):
    st.image(open_img)

    prompt_exec =prompt.format(produtos="\n".join(produtos) , respostas=resposta_template)   
    resp = generate(prompt_exec, 
                    img_file.getvalue(),
                    img_file.type)
    df = pd.DataFrame(json.loads(resp.text))
    return df 


st.set_page_config(page_title="Lista de Compras")

st.markdown("# Lista de Compras! ")

try:
    
    col, _ = st.columns(2)
    num_dias_adiante = col.number_input("Dias sem ir ao mercado",
                                       min_value=0,
                                       max_value=60,
                                       step=1)
    
    df_stats = pd.read_sql(query, engine)
    df_stats["comprar"] = df_stats["dias_ultima_compra"] + num_dias_adiante > df_stats["Dif_Dias"]
    
    df_compra = df_stats[df_stats["comprar"]]
    
    
except Exception as err:
    print(err)
    df_compra = pd.DataFrame()



if df_stats.empty:
    st.warning("Não há dados históricos suficientes!")
else:
    st.dataframe(df_compra)



st.markdown("## Adcionar Compra!")


produtos = sorted(df_compra["produto"].unique().tolist())

produto = st.selectbox("Produto", options=["Novo Produto"]+ (produtos or [])    ) 

if produto == "Novo Produto":
    st.text_input("Inserir novo Produto")
    
valor_produto = st.number_input("Valor", min_value=0.00)

if st.button("Registrar compra"):
    data = {
        "dt_compra": datetime.datetime.now().strftime("%Y-%m-%d"),
        "produto": produto.title(),
        "valor_produto" :valor_produto,
    }

    df_insert = pd.DataFrame([data])
    df_insert.to_sql("Compras",engine,if_exists="append", index=False)
    st.success("Novo produto registrado!")

st.markdown("## Importar histórico")

open_file = st.file_uploader("Entre com o arquivo .csv", type="csv")


if open_file:
    df = pd.read_csv(open_file, encoding="cp1252")
    df = st.data_editor(df)
    
    if st.button("Registrar dados!"):
        
        df.to_sql("compras", engine , if_exists="append" , index=False)
        
        st.success("Dados Registrados com sucesso!")
        

st.markdown("## Importar Nota Fistal")

open_img = st.file_uploader("Entre com o arquivo de imagem", type=["png","jpeg"])

if open_img:
    df = processa_nf(prompt=prompt, resposta_template=resposta, produtos=produtos, img_file=open_img)
    st.data_editor(df)
    
