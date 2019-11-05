import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def error_plot(df, path, ext):
    """
    Reads log data in pandas DataFrame format and creates error plots for 
    each function of the 3DPOD at a given directory with a given extension

    Parameters
    ----------
    df      :   pandas.DataFrame    
        DataFrame containing log data - usually read from csv produced by reader
    path    :   string    
        Path for output plots
    ext     :   string
        Image extension to define the format ("png","pdf","svg"...)

    Returns
    -------
    Nothing

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame.
        If path is not a string
        If ext is not a string
    ValueError
        If ext is not a supported extension for an image format.
    FileNotFoundError
        If path does not exist.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be an pandas DataFrame"
        )
    else:
        # Quantile method raises error for obj types
        df_no_obj = df.iloc[:, 1:-1]
        mean = df_no_obj.groupby("Number of processors").mean()
        p025 = df_no_obj.groupby("Number of processors").quantile(0.025)
        p975 = df_no_obj.groupby("Number of processors").quantile(0.975)

        for i in range(0, 7):
            plt.figure()
            (_, caps, _) = plt.errorbar(
                mean.index,
                mean.iloc[:, i],
                yerr=[mean.iloc[:, i] - p025.iloc[:, i],
                      p975.iloc[:, i] - mean.iloc[:, i]],
                linestyle="-",
                fmt="o",
                markersize=8,
                capsize=5,
            )
            for cap in caps:
                cap.set_markeredgewidth(1)
            plt.title(mean.columns[i])
            plt.ylabel("Time [s]")
            plt.xlabel("Number of processors")
            plt.savefig(
                os.path.join(path, "errorbar_" + str(i) + "." + ext),
                bbox_inches="tight"
            )


def reduce_df(df):
    """
    Takes in log-based DataFrame and performs two actions:
    1) Reduces the number of functions to only "Reading", "Computing" and "Writing"
    based on the column headers by summing up the functions that fit in that category
    2) Takes the average over all passess and number of processors

    Parameters
    ----------
    df      :   pandas.DataFrame    
        DataFrame containing log data - usually read from csv produced by reader

    Returns
    -------
    df_r    :   pandas.DataFrame    
        Reduced data frame with only averaged "Reading", "Computing" and "Writing" categories

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be an pandas DataFrame"
        )
    else:
        df_r = df.iloc[:, 1:8]
        col_n = df_r.columns.str.split()
        col_r = [item[0] for item in col_n]
        df_r.columns = [col_r]
        df_r = df_r.groupby(level=0, axis=1).sum().mean()
        return df_r


def piechart_plot(df, path, ext):
    """
    Reads log data in pandas DataFrame format and creates piechart plot for 
    the averaged 3DPOD data at a given directory with a given extension

    Parameters
    ----------
    df      :   pandas.DataFrame    
        DataFrame containing log data - usually read from csv produced by reader
    path    :   string    
        Path for output plots
    ext     :   string
        Image extension to define the format ("png","pdf","svg"...)

    Returns
    -------
    Nothing

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame.
        If path is not a string
        If ext is not a string
    ValueError
        If ext is not a supported extension for an image format.
    FileNotFoundError
        If path does not exist.
    """

    df_r = reduce_df(df)

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = df_r.index
    sizes = df_r
    explode = (0.1, 0, 0)  # only "explode" the 2nd slice

    fig1, ax1 = plt.subplots()
    ax1.pie(
        sizes,
        explode=explode,
        labels=labels,
        autopct="%1.1f%%",
        shadow=True,
        startangle=90,
    )
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis("equal")
    plt.title("Average time distribution for 3DPOD of 200 snapshots")
    plt.savefig(os.path.join(path, "piechart." + ext), bbox_inches="tight")


if __name__ == "__main__":
    # WIP, kept here as comment for reference of usage
    """
    path = "tests/input/run_test/out_3/"
    name = "logs.csv"
    df = pd.read_csv(path + name)

    plt.style.use("seaborn-colorblind")

    extension = "pdf"
    path = "tests/input/run_test/fig_3/"
    error_plot(df, path, extension)
    piechart_plot(df, path, extension)
    """
