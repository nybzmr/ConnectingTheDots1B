MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K_SECTIONS = 5
DESCRIPTION = "Persona-Driven Document Intelligence System"
INPUT_HELP = "Path to challenge input JSON"
OUTPUT_HELP = "Path for challenge output JSON"

def get_current_timestamp() -> str:
    from datetime import datetime
    return datetime.now().isoformat()