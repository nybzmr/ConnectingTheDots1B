## Methodology

Our solution uses a three-stage approach:

1. **Document Parsing:**
   - PDF text extraction using PDFMiner
   - Section detection using regex-based heading detection
   - Fallback to full document text when section detection fails

2. **Semantic Ranking:**
   - Sentence-BERT embeddings (`all-MiniLM-L6-v2`) for content representation
   - FAISS for efficient similarity search
   - Query formulation combining persona and job description

3. **Subsection Extraction:**
   - Paragraph-level embedding comparison
   - Selection of most relevant paragraph within top sections

Key optimizations:
- L2 normalization for better cosine similarity
- Efficient text chunking
- Batch processing of embeddings
- Lightweight model (80MB) for CPU execution