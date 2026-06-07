# 🚀 Jamestown Autonomous Hub

### Global Solution 2026.1 – FIAP
**Sistema Unificado de Gestão, Subsistência e Resiliência para Colônias em Ambientes Extremos**

**Disciplina:** Generative AI For Engineering (GAIE)  
**Grupo:**
* Breno Silva (RM99275)
* Eduardo Araujo (RM99758)
* Gabriela Trevisan (RM99500)
* Gustavo Akio (RM550241)
* Rafael Franck (RM550875)

---

## 🌌 1. Contexto do Problema Real
A consolidação de colônias permanentes em corpos celestes comerciais e de pesquisa estabeleceu a infraestrutura de software como o verdadeiro motor da nova corrida espacial. No entanto, operar em ambientes de radiação extrema, recursos severamente limitados e isolamento logístico total exige sistemas com tolerância a falhas quase nula. Falhas humanas na triagem de biossustentabilidade ou atrasos na resposta a falhas críticas de suporte à vida podem comprometer a segurança de toda a tripulação.

O **Jamestown Autonomous Hub** resolve esse problema unificando inteligência artificial, visão computacional, automação robótica de processos e engenharia de dados em uma plataforma protegida sob a filosofia Zero Trust. O sistema garante a subsistência alimentar da base e a integridade dos sistemas vitais sem sobrecarregar os astronautas.

### 🌎 Objetivos de Desenvolvimento Sustentável (ODS) Atendidos:
* **ODS 2 (Fome Zero e Agricultura Sustentável):** Garantido pelo monitoramento preditivo em tempo real e triagem de patologias nas estufas hidropônicas verticais da colônia.
* **ODS 9 (Indústria, Inovação e Infraestrutura):** Atendido pela criação de uma infraestrutura de software moderna, resiliente e segura para a economia orbital.

---

## 📊 2. Fonte dos Dados
Em conformidade com as diretrizes do projeto, utilizou-se um algoritmo generativo baseado em distribuições estatísticas controladas para simular o histórico físico-químico e operacional do ecossistema da base. O dataset gerado contém exatamente 1.200 linhas e 15 colunas, mapeando os seguintes parâmetros de telemetria dos sensores:

* timestamp: Registro temporal das leituras dos sensores (frequência de 15 minutos).
* module_id: Identificação do setor da estufa hidropônica (GH-01 a GH-04).
* ph: Equilíbrio químico da solução de nutrientes (Faixa ideal: 5.5 - 6.5).
* ec_ms_cm: Condutividade elétrica da água/nutrientes.
* co2_ppm: Concentração atmosférica de dióxido de carbono.
* temperature_c: Temperatura interna do módulo (estresse térmico).
* humidity_pct: Percentual de umidade relativa do ar.
* light_lux: Índice de luminosidade para o cultivo.
* radiation_msv: Radiação cósmica externa incidente.
* o2_pct: Nível de oxigênio no ambiente interno.
* pressure_kpa: Pressão de pressurização atmosférica da base.
* irrigation_cycles_24h: Ciclos de irrigação executados nas últimas 24 horas.
* vision_class: Output analítico do modelo de Visão Computacional (ACV).
  * 0 = Saudável | 1 = Alerta/Estresse | 2 = Patologia Crítica / Fungo
* component_temp_c: Temperatura física de bombas de sucção e recicladores.
* risk_label (Target): Diagnóstico final do estado do módulo (0 = Estável, 1 = Crítico).

---

## 🛠️ 3. Metodologia Utilizada
O pipeline de Machine Learning foi estruturado seguindo as melhores práticas de Engenharia de Dados:

