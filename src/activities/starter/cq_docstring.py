""" Examples of docstring styles and functions and class that are un-documented. """
import sqlite3

import pandas as pd
from matplotlib import pyplot as plt
import os
from io import StringIO


# Google-style docstring specification: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
def get_column_names_g(db_path: str, table_name: str) -> list:
    """Retrieves a list of column names for the specified database table.

    Args:
        db_path: Path to the database file
        table_name: Name of the table

    Returns:
        col_names: List of column names
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    col_names = [row[1] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return col_names


# Numpy-style docstring: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
def get_column_names_n(db_path: str, table_name: str) -> list:
    """
        Retrieves a list of column names for the specified database table.

        Parameters
        ----------
        db_path : str
            Path to the database file.
        table_name : str
            Name of the table.

        Returns
        -------
        col_names: list
            List of column names.
        """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    col_names = [row[1] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return col_names


# Sphinx/reStructuredText style docstring: https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
# AI prompt:   /doc Sphinx format docstring
def get_column_names_s(db_path: str, table_name: str) -> list:
    """
        Retrieves a list of column names for the specified database table.

        :param db_path: Path to the database file.
        :type db_path: str
        :param table_name: Name of the table.
        :type table_name: str
        :return: List of column names.
        :rtype: list
        """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    col_names = [row[1] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return col_names


# Copilot in VSCode / PyCharm
# Place the cursor under the function name and generate a docstring e.g. '/doc Google-style docstring'
def generate_histogram(df: pd.DataFrame):
    """
    Generate and save histograms for columns in a pandas DataFrame.

    This function creates and saves three sets of histogram plots using matplotlib:
    1. Histograms for all plottable columns in the DataFrame.
    2. Histograms for the specific columns "participants_m" and "participants_f".
    3. Histograms for rows where the "type" column equals "summer".

    Saved files:
    - output/histogram_df.png
    - output/histogram_participants.png
    - output/histogram_summer.png

    Args:
        df (pd.DataFrame): Input DataFrame containing numeric columns to plot. The DataFrame
            is expected to include the columns "participants_m", "participants_f", and "type"
            if the corresponding specialized histograms are to be produced.

    Returns:
        None

    Raises:
        KeyError: If the DataFrame does not contain required columns ("participants_m",
            "participants_f", or "type") when those specific histograms are attempted.
        ValueError: If the DataFrame contains no plottable numeric columns for the general
            histogram operation.
        OSError: If the output directory does not exist and cannot be created or if files
            cannot be written to disk.

    Notes:
        - The function uses matplotlib's DataFrame.hist method and saves figures with
          plt.savefig. Calling the function repeatedly without clearing figures may
          result in unexpected plot content; callers may wish to call plt.clf() or
          plt.close() between calls.
        - Ensure that an "output" directory exists or is writable before calling.
        - Non-numeric columns are ignored by the generic histogram call.
        - Filtering for summer histograms is done with df['type'] == 'summer'.

    Examples:
        >>> generate_histogram(df)
        This will save three PNG files into the "output" directory as described above.
    """
    # Histogram of any columns with values of a data type that can be plotted
    df.hist(
        sharey=False,  # defines whether y-axes will be shared among subplots.
        figsize=(12, 8)  # a tuple (width, height) in inches
    )
    plt.savefig("output/histogram_df.png")

    # Histograms of specific columns only
    df[["participants_m", "participants_f"]].hist()
    plt.savefig("output/histogram_participants.png")

    # Histograms based on filtered values
    summer_df = df[df['type'] == 'summer']
    summer_df.hist(sharey=False, figsize=(12, 8))
    plt.savefig("output/histogram_summer.png")


# Copilot in VSCode / PyCharm
# If you are happy to use gen-AI tools, place the cursor under the docstring and ask the AI to generate the code
def describe(csv_data_file: str) -> dict:
    """Opens the data as a pandas DataFrame applies pandas functions to describe the data.

    Applies the following pandas functions to the DataFrame and prints the output to file instead of terminal:
        df.shape
        df.head(num)
        df.tail(num)
        df.columns
        df.dtypes
        df.describe()
        df.info()

       Args:
       csv_data_file (str): File path of the .csv format data file.

    """
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Read CSV into DataFrame
    try:
        df = pd.read_csv(csv_data_file)
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise

    # Prepare output file and write textual summaries
    out_path = os.path.join("output", "describe_output.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(f"Source file: {csv_data_file}\n\n")

        fh.write("Shape:\n")
        fh.write(f"{df.shape}\n\n")

        fh.write("Head (first 5 rows):\n")
        fh.write(df.head().to_string() + "\n\n")

        fh.write("Tail (last 5 rows):\n")
        fh.write(df.tail().to_string() + "\n\n")

        fh.write("Columns:\n")
        fh.write(", ".join(map(str, df.columns)) + "\n\n")

        fh.write("Dtypes:\n")
        fh.write(df.dtypes.to_string() + "\n\n")

        fh.write("Describe:\n")
        fh.write(df.describe(include="all").to_string() + "\n\n")

        fh.write("Info:\n")
        buf = StringIO()
        df.info(buf=buf)
        fh.write(buf.getvalue())

    # Return a dictionary of results for programmatic use
    result = {
        "shape": df.shape,
        "head": df.head().to_dict(orient="records"),
        "tail": df.tail().to_dict(orient="records"),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "describe": df.describe(include="all").to_dict(),
        "info_file": out_path,
    }
    return result
    pass
