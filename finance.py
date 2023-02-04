# Importando as bibliotecas
import pandas as pd
import streamlit as st
import yfinance as yf
from datetime import date
from plotly import graph_objects as go
import plotly.express as px

st.set_page_config(page_title='Finance', page_icon = "", layout = 'wide', initial_sidebar_state = 'auto')
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)

# Função para pegar nome da ação e sigla
def dados_acao():
    caminho = 'C:/Users/Alex/Desktop/Projetos/Python/streamlit/App Ações/acoes.csv'
    return pd.read_csv(caminho, delimiter=';')


# Definindo variáveis
df = dados_acao()

acao = df['snome']

DATA_INICIAL = '2018-01-01'
DATA_FINAL = date.today().strftime('%Y-%m-%d')

 
st.markdown("# Finance")

# Sidebar

st.sidebar.title('Finance')
acao_e = st.sidebar.selectbox('Escolha uma Ação', acao)
st.sidebar.image('image.png')
df_acao = df[df['snome'] == acao_e]
acao_escolhida = df_acao.iloc[0]['sigla_acao']
acao_escolhida = acao_escolhida + '.SA'

@st.cache(allow_output_mutation=True)
def acao_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIAL, DATA_FINAL)
    df.reset_index(inplace=True)
    
    return df

df_valores = acao_online(acao_escolhida)
df_valores = df_valores.drop(['Volume'], axis=1)
df_valores['Balance'] = df_valores['Adj Close'].values - df_valores['Open'].values

st.subheader('Tabela - ' + acao_e)
st.dataframe(df_valores.tail(10), use_container_width=True)

# Grádico da Ação
st.subheader("Gráfico -" + acao_e)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores['Date'],y=df_valores['Adj Close'],
name="Preço de Fechamento", line_color='blue'))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Balanço nos Últimos 30 dias - " + acao_e)
fig = px.bar(df_valores.tail(30), x='Date', y='Balance', color="Balance",color_continuous_scale=px.colors.sequential.Cividis_r)
fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
st.plotly_chart(fig, use_container_width=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)