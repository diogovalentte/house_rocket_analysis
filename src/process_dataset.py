import os
import pathlib
import logging
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)-8s :: %(name)s :: %(message)s",
)
logger = logging.getLogger("process_dataset")


def load_data(path: str) -> pd.DataFrame:
    """Load the dataset"""
    data = pd.read_csv(path)

    logger.info(
        f"load_data :: House Rocket dataset has been successfully loaded with {data.shape[0]} rows and {data.shape[1]} columns."
    )

    return data


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Process columns
    _columns = [
        "ID",
        "Date",
        "Price",
        "Bedrooms",
        "Bathrooms",
        "Sqft Living",
        "Sqft Lot",
        "Floors",
        "Waterfront",
        "View",
        "Condition",
        "Grade",
        "Sqft Above",
        "Sqft Basement",
        "Year Built",
        "Year Renovated",
        "ZipCode",
        "Latitude",
        "Longitude",
        "Sqft Living 15",
        "Sqft Lot 15",
    ]
    df.columns = _columns

    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d-%m-%Y")

    # Clean duplicated and missing rows
    duplicated_rows_number = df.duplicated().sum()
    logger.info(f"clean_data :: dataset has {duplicated_rows_number} duplicated rows")
    if duplicated_rows_number > 0:
        df = df.drop_duplicates()

    missing_rows_number = df.isnull().all(axis=1).sum()
    logger.info(f"clean_data :: dataset has {missing_rows_number} missing/null rows")
    if missing_rows_number > 0:
        df = df.dropna(how="all")

    return df


def main():
    folder_path = pathlib.Path(__file__).parent.resolve()
    source_dataset_path = os.path.join(folder_path, "../data/raw/kc_house_data.csv")
    df = pd.read_csv(source_dataset_path)

    df = clean_data(df)
    cleaned_dataset_path = os.path.join(
        folder_path, "../data/cleaned/houses_data.parquet"
    )
    logger.info(f"Saving cleaned dataset...")
    df.to_parquet(cleaned_dataset_path)
    logger.info(f"Cleaned dataset saved to: {cleaned_dataset_path}")


if __name__ == "__main__":
    main()
