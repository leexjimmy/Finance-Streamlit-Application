# Importando as bibliotecas
import pandas as pd
import streamlit as st
import yfinance as yf
from datetime import date
from plotly import graph_objects as go
import plotly.express as px

st.set_page_config(page_title='Finance', page_icon = "", layout = 'wide', initial_sidebar_state = 'expanded')

def dados_acao():
    caminho = 'https://raw.githubusercontent.com/leexjimmy/Finance-Streamlit-Application/main/acoes.csv'
    return pd.read_csv(caminho, delimiter=';')

df = dados_acao()
acao = df['snome']

DATA_INICIAL = '2018-01-01'
DATA_FINAL = date.today().strftime('%Y-%m-%d')
 
st.markdown("# Finance")

# Sidebar
st.sidebar.markdown("<h1 style='text-align: center; color: black;'>Finance</h1>", unsafe_allow_html=True)
acao_e = st.selectbox('Escolha uma Ação', acao)
st.sidebar.image('image.png')
st.sidebar.markdown("<p style='text-align: center; color: black;'>Seja bem-vindo à aplicação Finance!</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: black;'>Para facilitar seus acessos, aqui vão algumas informações:</p>", unsafe_allow_html=True)
st.sidebar.write("* A tabela mostra a movimentação da ação selecionada nos últimos 10 dias e contém informações do preço de início, menor preço, maior preço, preço de fechamento e preço ajustado, que é feito pela própria bolsa de valores. Também existe uma coluna de Balance que mostra a diferença entre o valor inicial e o valor de fechamento para cada processo.")
st.sidebar.write("* O gráfico de linha traz informações do comportamento da ação no mercado desde o período de 2018 até os dias atuais, atualizando diáriamente de acordo com as movimentações da bolsa.")
st.sidebar.write("* O último gráfico de barras mostra informações sobre o o balanço entre o valor de abertura e fechamento para os últimos 30 dias de operação da bolsa de valores.")
st.sidebar.markdown("<p style='text-align: center; color: black;'>Obrigado pela atenção! E aproveite a aplicação.</p>", unsafe_allow_html=True)

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

# Chart One
st.subheader("Gráfico -" + acao_e)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores['Date'],y=df_valores['Adj Close'],
name="Preço de Fechamento", line_color='blue'))
st.plotly_chart(fig, use_container_width=True)

# Chart two
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
