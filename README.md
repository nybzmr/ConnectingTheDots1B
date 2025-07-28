Thank you for the context and the screenshot. Based on your folder structure, methodology, and the challenge theme **"Connect What Matters — For the User Who Matters"**, here’s a complete and professional `README.md` tailored for your project: **ConnectingTheDots1B**.

---

```markdown
# 🧠 ConnectingTheDots1B

> **Theme:** “Connect What Matters — For the User Who Matters”

ConnectingTheDots1B is an intelligent document analysis system designed to extract and prioritize the most relevant content from a collection of PDFs based on a specific **persona** and their **job-to-be-done**. It enables users such as researchers, analysts, or students to gain targeted insights from large, unstructured documents — fast and with precision.

---

## 🧩 Problem Statement

Given:
- A set of 3–10 related **PDF documents**
- A **persona**: a detailed role profile (e.g., PhD Researcher, Student, Analyst)
- A **job-to-be-done**: a specific task that persona wants to achieve (e.g., literature review, summary extraction)

Your task: Automatically find the most **relevant sections and paragraphs** across the PDFs that help this persona achieve their goal.

---

## 🔍 Methodology

We implement a **three-stage pipeline**:

### 1. 📄 Document Parsing
- Extracts raw text using `PDFMiner`
- Detects sections using **regex-based heading matching**
- Fallback to full document extraction if structured headings are unavailable

### 2. 🧠 Semantic Ranking
- Sentence embeddings via `all-MiniLM-L6-v2` (using `SentenceTransformers`)
- `FAISS` used for efficient semantic search
- Embedding-based query formulation combining **persona** and **job**

### 3. 🧬 Subsection Extraction
- Paragraph-level comparison against ranked sections
- Identifies and returns most relevant **paragraphs** within each top section

#### 🛠 Optimizations
- L2-normalized cosine similarity
- Efficient chunking and batching
- Lightweight embedding model (~80MB) optimized for CPU execution

---

## ⚙️ Setup & Usage

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/nybzmr/ConnectingTheDots1B.git
cd ConnectingTheDots1B
````

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Run Locally

```bash
python run.py --input-json challenge1b_input.json --output-json challenge1b__output.json
```

### 🐳 Run with Docker (Recommended)

```bash
docker build -t ctd1b .
docker run --rm -v $(pwd):/app ctd1b
```

---

## 📌 Constraints

* 💻 Runs entirely on **CPU**
* 🧠 Model size < **1 GB**
* ⚡ Processing time ≤ **60 seconds** for 3–5 PDFs
* 🔌 No internet access required during execution

---


## 👤 Author

**Nayaab Zameer**
GitHub: [@nybzmr](https://github.com/nybzmr)

---

## 📜 License

MIT License — see `LICENSE` file for details.

---

## 🌐 Future Improvements

* GUI or web dashboard
* Persona-sensitivity tuning
* Offline PDF visual annotation

---

## 🧠 “Connect What Matters — For the User Who Matters”

This project reflects a belief that information is only as valuable as it is relevant. By bridging documents with people’s goals, ConnectingTheDots1B empowers **purpose-driven reading**.

```

---
