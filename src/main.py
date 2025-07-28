import argparse
import logging
from . import config
from .utils import load_json, save_json, setup_logging
from .pdf_parser import DocumentParser
from .embedding_utils import EmbeddingProcessor

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description=config.DESCRIPTION)
    parser.add_argument("--input-json", required=True, help=config.INPUT_HELP)
    parser.add_argument("--output-json", required=True, help=config.OUTPUT_HELP)
    args = parser.parse_args()

    try:
        # Load input data
        input_data = load_json(args.input_json)
        
        # Process documents
        parser = DocumentParser()
        sections = []
        for doc in input_data["documents"]:
            sections.extend(parser.process_document(doc["filename"]))
        
        # Process embeddings and ranking
        processor = EmbeddingProcessor(
            model_name=config.MODEL_NAME,
            top_k=config.TOP_K_SECTIONS
        )
        query = f"{input_data['persona'].get('role', '')} {input_data['job_to_be_done'].get('task', '')}"
        ranked_sections = processor.rank_sections(sections, query)
        
        # Generate output
        output = {
            "metadata": {
                "input_documents": [d["filename"] for d in input_data["documents"]],
                "persona": input_data["persona"],
                "job_to_be_done": input_data["job_to_be_done"],
                "processing_timestamp": config.get_current_timestamp()
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        
        for rank, section in enumerate(ranked_sections, start=1):
            output["extracted_sections"].append({
                "document": section.filename,
                "section_title": section.title,
                "importance_rank": rank,
                "page_number": section.page
            })
            best_paragraph = processor.select_best_paragraph(
                section.text, 
                query
            )
            output["subsection_analysis"].append({
                "document": section.filename,
                "refined_text": best_paragraph,
                "page_number": section.page
            })
        
        # Save output
        save_json(args.output_json, output)
        logging.info(f"Successfully generated output at {args.output_json}")
        
    except Exception as e:
        logging.exception(f"Processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()