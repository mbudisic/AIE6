from typing import Tuple
import pandas as pd
from functools import partial
import numpy as np


def summary_stats(df: pd.DataFrame, mean_label="Mean", std_label="StdDev"):
    """
    Adds summary rows (mean and standard deviation) to a pandas DataFrame.

    This function calculates the mean of numeric columns and estimates the standard
    deviation using a jackknife resampling method. It then appends these summary
    statistics as new rows to the original DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame to summarize
        mean_label (str, optional): Label for the mean row. Defaults to "Mean".
        std_label (str, optional): Label for the standard deviation row. Defaults to "StdDev".

    Returns:
        pd.DataFrame: Original DataFrame with summary rows appended

    Raises:
        ValueError: If the DataFrame has fewer than 2 rows (needed for jackknife estimation)
    """
    # 1. Identify numeric vs non-numeric columns
    df = df.infer_objects()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    non_numeric_cols = df.columns.difference(numeric_cols)

    n = len(df)
    if n < 2:
        raise ValueError("Need at least two rows for jackknife estimate")

    # 2. Compute the plain mean
    means = df[numeric_cols].mean()

    # 3. Compute jackknife leave-one-out std dev
    jackknife_std = {}
    # total sums up front for speed
    col_sums = df[numeric_cols].sum()
    for col in numeric_cols:
        x = df[col].values
        # leave-one-out means: (sum(x) - x[i])/(n-1)
        loo_means = (col_sums[col] - x) / (n - 1)
        # jackknife variance formula: (n-1)/n * Σ (θ_i – θ̄)²
        theta = loo_means.mean()
        var = (n - 1) / n * np.sum((loo_means - theta) ** 2)
        jackknife_std[col] = np.sqrt(var)

    jackknife_std = pd.Series(jackknife_std)

    # 4. Build a 2×cols DataFrame for the summary rows
    summary = pd.DataFrame(index=[mean_label, std_label], columns=df.columns)

    # fill numeric summaries
    for col in numeric_cols:
        summary.at[mean_label, col] = means[col]
        summary.at[std_label, col] = jackknife_std[col]
    # fill non-numeric with labels
    for col in non_numeric_cols:
        summary.at[mean_label, col] = mean_label
        summary.at[std_label, col] = std_label

    # 5. Concatenate and return
    retval = pd.concat([df, summary], axis=0)
    # Convert columns to numeric where possible, ignoring errors
    retval = retval.apply(partial(pd.to_numeric))
    # Infer the best data types for each column
    retval = retval.infer_objects()
    return retval


def combine_stats(
    dfs: Tuple[pd.DataFrame, ...], field: str, names: Tuple[str, ...]
) -> pd.DataFrame:
    """
    Combine statistics from multiple DataFrames for a specific field.

    Args:
        dfs: Tuple containing pandas DataFrames to compare
        field: The field name to extract from all DataFrames
        names: Tuple of strings to use as labels for the DataFrames in the output
             (must have the same length as dfs)

    Returns:
        pd.DataFrame: Combined statistics with rows labeled according to names
    """
    if len(dfs) != len(names):
        raise ValueError("Number of DataFrames must match number of names")

    # Extract the field row from each DataFrame and combine them
    field_data = []
    for df in dfs:
        # Get the row for the specified field
        row_data = df.loc[[field]]
        field_data.append(row_data)

    # Combine all the data
    combined_stats = pd.concat(field_data)
    # Set the index to the model names
    combined_stats.index = names
    return combined_stats.select_dtypes(include="number")


def z_test(mu1, mu2, se1, se2):
    """
    Perform a two-sample z-test to compare two means.

    Args:
        mu1: Mean of the first sample
        mu2: Mean of the second sample
        se1: Standard error of the first sample
        se2: Standard error of the second sample

    Returns:
        Tuple[float, float]: z-statistic and p-value for the test
    """

    z = (mu2 - mu1) / np.sqrt(se1**2 + se2**2)
    p = 2 * norm.sf(abs(z))
    return z, p
