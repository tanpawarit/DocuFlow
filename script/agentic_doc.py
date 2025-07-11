import os
from typing import Any, List

from agentic_doc.parse import parse

os.environ["VISION_AGENT_API_KEY"] = (
    "ZTVrc2JiamN0MDA5ZGprbHh6MmdtOlFSdTZhVlFKcGo2cDBuYjBOYm1uZWY2QlQzd21nZ1Zo"
)


def extract_credit_note_data(image_path: str) -> None:
    """
    Extracts and prints data from a credit note image using agentic-doc.
    Args:
        image_path (str): Path to the credit note image file.
    """
    results: List[Any] = parse(image_path)
    if not results:
        print("No data extracted.")
        return
    result = results[0]
    print("--- Extracted Markdown ---")
    print(result.markdown)
    print("\n--- Structured Chunks ---")
    for chunk in result.chunks:
        print(chunk)


def main() -> None:
    """Main function to extract data from credit_note_1.png."""
    image_path: str = "/Users/pawarison/dev/DocuFlow/data/synthetic_data/credit_notes/credit_note_1.png"
    extract_credit_note_data(image_path)


if __name__ == "__main__":
    main()
