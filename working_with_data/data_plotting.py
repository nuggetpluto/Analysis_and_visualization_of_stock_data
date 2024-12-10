import os
import matplotlib.pyplot as plt


def create_and_save_plot(data, ticker, period, filename=None):
    plt.figure(figsize=(10, 6))

    # Построение графика
    dates = data.index.to_numpy()
    plt.plot(dates, data['Close'].values, label='Close Price')
    plt.plot(dates, data['Moving_Average'].values, label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    folder = "exported_data"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    plt.savefig(file_path)
    print(f"График сохранен как {file_path}")
