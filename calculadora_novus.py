import streamlit as st
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Calculadora de Economia Tributária | Novus", 
    page_icon="📊", 
    layout="centered"
)

# 2. ESTILIZAÇÃO CUSTOMIZADA (CSS)
# DICA: Substitua o #004A8D e #FF7A00 pelas cores que você encontrar no manual!
st.markdown("""
    <style>
    .stApp {
        background-color: #404040;
    }
    .main-title {
        color: #004A8D;
        font-family: 'Helvetica', sans-serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .result-card {
        background-color: #F8F9FA;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #E9ECEF;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .economy-value {
        color: #28A745;
        font-size: 42px;
        font-weight: bold;
        margin: 10px 0;
    }
    .cta-button {
        background-color: #FF7A00;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGOTIPO
# Certifique-se de que a imagem está na mesma pasta
logo_path = "logo_novus.png" 
if os.path.exists(logo_path):
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.image(logo_path, use_container_width=True)
else:
    st.markdown("<h1 class='main-title'>NOVUS CONTABILIDADE</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-size: 24px;'>Descubra quanto você pode economizar em impostos</h2>", unsafe_allow_html=True)
st.write("---")

# 4. FORMULÁRIO DE ENTRADA
with st.container():
    faturamento = st.number_input("Qual o seu faturamento mensal médio?", min_value=0.0, step=1.0, format="%.2f")
    
    col1, col2 = st.columns(2)
    with col1:
        funcionarios = st.number_input("Número de funcionários", min_value=0, step=1)
    with col2:
        regime = st.selectbox("Regime Tributário Atual", ["Simples Nacional", "Lucro Presumido", "Lucro Real", "Não sei"])

st.write("")
# --- LOGICA DO BOTÃO (SUBSTITUA A PARTIR DAQUI) ---

if st.button("CALCULAR ECONOMIA REAL", use_container_width=True):
    # 1. Definição do fator (Tudo alinhado dentro do IF)
    if regime == "Simples Nacional":
        fator_economia = 0.08
    elif regime == "Lucro Presumido":
        fator_economia = 0.05
    elif regime == "Lucro Real":
        fator_economia = 0.023
    else:
        fator_economia = 0.05
    
    # 2. Cálculo (Também dentro do IF)
    total_economia = faturamento * fator_economia
    
    # 3. Exibição ÚNICA do Card (Também dentro do IF)
    st.markdown(f"""
        <div class="result-card">
            <p style="font-size: 14px; color: #6C757D; margin-bottom: 5px;">
                Cálculo baseado em alíquota média de <b>{fator_economia*100}%</b> para o regime <b>{regime}</b>.
            </p>
            <p style="font-size: 18px; color: #495057;">Empresas com o seu perfil economizam em média:</p>
            <div class="economy-value">R$ {total_economia:,.2f} / mês</div>
            <p style="color: #6C757D;">Isso representa <b>R$ {total_economia*12:,.2f}</b> de economia por ano.</p>
            <hr>
            <h4 style="color: #004A8D;">Psicologia do Ricardo: Números concretos.</h4>
            <p style="color: #495057;">Não fazemos promessas, entregamos eficiência de caixa real.</p>
            <a href="https://wa.me/5532999201923?text=Olá! Usei a calculadora e vi que posso economizar R$ {total_economia:,.2f} no regime {regime}. Quero uma análise!" class="cta-button">AGENDAR ANÁLISE COM ESPECIALISTA</a>
        </div>
    """, unsafe_allow_html=True)
    # 5. EXIBIÇÃO DO RESULTADO (Sem balões, foco no número)
    st.markdown(f"""
        <div class="result-card">
            <p style="font-size: 18px; color: #495057;">Empresas com o seu perfil economizam em média:</p>
            <div class="economy-value">R$ {total_economia:,.2f} / mês</div>
            <p style="color: #6C757D;">Isso representa <b>R$ {total_economia*12:,.2f}</b> de economia por ano.</p>
            <hr>
            <h4>Psicologia do Ricardo: Números concretos.</h4>
            <p>Não fazemos promessas, entregamos eficiência de caixa.</p>
            <a href="https://wa.me/5532999201923?text=Olá! Usei a calculadora e vi que posso economizar R$ {total_economia:,.2f}. Quero uma análise!" class="cta-button">AGENDAR ANÁLISE COM ESPECIALISTA</a>
        </div>
    """, unsafe_allow_html=True)

    # 6. DISPARO PARA O n8n (Opcional - Próximo passo)

    # Aqui poderíamos enviar os dados para o seu comercial via Webhook