1. Engenharia de Atributos: Criação de flags operacionais binárias (ph_out_of_range, humidity_low, radiation_high, component_overheat) e desenvolvimento do indicador complexo de estresse do ecossistema: environmental_stress_score.
2. Tratamento de Desbalanceamento Extremo: Como falhas severas representavam apenas 2.42% do histórico real coletado, aplicou-se a técnica SMOTE (Synthetic Minority Over-sampling Technique) exclusivamente no conjunto de treinamento (equilibrando a base em 937 amostras por classe), eliminando o viés algorítmico.
3. Validação Estratificada: Divisão dos dados em 80% para treino e 20% para teste utilizando amostragem estruturada, prevenindo o vazamento de dados (data leakage).

---

## 🤖 4. Modelos Testados e Resultados Obtidos
Foram implementados, calibrados e comparados dois modelos preditivos baseados em técnicas distintas de aprendizado supervisionado: Random Forest Classifier e XGBoost Classifier.

Os resultados consolidados na base de testes foram:

| Métrica | Random Forest Calibrado | XGBoost Classifier Calibrado |
| :--- | :---: | :---: |
| Acurácia Geral | 95.83% | 68.33% |
| Recall (Classe 1 - Crítico) | 0.00% | 50.00% |
| F1-Score (Classe 1 - Crítico) | 0.00% | 7.00% |

### 🧠 Análise de Métricas e Escolha do Melhor Modelo:
Em sistemas críticos aeroespaciais de suporte à vida, a métrica mais importante é o Recall (Sensibilidade), uma vez que um Falso Negativo (deixar um colapso iminente ocorrer sem alertar) é um evento catastrófico. 

O modelo Random Forest, apesar de possuir uma acurácia geral inflada (95.83%), obteve Recall nulo (0.00%), ignorando os cenários de falha reais. Já o XGBoost Classifier, calibrado com o hiperparâmetro scale_pos_weight baseado na proporção real de desbalanceamento, conseguiu capturar 50.00% das anomalias severas. Optou-se formalmente pelo XGBoost, aceitando uma taxa maior de falsos alarmes operacionais em troca do aumento drástico na segurança física da tripulação.

Apesar da baixa precisão, em ambientes aeroespaciais a detecção antecipada de falhas é mais importante do que a geração de alarmes adicionais.

---

## 🔍 5. Interpretação com SHAP
Para remover o aspecto de "caixa-preta" e garantir a auditabilidade das decisões tomadas pela IA, aplicou-se a técnica SHAP (SHapley Additive exPlanations):

* Ciclos de Irrigação (irrigation_cycles_24h): Apresentou-se como o atributo de maior peso global. Valores baixos empurram de forma drástica a predição em direção ao Alerta Crítico.
* Pressão Atmosférica (pressure_kpa): O modelo identificou que picos isolados de despressurização representam um vetor imediato de colapso operacional do sistema.

No deploy, os valores SHAP foram mapeados em regras lógicas de negócio, permitindo que a aplicação exiba justificativas textuais precisas sobre qual sensor disparou o risco para guiar os reparos dos astronautas.

*<img width="829" height="859" alt="image" src="https://github.com/user-attachments/assets/b7f8c21b-dec2-418a-a84e-5288e24ed617" />
*

---

## 🚀 6. Instruções para Execução do Projeto

### Pré-requisitos
Certifique-se de possuir o Python 3.8+ instalado e as dependências listadas abaixo:

pip install pandas numpy scikit-learn xgboost imbalanced-learn shap streamlit joblib matplotlib

### Executando o Painel de Telemetria Localmente
1. Clone este repositório:
git clonegit clone https://github.com/gabitrevisan/jamestown-autonomous-hub.git
cd gen-ai-for-eng
3. Certifique-se de que o arquivo best_jamestown_model.pkl está na mesma pasta do script app.py.

4. Inicie a aplicação web do Streamlit:
streamlit run app.py

---

## 🔗 7. Links da Aplicação
* Link do Repositório (GitHub): https://github.com/gabitrevisan/jamestown-autonomous-hub/tree/main/gen-ai-for-eng
* Link da Aplicação em Funcionamento: 

## 8. Requeriments 

pandas
numpy
scikit-learn
xgboost
imbalanced-learn
shap
streamlit
joblib
matplotlib
