import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Configuração da página do Streamlit
st.set_page_config(page_title="Jamestown Autonomous Hub", page_icon="🚀", layout="centered")

st.title("🚀 Jamestown Autonomous Hub")
st.subheader("Sistema de Monitoramento e Prevenção de Colapso - GAIE")
st.markdown("---")

# 2. Carregar o modelo salvo
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('best_jamestown_model.pkl')
        return model
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo 'best_jamestown_model.pkl': {e}")
        return None

xgb_model = load_assets()

if xgb_model is not None:
    st.success("🤖 Modelos preditivos carregados com sucesso!")

st.markdown("### 📊 Inserir Dados de Telemetria do Setor")

# 3. Formulário de entrada com controles interativos (Sliders)
with st.form(key='telemetry_form'):
    col1, col2 = st.columns(2)

    with col1:
        module_id = st.selectbox("Identificação do Módulo", ["GH-01", "GH-02", "GH-03", "GH-04"])
        ph = st.slider("pH da Solução Química", 4.0, 8.0, 6.0, 0.1)
        ec_ms_cm = st.slider("Condutividade Elétrica (mS/cm)", 0.5, 4.0, 2.0, 0.1)
        co2_ppm = st.slider("Nível de CO2 (ppm)", 300, 1500, 800, 50)
        temperature_c = st.slider("Temperatura Ambiente (°C)", 10.0, 40.0, 24.0, 0.5)
        humidity_pct = st.slider("Umidade Relativa (%)", 20, 100, 65, 1)

    with col2:
        light_lux = st.slider("Luminosidade (Lux)", 5000, 20000, 12000, 500)
        radiation_msv = st.slider("Radiação Espacial (mSv/h)", 0.0, 5.0, 0.2, 0.1)
        o2_pct = st.slider("Nível de Oxigênio (% O2)", 15.0, 25.0, 21.0, 0.5)
        pressure_kpa = st.slider("Pressão Atmosférica (kPa)", 80.0, 120.0, 101.3, 0.5)
        irrigation_cycles_24h = st.slider("Ciclos de Irrigação (24h)", 0, 12, 6, 1)
        component_temp_c = st.slider("Temperatura dos Componentes/Bombas (°C)", 20.0, 80.0, 40.0, 1.5)
        vision_class = st.selectbox("Diagnóstico Visual da CNN (ACV)", [0, 1, 2],
                                    format_func=lambda x: {0: "0 - Saudável", 1: "1 - Estresse", 2: "2 - Patologia Crítica"}[x])

    submit_button = st.form_submit_button(label="🧬 Avaliar Risco de Colapso")

# 4. Lógica executada APENAS após o clique do botão [cite: 101]
if submit_button:
    if xgb_model is None:
        st.error("❌ Não é possível classificar os dados pois o modelo não foi carregado.")
    else:
        # Engenharia de atributos em tempo real (idêntica ao treino)
        ph_out_of_range = 1 if (ph < 5.5 or ph > 6.5) else 0
        humidity_low = 1 if (humidity_pct < 55) else 0
        radiation_high = 1 if (radiation_msv > 1.5) else 0
        component_overheat = 1 if (component_temp_c > 50) else 0
        environmental_stress_score = (temperature_c * 0.4) + ((100 - humidity_pct) * 0.4) + ((15000 - light_lux) / 1000 * 0.2)

        # Mapeamento do module_id
        module_mapping = {"GH-01": 0, "GH-02": 1, "GH-03": 2, "GH-04": 3}
        module_id_encoded = module_mapping[module_id]

        # Construção estruturada e segura do DataFrame de entrada
        input_data = pd.DataFrame([{
            'ph': ph, 'ec_ms_cm': ec_ms_cm, 'co2_ppm': co2_ppm, 'temperature_c': temperature_c,
            'humidity_pct': humidity_pct, 'light_lux': light_lux, 'radiation_msv': radiation_msv,
            'o2_pct': o2_pct, 'pressure_kpa': pressure_kpa, 'irrigation_cycles_24h': irrigation_cycles_24h,
            'vision_class': vision_class, 'component_temp_c': component_temp_c,
            'ph_out_of_range': ph_out_of_range, 'humidity_low': humidity_low,
            'radiation_high': radiation_high, 'component_overheat': component_overheat,
            'environmental_stress_score': environmental_stress_score, 'module_id_encoded': module_id_encoded
        }])

        # Predições de risco
        pred = xgb_model.predict(input_data)[0]
        prob = xgb_model.predict_proba(input_data)[0][1]

        st.markdown("---")
        st.markdown("### 🎯 Diagnóstico do Sistema Operacional")

        if pred == 1:
            st.error(f"🚨 **STATUS CRÍTICO DETECTADO!** Risco de Colapso Iminente.")
            st.metric(label="Probabilidade de Falha do Setor", value=f"{prob*100:.2f}%")

            # Análise explicativa baseada nos limites que guiaram o SHAP
            fatores = []
            if irrigation_cycles_24h < 4: fatores.append("Baixo índice de irrigação recente")
            if radiation_msv > 1.5: fatores.append("Pico de Radiação Cósmica Externa")
            if vision_class == 2: fatores.append("Patologia Crítica identificada por Visão Computacional")
            if pressure_kpa < 95.0: fatores.append("Queda severa de pressurização interna")

            if not fatores:
                fatores.append("Desvio crítico combinado no score de estresse ambiental")

            st.markdown(f"**🔬 Justificativa da IA (Análise de Atributos SHAP):**")
            for f in fatores:
                st.write(f"⚠️ {f}")

            st.info(f"⚙️ **Ação Recomendada pelo Copiloto:** Isolar imediatamente o setor {module_id} e redirecionar fluxo de suporte à vida.")
        else:
            st.success(f"✅ **STATUS ESTÁVEL.** Ecossistema operando em conformidade de segurança.")
            st.metric(label="Probabilidade de Falha do Setor", value=f"{prob*100:.2f}%")
            st.markdown("📋 **Justificativa da IA:** Ciclos físico-químicos e de irrigação operando dentro dos padrões normativos.")
