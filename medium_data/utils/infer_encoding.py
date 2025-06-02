"""
Infers the enconding of a file using the `chardet` library.
"""

import chardet
from medium_data.utils.get_logger import get_logger

def infer_encoding(file_path: str) -> str:
    """
    Infers the encoding of a file.

    Args:
        file_path (str): Path to the file to infer encoding.

    Returns:
        str: The inferred encoding of the file.
    """
    try:

        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Read a sample of the file
            result = chardet.detect(raw_data)

            if 'encoding' not in result:
                raise ValueError("Encoding could not be detected.")

            return result['encoding']

    except Exception as e:
        raise ValueError(f"Error inferring encoding for '{file_path}': {e}")


if __name__ == "__main__":
    import argparse

    logger = get_logger(__name__)

    parser = argparse.ArgumentParser(description="Infer the encoding of a file.")

    parser.add_argument(
        "-f",
        "--file-path",
        type=str,
        required=True,
        help="Path to the file to infer encoding."
    )

    args = parser.parse_args()

    try:
        encoding = infer_encoding(args.file_path)
        logger.info(f"Inferred encoding for '{args.file_path}': {encoding}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")