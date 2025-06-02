"""
Converts CSV files to Parquet format, using pyarrow.
"""

from typing import Tuple
import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq
from medium_data.utils.infer_encoding import infer_encoding
from medium_data.utils.get_logger import get_logger

THIS_FILE_NAME = __file__.split("/")[-1]

def convert_csv_to_parquet(csv_file: str, parquet_file: str, encoding: str) -> Tuple[bool, str]:
    """
    Convert a CSV file to Parquet format.

    Args:
        csv_file (str): Path to the input CSV file.
        parquet_file (str): Path to the output Parquet file.
    """

    logger = get_logger(THIS_FILE_NAME)

    writer = None

    try:
        read_opts = pv.ReadOptions(encoding=encoding, block_size=64 * 1024 * 1024)
        batch_count = 0

        with pv.open_csv(csv_file, read_options=read_opts) as reader:
            for batch in reader:
                if writer is None:
                    writer = pq.ParquetWriter(parquet_file, batch.schema)
                writer.write_table(pa.Table.from_batches([batch]))
                batch_count += 1
                if batch_count % 100 == 0:
                    logger.info(f"Processed {batch_count} batches...")

    except Exception as e:
        return (False, f"Error converting '{csv_file}' to Parquet: {e}")

    finally:
        if writer:
            writer.close()

    logger.info(f"Conversion complete. Total batches: {batch_count}")
    return (True, "")


def main(
    csv_file: str,
    parquet_file: str,
) -> None:
    """
    Main function to convert CSV to Parquet.

    Args:
        csv_file (str): Path to the input CSV file.
        parquet_file (str): Path to the output Parquet file.
        encoding (str, optional): Encoding of the CSV file. If None, it will be inferred.
    """

    logger = get_logger(THIS_FILE_NAME)

    try:
        encoding = infer_encoding(csv_file)

        logger.info(f"Inferred encoding for '{csv_file}': {encoding}")

        success = convert_csv_to_parquet(csv_file, parquet_file, encoding)

        if success[0]:
            logger.info(f"Successfully converted '{csv_file}' to '{parquet_file}'.")
        else:
            logger.info(success[1])

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert CSV files to Parquet format.")

    parser.add_argument(
        "-c",
        "--csv-file",
        type=str,
        required=True,
        help="Path to the input CSV file."
    )

    parser.add_argument(
        "-p",
        "--parquet-file",
        type=str,
        required=True,
        help="Path to the output Parquet file."
    )

    args = parser.parse_args()

    main(args.csv_file, args.parquet_file)