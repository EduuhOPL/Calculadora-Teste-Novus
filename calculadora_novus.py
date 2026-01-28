import streamlit as st
import os
import requests

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

# 4. FORMULÁRIO DE ENTRADA E CAPTURA DE LEAD
with st.container():
    st.markdown("### 📝 Informe seus dados para o cálculo")
    col_nome, col_email = st.columns(2)
    with col_nome:
        nome = st.text_input("Seu Nome completo")
    with col_email:
        email = st.text_input("Seu melhor E-mail")
    
    telefone = st.text_input("WhatsApp (com DDD)")

    st.write("---")
    st.markdown("### 📊 Dados da Empresa")
    faturamento = st.number_input("Qual o seu faturamento mensal médio?", min_value=0.0, step=1.0, format="%.2f")
    
    col1, col2 = st.columns(2)
    with col1:
        funcionarios = st.number_input("Número de funcionários", min_value=0, step=1)
    with col2:
        regime = st.selectbox("Regime Tributário Atual", ["Simples Nacional", "Lucro Presumido", "Lucro Real", "Não sei"])

st.write("")

# LÓGICA DO BOTÃO
if st.button("CALCULAR ECONOMIA REAL", use_container_width=True):
    # Validação simples: Só calcula se nome e email estiverem preenchidos
    if not nome or not email or not telefone:
        st.error("⚠️ Por favor, preencha seu nome, e-mail e telefone para liberar o resultado.")
    else:
        # Lógica de porcentagem dinâmica
        if regime == "Simples Nacional":
            fator_economia = 0.08
        elif regime == "Lucro Presumido":
            fator_economia = 0.05
        elif regime == "Lucro Real":
            fator_economia = 0.023
        else:
            fator_economia = 0.05
        
        total_economia = faturamento * fator_economia
        
        # 5. EXIBIÇÃO DO RESULTADO
        st.markdown(f"""
            <div class="result-card">
                <p style="font-size: 14px; color: #6C757D; margin-bottom: 5px;">
                    Olá <b>{nome}</b>! Veja o potencial de economia para sua empresa:
                </p>
                <div class="economy-value">R$ {total_economia:,.2f} / mês</div>
                <p style="color: #6C757D;">Isso representa <b>R$ {total_economia*12:,.2f}</b> de economia por ano.</p>
                <hr>
                <h4 style="color: #004A8D; font-size: 15px;">⚠️ Nota: Este cálculo é uma estimativa baseada em médias de mercado e não substitui uma análise técnica detalhada dos documentos contábeis da sua empresa..</h4>
                <a href="https://wa.me/5532999201923?text=Olá! Meu nome é {nome} e usei a calculadora. Vi que posso economizar R$ {total_economia:,.2f} no regime {regime}." class="cta-button">FALAR COM ESPECIALISTA AGORA</a>
            </div>
        """, unsafe_allow_html=True)
    
        if "@" not in email or "." not in email:
           st.error("📧 Por favor, insira um e-mail válido.")
    elif len(telefone) < 10:
        st.error("📱 Por favor, insira um WhatsApp com DDD.")
    else:
         # Se chegou aqui, os dados estão OK, então fazemos o cálculo e o envio
         total_economia = faturamento * fator_economia
        
        # Envio para o n8n usando o Secret
        try:
            webhook_url = st.secrets["WEBHOOK_URL"]
            requests.post(webhook_url, json=dados_lead, timeout=5)
        except Exception as e:
            print(f"Erro no webhook: {e}")

        # Exibição do resultado
        st.markdown(f""" <div class="result-card"> ... </div> """, unsafe_allow_html=True) 

