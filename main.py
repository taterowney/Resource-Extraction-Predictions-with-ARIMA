import statsmodels.api as sm
import pandas as pd
from matplotlib import pyplot as plt


def int_to_word_scientific_notation(number):
    # Define the suffixes for each power of 10
    suffixes = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion']
    # Divide the number by powers of 10 and determine the appropriate suffix
    power = 0
    while number >= 1000:
        number /= 1000.0
        power += 1
    # Format the result with one decimal place and the determined suffix
    result = f"{number:.1f} {suffixes[power]}"
    return result


def plot_data(name, path, prefix="", start_date=1900):
    if prefix:
        prefix_bold = "$\\bf{" + prefix.replace("$", "") + "}$ "
    else:
        prefix_bold = ""
    with open(path, "r") as f:
        data = f.readlines()
        data = [float(d.strip().replace(",", "")) for d in data]

    data = pd.DataFrame(data)

    model = sm.tsa.arima.ARIMA(data, order=(13, 3, 3))
    results = model.fit()
    print(results.summary())
    print(f"Parameters: {results.params}")
    print("\n\n\n")
    print(f"AIC: {results.aic}")
    print("\n\n\n")
    print("Total mined (tons): " + str(int_to_word_scientific_notation(results.predict(2024-1900, 2058-1900).sum())))


    data.index = pd.to_datetime(data.index + start_date, format="%Y")
    plt.plot(data, color="black")

#    ax = plt.gca()
#    ax.set_xlim([1900, 2058])

    predicted_trend = results.predict(2021-start_date, 2058-start_date)
    predicted_trend.index = pd.to_datetime(predicted_trend.index + start_date, format="%Y")
    plt.plot(predicted_trend, color="blue", linestyle="dashed")
    plt.xlabel("Year")
    plt.ylabel(f"{name} mined ({prefix}metric tons)")
    plt.title(f"{name} Mined ({prefix_bold}metric tons) versus Time (years)", fontweight="bold")

    # add label showing yearly production in 2058
    production_2058 = int(predicted_trend.iloc[-1])
    #plt.annotate(f"Predicted production in 2058: {production_2058} tons", xy=(2058, production_2058), xytext=(2058, production_2058+1000), arrowprops=dict(facecolor='black', shrink=0.05))
    plt.text(0.05, 0.95, f"Predicted annual mining in 2058: {int_to_word_scientific_notation(production_2058)} metric tons", bbox=dict(facecolor='white', alpha=1), transform=plt.gca().transAxes)
    plt.plot(pd.to_datetime(2058, format="%Y"), production_2058, marker="*", color="blue", markersize=20, transform=plt.gca().transData)
    name = name.replace(" ", "")
    plt.savefig(f"plots/{name}.png")
    plt.show()


    print(results.predict(2030-start_date, 2030-start_date))


def plot_cobalt():
    plt.figure(figsize=(7.5, 5))
    with open("data_cobalt.txt", "r") as f:
        data = f.readlines()
        data = [float(d.strip().replace(",", "")) for d in data]

    data = pd.DataFrame(data)
    data.index = pd.to_datetime(data.index + 2010, format="%Y")

    future_projection = pd.DataFrame([190000 + 7360 * i for i in range(2058-2022)])
    future_projection.index = pd.to_datetime(future_projection.index + 2022, format="%Y")

    production_2058 = int(future_projection.iloc[-1])

#    plt.plot(pd.to_datetime(1900, format="%Y"), 0, color="white")

    plt.plot(data, color="black")
    plt.plot(future_projection, color="blue", linestyle="dashed")
    plt.xlabel("Year")
    plt.ylabel("Cobalt mined (metric tons)")
    plt.title("Cobalt Mined (metric tons) versus Time (years)", fontweight="bold")
    plt.text(0.05, 0.95,
             f"Predicted annual mining in 2058: {int_to_word_scientific_notation(production_2058)} metric tons",
             bbox=dict(facecolor='white', alpha=1), transform=plt.gca().transAxes)
    plt.plot(pd.to_datetime(2058, format="%Y"), production_2058+5000, marker="*", color="blue", markersize=20, transform=plt.gca().transData)
    plt.savefig("plots/Cobalt.png")
    plt.show()

def plot_gallium():
    plt.figure(figsize=(7.5, 5))
    with open("data_gallium.txt", "r") as f:
        data = f.readlines()
        data = [float(d.strip().replace(",", "")) for d in data]

    data = pd.DataFrame(data)
    data.index = pd.to_datetime(data.index + 2016, format="%Y")

    future_projection = pd.DataFrame([540 + 35.3 * i for i in range(2058 - 2022)])
    future_projection.index = pd.to_datetime(future_projection.index + 2022, format="%Y")

    production_2058 = int(future_projection.iloc[-1])

    #    plt.plot(pd.to_datetime(1900, format="%Y"), 0, color="white")

    plt.plot(data, color="black")
    plt.plot(future_projection, color="blue", linestyle="dashed")
    plt.xlabel("Year")
    plt.ylabel("Gallium produced (metric tons)")
    plt.title("Gallium Produced (metric tons) versus Time (years)", fontweight="bold")
    plt.text(0.05, 0.95,
             f"Predicted annual production in 2058: {round(production_2058)} metric tons",
             bbox=dict(facecolor='white', alpha=1), transform=plt.gca().transAxes)
    plt.plot(pd.to_datetime(2058, format="%Y"), production_2058, marker="*", color="blue", markersize=20,
             transform=plt.gca().transData)
    plt.savefig("plots/Gallium.png")
    plt.show()


plot_data("Rare Earth Elements", "data_REEs.txt", prefix="$10^6$ ")
plot_data("Platinum Group Elements", "data_PGEs.txt")
plot_data("Lithium", "data_lithium.txt", prefix="$10^7$ ")
plot_cobalt()
plot_gallium()