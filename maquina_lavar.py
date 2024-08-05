import streamlit as st
import numpy as np
import plotly.graph_objects as go

def pertinencia_PS(x):
    if x <= 50:
        return 1 - (x / 50)
    else:
        return 0
    
def pertinencia_MS(x):
    if 0 <= x <= 50:
        return x / 50
    elif 50 < x <= 100:
        return (100 - x) / 50
    else:
        return 0
    
def pertinencia_GS(x):
    if x >= 50:
        return (x - 50) / 50
    else:
        return 0
    
def pertinencia_SM(x):
    if x <= 50:
        return 1 - (x / 50)
    elif 50 < x:
        return 0
    
def pertinencia_MM(x):
    if 0 <= x <= 50:
        return x / 50
    elif 50 < x <= 100:
        return (100 - x) / 50
    else:
        return 0
        
def pertinencia_GM(x):
    if x >= 50:
        return (x - 50) / 50
    else:
        return 0

def pertinencia_MC(y):
    if y <= 10:
        return 1 - (y / 10)
    else:
        return 0
    
def pertinencia_C(y):
    if 0 <= y <= 10:
        return y / 10
    elif 10 < y <= 25:
        return (25 - y) / 15
    else:
        return 0
    
def pertinencia_M(y):
    if 10 <= y <= 25:
        return (y - 10) / 15
    elif 25 < y <= 40:
        return (40 - y) / 15
    else:
        return 0
    
def pertinencia_L(y):
    if 25 <= y <= 40:
        return (y - 25) / 15
    elif 40 < y <= 60:
        return (60 - y) / 20
    else:
        return 0
    
def pertinencia_ML(y):
    if y >= 40:
        return (y - 40) / 20
    if y >= 60:
        return (60 - y) / 10
    else:
        return 0

st.set_page_config(page_title="Sistema de Inferência Nebulosa para Máquina de Lavar", page_icon="🧼", layout="wide")

st.title("Sistema de Inferência Nebulosa para Máquina de Lavar")

col1, col2 = st.columns(2)

with col1:
    X1 = st.slider("Grau de Sujeira (X1)", 0, 100, 25)
    X2 = st.slider("Quantidade de Manchas (X2)", 0, 100, 75)

    mu_PS = pertinencia_PS(X1)
    mu_MS = pertinencia_MS(X1)
    mu_GS = pertinencia_GS(X1)

    mu_SM = pertinencia_SM(X2)
    mu_MM = pertinencia_MM(X2)
    mu_GM = pertinencia_GM(X2)

    # Inferência
    mu_C = mu_MS * mu_SM
    mu_MC = mu_PS * mu_SM
    mu_M = (mu_PS * mu_MM) + (mu_MS * mu_MM) + (mu_GS * mu_SM)
    mu_L = (mu_PS * mu_GM) + (mu_MS * mu_GM) + (mu_GS * mu_MM)
    mu_ML = mu_GS * mu_GM

    # Verificação para evitar divisão por zero
    soma_graus = mu_MC + mu_C + mu_M + mu_L + mu_ML

    MC = 10
    C = 20
    M = 30
    L = 45
    ML = 60

    # Defuzzificação - Média Ponderada
    if soma_graus == 0:
        Y_MP = 0  # Definir um valor padrão ou outro tratamento apropriado
    else:
        Y_MP = (mu_MC * MC + mu_C * C + mu_M * M + mu_L * L + mu_ML * ML) / soma_graus

    # Defuzzificação - Centro de Gravidade
    numerador = (MC * mu_MC) + (C * mu_C) + (M * mu_M) + (L * mu_L) + (ML * mu_ML)
    denominador = mu_MC + mu_C + mu_M + mu_L + mu_ML

    if denominador == 0:
        Y_CG = 0  # Definir um valor padrão ou outro tratamento apropriado
    else:
        Y_CG = numerador / denominador

    st.write(f"Para X1 = {X1}:")
    st.write(f"- PS (Pouco Sujo): {mu_PS:.2f}")
    st.write(f"- MS (Médio Sujo): {mu_MS:.2f}")
    st.write(f"- GS (Muito Sujo): {mu_GS:.2f}")

    st.write(f"Para X2 = {X2}:")
    st.write(f"- SM (Sem Manchas): {mu_SM:.2f}")
    st.write(f"- MM (Média Manchas): {mu_MM:.2f}")
    st.write(f"- GM (Muitas Manchas): {mu_GM:.2f}")

    st.write(f"Tempo de lavagem (média ponderada): {Y_MP:.2f} minutos")
    st.write(f"Tempo de lavagem (centro de gravidade): {Y_CG:.2f} minutos")

