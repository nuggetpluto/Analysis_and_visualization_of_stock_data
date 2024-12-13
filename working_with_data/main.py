import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc),"
        " GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")

    print(
        "Общие периоды времени для данных о запасах включают:"
        " 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")
    threshold = float(input("Введите порог колебаний в процентах (например, 5 для 5%): "))
    export_filename = input("Введите имя файла для экспорта данных (без расширения): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Рассчитываем RSI и MACD
    stock_data = dd.calculate_rsi(stock_data)
    stock_data = dd.calculate_macd(stock_data)

    # Уведомление о сильных колебаниях
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Вывод средней цены
    dd.calculate_and_display_average_price(stock_data)

    # Добавляем скользящее среднее
    stock_data = dd.add_moving_average(stock_data)

    # Экспорт данных и параметров пользователя
    user_inputs = {
        "Ticker": ticker,
        "Period": period,
        "Threshold": threshold
    }
    dd.export_data_to_csv(stock_data, export_filename, user_inputs)

    # Построение и сохранение графика
    graph_filename = f"{ticker}_{period}_chart_with_indicators.png"
    dplt.create_and_save_plot(stock_data, ticker, period, filename=graph_filename)


if __name__ == "__main__":
    main()
