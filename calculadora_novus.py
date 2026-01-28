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

# --- 4. FORMULÁRIO DE ANÁLISE TRIBUTÁRIA ---
with st.container():
    st.markdown("### 📝 Dados de Contato")
    col_nome, col_email = st.columns(2)
    with col_nome:
        nome = st.text_input("Seu Nome completo")
    with col_email:
        email = st.text_input("Seu melhor E-mail")
    
    telefone = st.text_input("WhatsApp (com DDD)")

    st.write("---")
    st.markdown("### 📊 Perfil da Empresa")
    faturamento_mensal = st.number_input("Qual o seu faturamento mensal médio? (R$)", min_value=0.0, step=1000.0, format="%.2f")
    
    # 1. Substituindo funcionários por Segmento
    segmento = st.selectbox("Qual o Segmento da sua empresa?", ["Comércio", "Serviço", "Indústria"])

st.write("")

# --- LÓGICA DO BOTÃO ---
if st.button("GERAR DIAGNÓSTICO TRIBUTÁRIO", use_container_width=True):
    if not nome or not email or not telefone or faturamento_mensal <= 0:
        st.error("⚠️ Por favor, preencha todos os campos para liberar o diagnóstico.")
    
    elif "@" not in email or "." not in email:
        st.error("📧 Por favor, insira um e-mail válido.")
    
    else:
        # 2. Lógica de Enquadramento (Baseada no Faturamento Anual)
        faturamento_anual = faturamento_mensal * 12
        
        if faturamento_anual <= 81000:
            regime_sugerido = "MEI (Microempreendedor Individual)"
            cor_regime = "#28A745" # Verde
        elif faturamento_anual <= 48000000: # Conforme seu critério de 48M
            regime_sugerido = "Simples Nacional"
            cor_regime = "#004A8D" # Azul Novus
        elif faturamento_anual <= 78000000:
            regime_sugerido = "Lucro Presumido"
            cor_regime = "#FF7A00" # Laranja
        else:
            regime_sugerido = "Lucro Real"
            cor_regime = "#DC3545" # Vermelho (Complexidade Alta)

        # 3. Disparo para o n8n (Atualizado)
        try:
            webhook_url = st.secrets["WEBHOOK_URL"]
            dados_lead = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "faturamento_mensal": faturamento_mensal,
                "faturamento_anual": faturamento_anual,
                "segmento": segmento,
                "regime_sugerido": regime_sugerido
            }
            requests.post(webhook_url, json=dados_lead, timeout=5)
        except:
            pass

        # 4. EXIBIÇÃO DO RESUMO (Informações Resumidas)
        st.markdown(f"""
            <div class="result-card">
                <h3 style="color: #004A8D;">📋 Resumo da Análise Tributária</h3>
                <div style="text-align: left; background-color: #ffffff; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p style="color: #404040; margin: 10px 0;"><b>Nome:</b> {nome}</p>
                    <p style="color: #404040; margin: 10px 0;"><b>Segmento:</b> {segmento}</p>
                    <p style="color: #404040; margin: 10px 0;"><b>Faturamento Mensal:</b> R$ {faturamento_mensal:,.2f}</p>
                    <p style="color: #404040; margin: 10px 0;"><b>Faturamento Anual Est.:</b> R$ {faturamento_anual:,.2f}</p>
                </div>
                <hr>
                <p style="font-size: 16px; color: #495057; margin-bottom: 0;">Regime Tributário Sugerido:</p>
                <div style="color: {cor_regime}; font-size: 28px; font-weight: bold; margin: 10px 0;">{regime_sugerido}</div>
                <p style="font-size: 13px; color: #6C757D;">*Análise baseada nos limites de faturamento informados.</p>
                <hr>
                <a href="https://wa.me/5532999201923?text=Olá! Gere o diagnóstico para {nome}. Faturamento de R$ {faturamento_mensal:,.2f} no segmento {segmento}. O regime sugerido foi {regime_sugerido}." class="cta-button">VALIDAR COM UM CONTADOR NOVUS</a>
            </div>
        """, unsafe_allow_html=True)