with col2:
    x_values = np.linspace(0, 100, 400)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=[pertinencia_PS(x) for x in x_values], mode='lines', name='PS'))
    fig.add_trace(go.Scatter(x=x_values, y=[pertinencia_MS(x) for x in x_values], mode='lines', name='MS'))
    fig.add_trace(go.Scatter(x=x_values, y=[pertinencia_GS(x) for x in x_values], mode='lines', name='GS'))
    fig.add_trace(go.Scatter(x=[X1], y=[0], mode='markers', marker=dict(size=10, color='red'), name=f'Seleção X1={X1}'))
    fig.add_vline(x=X1, line=dict(dash='dot', color='red'))
    fig.update_layout(title='Conjuntos Fuzzy - Sujeira (X1)', xaxis_title='Grau de Sujeira', yaxis_title='Pertinência')
    st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=[pertinencia_SM(x) for x in x_values], mode='lines', name='SM'))
    fig.add_trace(go.Scatter(x=x_values, y=[pertinencia_MM(x) for x in x_values], mode='lines', name='MM'))
    fig.add_trace(go.Scatter(x=x_values, y=[pertinencia_GM(x) for x in x_values], mode='lines', name='GM'))
    fig.add_trace(go.Scatter(x=[X2], y=[0], mode='markers', marker=dict(size=10, color='red'), name=f'Seleção X2={X2}'))
    fig.add_vline(x=X2, line=dict(dash='dot', color='red'))
    fig.update_layout(title='Conjuntos Fuzzy - Manchas (X2)', xaxis_title='Quantidade de Manchas', yaxis_title='Pertinência')
    st.plotly_chart(fig)

    y_values = np.linspace(0, 60, 400)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_values, y=[pertinencia_MC(y) for y in y_values], mode='lines', name='MC'))
    fig.add_trace(go.Scatter(x=y_values, y=[pertinencia_C(y) for y in y_values], mode='lines', name='C'))
    fig.add_trace(go.Scatter(x=y_values, y=[pertinencia_M(y) for y in y_values], mode='lines', name='M'))
    fig.add_trace(go.Scatter(x=y_values, y=[pertinencia_L(y) for y in y_values], mode='lines', name='L'))
    fig.add_trace(go.Scatter(x=y_values, y=[pertinencia_ML(y) for y in y_values], mode='lines', name='ML'))
    fig.add_trace(go.Scatter(x=[Y_MP], y=[0], mode='markers', marker=dict(size=10, color='blue'), name=f'Tempo MP={Y_MP:.2f}'))
    fig.add_trace(go.Scatter(x=[Y_CG], y=[0], mode='markers', marker=dict(size=10, color='green'), name=f'Tempo CG={Y_CG:.2f}'))
    fig.add_vline(x=Y_MP, line=dict(dash='dot', color='blue'))
    fig.add_vline(x=Y_CG, line=dict(dash='dot', color='green'))
    fig.update_layout(title='Conjuntos Fuzzy - Tempo de Lavagem (Y)', xaxis_title='Tempo de Lavagem', yaxis_title='Pertinência')
    st.plotly_chart(fig)
