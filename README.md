# AgriBoot – AI-Powered Agricultural Advisory System

AgriBoot is an intelligent agricultural advisory platform designed to assist farmers with accurate, context-aware, and easy-to-understand recommendations. By combining Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), hybrid intent classification, and semantic entity extraction, AgriBoot delivers personalized agricultural guidance in real time.

Whether a farmer wants to know the best fertilizer for wheat, identify a crop disease, or learn irrigation practices, AgriBoot provides reliable answers grounded in domain-specific agricultural knowledge.

The platform is available across multiple interfaces:

- Web Application (Streamlit)
- Desktop Application (PyQt5)
- Mobile Application (React Native)
- FastAPI Backend for seamless integration

---

## Key Features

- Multi-Stage Intent Classification
- Retrieval-Augmented Generation (RAG)
- Semantic Entity Extraction
- Domain-Specific Agricultural Knowledge Base
- LLM-Powered Answer Generation
- Cross-Platform Support
- FastAPI-Based Backend Services
- Pinecone Vector Database Integration
- Real-Time Agricultural Recommendations

---

## System Workflow

AgriBoot follows a multi-stage pipeline to generate intelligent responses:

### Step 1: User Query

A farmer asks a question such as:

> "Which fertilizer is best for wheat?"

---

### Step 2: Intent Classification

The system identifies the user's intent using a hybrid approach:

- Keyword Matching
- Embedding Similarity
- Zero-Shot Classification

Supported intents include:

| Code | Intent |
|------|--------|
| CD | Crop Disease |
| FR | Fertilizer Recommendation |
| HT | Harvest Guidance |
| I | Irrigation |
| PC | Pest Control |
| SM | Soil Management |
| M | Agricultural Machinery |
| MP | Market Price Information |

---

### Step 3: Entity Extraction

AgriBoot extracts relevant agricultural entities such as:

- Crop Name
- Disease Name
- Fertilizer
- Pesticide
- Equipment
- Soil Type

---

### Step 4: Knowledge Retrieval

Relevant information is retrieved from a Pinecone vector database containing agricultural documents and expert resources.

---

### Step 5: AI Response Generation

The retrieved context is provided to a Groq-powered LLM (Llama 3.1), which generates a clear and farmer-friendly response.

---

## Architecture

```text
Farmer Query
      │
      ▼
Intent Classification
      │
      ▼
Entity Extraction
      │
      ▼
Semantic Retrieval (Pinecone)
      │
      ▼
RAG Pipeline
      │
      ▼
LLM Response Generation
      │
      ▼
Agricultural Advisory
```

---

## Project Structure

```text
AgriBoot/
│
├── backend/
│   ├── config.py
│   ├── constants.py
│   ├── data_loader.py
│   ├── embeddings.py
│   ├── entity_extractor.py
│   ├── generator.py
│   ├── intent_classifier.py
│   ├── retriever.py
│   ├── pipeline.py
│   └── main.py
│
├── data/
│   └── raw/
│
├── frontend/
│   ├── app/
│   └── web/
│
├── scripts/
│   └── build_index.py
│
├── .env
├── requirements.txt
├── environment.yml
└── README.md
```

---

## Technology Stack

| Category | Technologies |
|---------|--------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit, PyQt5, React Native |
| Vector Database | Pinecone |
| LLM | Llama 3.1 (Groq) |
| Embeddings | all-MiniLM-L6-v2 |
| NLP | Sentence Transformers |
| Deployment | Docker |
| API Testing | Swagger UI |

---

## Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd AgriBoot
```

---

### Create Virtual Environment

#### Using Conda

```bash
conda create -n agriboot python=3.11 -y
conda activate agriboot
```

#### Using venv

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

Optional:

```bash
python -m spacy download en_core_web_sm
```

---

## Configure Environment Variables

Create a `.env` file:

```env
PINECONE_API_KEY=your_api_key
PINECONE_INDEX_NAME=farmer-advisory
GROQ_API_KEY=your_groq_api_key
API_URL=http://localhost:8000
```

---

## Build the Knowledge Base

Place all agricultural PDF and TXT documents inside:

```text
data/raw/
```

Build the vector index:

```bash
python scripts/build_index.py
```

This process:

- Loads documents
- Splits text into chunks
- Generates embeddings
- Uploads vectors to Pinecone

---

## Running the Backend

Start the FastAPI server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Visit:

```text
http://localhost:8000/docs
```

to access the Swagger API documentation.

---

## Sample API Request

```bash
curl -X POST http://localhost:8000/ask \
-H "Content-Type: application/json" \
-d '{"query":"best fertilizer for wheat"}'
```

---

## Running the Web Application

```bash
streamlit run frontend/web/app.py
```

Open:

```text
http://localhost:8501
```

### Features

- Modern User Interface
- Query History
- Intent Detection
- Confidence Scores
- Retrieved Context Visualization
- AI Advisory Cards

---

## Desktop Application

Launch the desktop application:

```bash
python -m frontend.app.agriboot_desktop
```

### Desktop Features

- WhatsApp-Style Chat Interface
- Typing Indicators
- Metadata Pills
- Entity Badges
- Query History
- Cross-Platform Support

---

## Mobile Application

```bash
cd mobile
npm install
npx expo start
```

The mobile application communicates with the same FastAPI backend.

---

## Packaging as an Executable

Generate a Windows executable:

```bash
pip install pyinstaller

pyinstaller \
--onefile \
--windowed \
--name AgriBoot \
agriboot_desktop.py
```

The generated executable will be available in:

```text
dist/
```

---

## Customization

| Component | File |
|----------|------|
| Intent Keywords | `backend/constants.py` |
| Embedding Model | `.env` |
| Chunk Size | `.env` |
| Chunk Overlap | `.env` |
| LLM Model | `.env` |

---

## Future Scope

- Voice-Based Farmer Interaction
- Multilingual Support
- Satellite Data Integration
- Weather Forecasting
- Crop Yield Prediction
- Offline Mobile Support
- Smart Irrigation Recommendations

---

## Why AgriBoot?

AgriBoot bridges the gap between farmers and modern AI technologies by providing intelligent, accessible, and context-aware agricultural guidance. By leveraging Retrieval-Augmented Generation and Large Language Models, the platform empowers farmers to make informed decisions that improve productivity, sustainability, and profitability.

---

## License

This project is licensed under the MIT License.

---

## Author

**Rousan Ali**

- B.Tech in Information Technology
- AI & Machine Learning Researcher
- Developer of AgriBoot

> "Empowering Agriculture Through Artificial Intelligence."