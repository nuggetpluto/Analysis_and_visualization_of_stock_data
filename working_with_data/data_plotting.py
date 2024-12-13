import os
import matplotlib.pyplot as plt


def create_and_save_plot(data, ticker, period, filename=None):
    plt.figure(figsize=(12, 8))

    # График цен
    plt.subplot(3, 1, 1)
    dates = data.index.to_numpy()
    plt.plot(dates, data['Close'], label='Close Price')
    plt.plot(dates, data['Moving_Average'], label='Moving Average')
    plt.title(f"{ticker} Цена акций")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # График RSI
    if 'RSI' in data.columns:
        plt.subplot(3, 1, 2)
        plt.plot(dates, data['RSI'], label='RSI', color='orange')
        plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
        plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
        plt.title("Индекс относительной силы (RSI)")
        plt.xlabel("Дата")
        plt.ylabel("RSI")
        plt.legend()

    # График MACD
    if 'MACD' in data.columns and 'Signal_Line' in data.columns:
        plt.subplot(3, 1, 3)
        plt.plot(dates, data['MACD'], label='MACD', color='blue')
        plt.plot(dates, data['Signal_Line'], label='Signal Line', color='red')
        plt.title("MACD и сигнальная линия")
        plt.xlabel("Дата")
        plt.ylabel("MACD")
        plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_chart_with_indicators.png"

    folder = "exported_data"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    plt.tight_layout()
    plt.savefig(file_path)
    print(f"График сохранен как {file_path}")
