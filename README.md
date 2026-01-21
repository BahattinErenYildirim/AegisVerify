# 🛡️ AegisVerify - AI Powered Information Verification System

**AegisVerify**, kullanıcı tarafından sağlanan metinleri, haberleri veya iddiaları analiz eden, çok katmanlı bir **Yapay Zeka Doğrulama ve Risk Analiz Sistemidir.**

## 🚀 Özellikler

* **🔍 Doğruluk Puanlaması:** İddiaları 0-100 arasında puanlar.
* **🌍 RAG (Retrieval-Augmented Generation):** Wikipedia, NewsAPI ve Google FactCheck servislerini tarayarak kanıt toplar.
* **⚠️ Scam & Fraud Tespiti:** Oltalama girişimlerini ve tehlikeli URL'leri tespit eder.
* **🧠 Mantıksal Analiz:** Metindeki çelişkileri ve mantık hatalarını (Logic Analyzer) bulur.
* **🤖 Çoklu Ajan Mimarisi:** Google Gemini tabanlı yapay zeka ile adli bilişim raporu hazırlar.

## 🛠️ Kurulum

Projeyi yerel makinenizde çalıştırmak için:

1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/KULLANICI_ADIN/AegisVerify.git](https://github.com/KULLANICI_ADIN/AegisVerify.git)
    cd AegisVerify
    ```

2.  **Gereksinimleri yükleyin:**
    ```bash
    pip install -r app/backend/requirements.txt
    pip install -r app/frontend/requirements.txt
    ```

3.  **Ortam Değişkenlerini (.env) Ayarlayın:**
    `app/backend/` içine `.env` dosyası oluşturun ve anahtarlarınızı ekleyin:
    ```ini
    GEMINI_API_KEY=your_key_here
    NEWS_API_KEY=your_key_here
    GOOGLE_FACTCHECK_KEY=your_key_here
    ```

4.  **Çalıştırın:**
    * Backend: `cd app/backend && uvicorn main:app --reload`
    * Frontend: `cd app/frontend && streamlit run streamlit_app.py`

## 🏗️ Teknoloji Yığını
* **Backend:** FastAPI, Python
* **Frontend:** Streamlit
* **AI:** Google Gemini 2.0 Flash
* **Search:** Wikipedia API, NewsAPI, Google FactCheck Tools