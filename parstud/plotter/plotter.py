import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_generic():
    plt.figure()
    for i in range(1, 8):
        plt.plot(df.stdout_file, df.iloc[:, i], label=df.columns[i])
    plt.ylabel("time [s]")
    plt.legend()
    plt.show()


def box_plot():
    np_list = list(set(df.iloc[:, -2]))

    for j in range(3):
        df_filt = df[df.iloc[:, -2] == np_list[j]]
        for i in range(1, 8):
            plt.subplot(3, 7, i + (j * 7))
            plt.boxplot(df_filt.iloc[:, i])
    plt.show()


def error_plot(df, path, ext):
    df_no_obj = df.iloc[:, 1:-1]  # Quantile method raises error for obj types
    mean = df_no_obj.groupby("Number of processors").mean()
    p025 = df_no_obj.groupby("Number of processors").quantile(0.025)
    p975 = df_no_obj.groupby("Number of processors").quantile(0.975)

    for i in range(0, 7):
        plt.figure()
        (_, caps, _) = plt.errorbar(
            mean.index,
            mean.iloc[:, i],
            yerr=[mean.iloc[:, i] - p025.iloc[:, i], p975.iloc[:, i] - mean.iloc[:, i]],
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
        plt.savefig(path + "errorbar_" + str(i) + "." + ext, bbox_inches="tight")


def reduce_df(df):
    df_r = df.iloc[:, 1:8]
    col_n = df_r.columns.str.split()
    col_r = [item[0] for item in col_n]
    df_r.columns = [col_r]
    df_r = df_r.groupby(level=0, axis=1).sum().mean()
    return df_r


def piechart_plot(df, path, ext):
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
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Average time distribution for 3DPOD of 200 snapshots")
    plt.savefig(path + "piechart." + ext, bbox_inches="tight")


if __name__ == "__main__":

    path = "tests/input/run_test/out_1/"
    name = "logs.csv"
    df = pd.read_csv(path + name)

    plt.style.use("seaborn-colorblind")

    extension = "pdf"
    path = "tests/input/run_test/fig/"
    error_plot(df, path, extension)
    piechart_plot(df, path, extension)

