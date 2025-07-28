The intelligent document analyst is implemented as a CPU‑only pipeline optimized for sub‑1 GB models and sub‑60 s processing on 3–5 PDFs. The core methodology comprises four stages:

1. **Parsing & Segmentation**

   * We use `pdfminer.six` to convert each PDF into a raw text stream.
   * Pages are segmented into headings and paragraphs via simple regex patterns (e.g., lines starting with digits or uppercase words) to identify section titles.
   * Each section record retains: document ID, title, page number, and raw text.

2. **Embedding & Indexing**

   * A lightweight sentence‑transformers model (e.g., `all-MiniLM-L6-v2`, \~117 MB) encodes each section into a 384‑dimensional vector (model + PyTorch \~400 MB total).
   * We build a FAISS flat index (`IndexFlatL2`) for rapid similarity search.
   * All embeddings are computed once per run and stored in RAM, ensuring < 1 GB memory footprint.

3. **Persona + Job Query Construction**

   * We concatenate the persona description and the job‑to‑be‑done into a single query string.
   * The query is embedded with the same sentence‑transformer model, yielding a query vector.

4. **Retrieval, Ranking & Output**

   * FAISS returns the top K nearest sections by L2 distance.
   * We assign an **importance\_rank** based on inverse distance (closer → higher rank).
   * For each top section, we also extract and refine sub‑paragraphs by splitting on sentence boundaries and re‑ranking them against the query embedding to produce a refined text snippet.
   * A JSON builder aggregates all results into the specified schema:

     ```json
     {
       "metadata": { "documents": [...], "persona": "...", "job": "...", "timestamp": "..." },
       "sections": [ { "document": "...", "page": 5, "title": "Methodology", "importance_rank": 1 }, ... ],
       "subsections": [ { "document": "...", "page": 5, "text": "...", "rank": 1 }, ... ]
     }
     ```
   * Processing is done within 60 s for up to 5 PDFs on standard CPUs (2–4 cores).

**Key Optimizations & Constraints**

* **Model size**: We choose a MiniLM variant to stay under 1 GB.
* **No internet at runtime**: All models are downloaded at build time inside `requirements.txt`.
* **Dockerized**: The entire pipeline is containerized to ensure consistency across environments.

