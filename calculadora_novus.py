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

# 4. FORMULÁRIO DE ANÁLISE TRIBUTÁRIA
with st.container():
    st.markdown("### 📝 Dados de Contato")
    col_nome, col_email = st.columns(2)
    with col_nome:
        nome = st.text_input("Seu Nome completo")
    with col_email:
        email = st.text_input("Seu melhor E-mail")
    
    telefone = st.text_input("WhatsApp (com DDD)")

    st.write("---")
    st.markdown("### 🏭 Perfil da Empresa")
    faturamento = st.number_input("Qual o seu faturamento mensal médio?", min_value=0.0, step=1000.0, format="%.2f")
    
    # Substituindo funcionários por Segmento
    segmento = st.selectbox("Qual o Segmento da sua empresa?", ["Comércio", "Serviço", "Indústria"])

# --- LÓGICA DO BOTÃO (CORRIGIDA) ---

if st.button("GERAR ANÁLISE TRIBUTÁRIA", use_container_width=True):
    if not nome or not email or not telefone or faturamento == 0:
        st.error("⚠️ Por favor, preencha todos os campos para gerar o diagnóstico.")
    else:
        # LÓGICA DE ANÁLISE (Inteligência Artificial da Novus)
        # Regra simplificada: Simples Nacional até 400k/mês (4.8M ano)
        if faturamento <= 400000:
            regime_sugerido = "Simples Nacional"
            recomendacao = "Sua empresa se enquadra no limite de faturamento do Simples Nacional, o que geralmente simplifica o recolhimento."
        
        # Indústria ou faturamento muito alto tende ao Lucro Real
        elif segmento == "Indústria" or faturamento > 1000000:
            regime_sugerido = "Lucro Real"
            recomendacao = "Pelo volume de faturamento ou segmento industrial, o Lucro Real pode oferecer créditos tributários vantajosos."
        
        # Caso contrário, Lucro Presumido
        else:
            regime_sugerido = "Lucro Presumido"
            recomendacao = "O Lucro Presumido pode ser a melhor opção para otimizar a carga tributária sobre sua margem de lucro."

        # 5. EXIBIÇÃO DO RESUMO DA ANÁLISE
        st.markdown(f"""
            <div class="result-card">
                <h3 style="color: #004A8D;">📋 Resumo do Diagnóstico</h3>
                <div style="text-align: left; margin-bottom: 20px; color: #404040;">
                    <p><b>Cliente:</b> {nome}</p>
                    <p><b>Segmento:</b> {segmento}</p>
                    <p><b>Faturamento Mensal:</b> R$ {faturamento:,.2f}</p>
                </div>
                <hr>
                <p style="font-size: 18px; color: #495057;">Regime Sugerido:</p>
                <div class="economy-value" style="color: #004A8D; font-size: 32px;">{regime_sugerido}</div>
                <p style="color: #6C757D; padding: 10px;">{recomendacao}</p>
                <hr>
                <a href="https://wa.me/5532999201923?text=Olá! Gere o diagnóstico para {nome} ({segmento}). O regime sugerido foi {regime_sugerido}. Quero validar!" class="cta-button">VALIDAR DIAGNÓSTICO COM ESPECIALISTA</a>
            </div>
        """, unsafe_allow_html=True)

        # Envio para o n8n (Atualizado com os novos campos)
        try:
            webhook_url = st.secrets["WEBHOOK_URL"]
            dados_lead = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "faturamento": faturamento,
                "segmento": segmento,
                "regime_sugerido": regime_sugerido
            }
            requests.post(webhook_url, json=dados_lead, timeout=5)
        except:
            pass
        
        # 3. Preparação dos dados para o Lead (Dicionário)
        dados_lead = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "faturamento": faturamento,
            "regime": regime,
            "economia_mensal": total_economia,
            "economia_anual": total_economia * 12
        }

        # 4. Envio para o n8n usando o Secret (Correção do SyntaxError)
        try:
            webhook_url = st.secrets["WEBHOOK_URL"] 
            requests.post(webhook_url, json=dados_lead, timeout=5)
        except Exception as e:
            # O erro de envio não trava a tela do cliente, apenas loga no servidor
            print(f"Erro no webhook: {e}")

        # 5. EXIBIÇÃO DO RESULTADO (Card Único)
        st.markdown(f"""
            <div class="result-card">
                <p style="font-size: 14px; color: #6C757D; margin-bottom: 5px;">
                    Olá <b>{nome}</b>! Veja o potencial de economia para sua empresa:
                </p>
                <div class="economy-value">R$ {total_economia:,.2f} / mês</div>
                <p style="color: #6C757D;">Isso representa <b>R$ {total_economia*12:,.2f}</b> de economia por ano.</p>
                <hr>
                <h4 style="color: #004A8D; font-size: 15px;">⚠️ Nota: Este cálculo é uma estimativa baseada em médias de mercado e não substitui uma análise técnica detalhada.</h4>
                <a href="https://wa.me/5532999201923?text=Olá! Meu nome é {nome} e usei a calculadora. Vi que posso economizar R$ {total_economia:,.2f} no regime {regime}." class="cta-button">FALAR COM ESPECIALISTA AGORA</a>
            </div>
        """, unsafe_allow_html=True)


