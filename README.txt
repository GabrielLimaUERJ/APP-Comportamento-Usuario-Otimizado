# 🚀 Análise de Comportamento de Usuários (App Interativo)

## 🎯 Objetivo

Desenvolver uma aplicação completa de análise de dados capaz de:

* Simular o comportamento de usuários em um ambiente digital
* Processar e analisar os dados em tempo real
* Exibir métricas e insights através de um dashboard interativo

O foco do projeto é demonstrar a construção de um **produto de dados end-to-end**, integrando geração, análise e visualização em uma única aplicação.

---

## 🧠 Conceito de Negócio

O projeto simula um funil de conversão:

**visita → clique → compra**

A partir disso, são analisados:

* Taxa de conversão entre etapas
* Drop-off (perda de usuários no funil)
* Performance por canal de aquisição
* Performance por dispositivo

---

## 🛠️ Tecnologias Utilizadas

* **Python** → geração de dados e lógica da aplicação
* **DuckDB** → execução de queries SQL em memória
* **Streamlit** → construção do dashboard interativo
* **Plotly** → visualização avançada (funil de conversão)

---

## 🔄 Como Funciona

A aplicação segue um fluxo automatizado:

1. **Simulação de Dados**

   * Geração de eventos de usuários
   * Eventos: visita, clique e compra
   * Atributos: origem de tráfego e dispositivo

2. **Processamento com SQL**

   * Criação de tabela em memória com DuckDB
   * Cálculo de métricas de conversão
   * Agregações por origem e device

3. **Visualização Interativa**

   * KPIs de conversão
   * Gráfico de funil
   * Análises segmentadas
   * Insights automáticos

---

## 📊 Funcionalidades

* 🔄 Geração dinâmica de dados (botão de simulação)
* 📈 KPIs automáticos de conversão
* 🔻 Funil de conversão interativo
* 🌐 Análise por origem de tráfego
* 💻 Análise por dispositivo
* 🧠 Geração automática de insights

---

## ▶️ Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/user-behavior-app.git
cd user-behavior-app
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o app:

```bash
streamlit run app.py
```

---

## 📁 Estrutura do Projeto

```text
📦 user-behavior-app
 ┣ 📜 app.py
 ┣ 📜 requirements.txt
 ┗ 📄 README.md
```

---

## 📈 Principais Métricas

* Taxa de conversão total (~25%)
* Conversão visita → clique (~70%)
* Conversão clique → compra (~35%)

---

## 🧠 Insights

* A maior perda ocorre na etapa final do funil (compra)
* Indica possível fricção no processo de conversão
* Diferenças entre canais permitem identificar oportunidades de otimização
* Consistência entre dispositivos sugere experiência equilibrada