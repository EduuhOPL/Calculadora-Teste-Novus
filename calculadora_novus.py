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
if st.button("CALCULAR ECONOMIA REAL", use_container_width=True):
    # LÓGICA TRIBUTÁRIA (Exemplo de simulação de economia)
    # Lógica de porcentagem dinâmica por regime
    if regime == "Simples Nacional":
       fator_economia = 0.08 # 8%
elif regime == "Lucro Presumido":
       fator_economia = 0.05 # 5%
elif regime == "Lucro Real":
    fator_economia = 0.023 # 2.3%
else:
    fator_economia = 0.05 # Valor padão para "Não Sei"
    total_economia = faturamento * fator_economia
    
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

st.caption("⚠️ Nota: Este cálculo é uma estimativa baseada em médias de mercado e não substitui uma análise técnica detalhada dos documentos contábeis da sua empresa.")
    # 6. DISPARO PARA O n8n (Opcional - Próximo passo)

    # Aqui poderíamos enviar os dados para o seu comercial via Webhook


