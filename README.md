# 🚚 Intelligent Engine Maintenance Assistant: RAG-Powered Fleet Analytics

### **Open-Source End-to-End Solution for Trucking Industry Challenges**

---

## 🔥 Overview

The **Intelligent Engine Maintenance Assistant** is an open-source, production-ready Retrieval-Augmented Generation (RAG) system designed specifically for the trucking and logistics industry. It combines language models, vector similarity search, and domain-specific data to deliver instant, accurate maintenance advice, regulatory queries, and cost analysis for fleet managers, mechanics, and drivers.

---

## 🎯 Key Features

- **End-to-End RAG Pipeline**: Integrates document processing, embeddings, vector search, and large language models (Google AI Studio) into a seamless system.
- **Interactive Dashboard**: Built with Streamlit for intuitive query input and rich data visualization.
- **Knowledge Base**: Uses synthetic but realistic datasets including maintenance logs, diagnostics codes, and fleet info.
- **Source Citations & Confidence Scores**: Ensures transparency of generated answers.
- **Open Source & Extensible**: Modular, easy to modify, and tailored for scalability.

---

## 📝 Problem Statement

Fleet maintenance involves scattered, unstructured documentation, complex regulations, and real-time diagnostics—making quick, accurate decision-making difficult. Traditional reactive maintenance minimizes vehicle uptime and increases costs. This project aims to harness AI to synthesize unstructured data sources, streamline maintenance and compliance workflows, and reduce operational costs.

---

## 🚀 Demo & Capabilities

Users can input questions like:
- "What does OBD code P0171 mean for a 2019 Freightliner Cascadia?"
- "When should I replace the air filter on a truck with 150,000 miles?"
- "What are DOT brake inspection requirements?"

The system retrieves relevant info, generates precise answers, and displays analysis results—empowering maintenance teams with instant insights.

---

## 🛠️ Tech Stack

| Component | Technology / Library | Details |
| --------- | --------------------- | ------- |
| Language | Python 3.8+ | Main scripting language |
| Framework | Streamlit | Web UI/dashboard |
| RAG Orchestration | LangChain | Modular pipeline orchestration |
| Vector Store | Chroma | Lightweight, open-source vector database |
| Embeddings | Google AI Studio | Semantic text embeddings |
| LLM | Google Gemini (via API) | Text generation and reasoning |
| Data Processing | pandas, PyPDF2, etc. | Document & CSV handling |
| Monitoring | Logging, custom metrics | Performance tracking |

---

## 📂 Project Structure

