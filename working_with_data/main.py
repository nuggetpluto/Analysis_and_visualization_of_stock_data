import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент анализа биржевых данных с улучшенными индикаторами.")
    print(
        "Примеры тикеров: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    print("Выберите способ задания временного периода:")
    print("1. Предустановленный период (например, '1mo', '6mo', '1y')")
    print("2. Конкретные даты начала и окончания (формат: YYYY-MM-DD)")
    choice = input("Ваш выбор (1 или 2): ")

    if choice == '1':
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        start, end = None, None
    elif choice == '2':
        start = input("Введите дату начала (в формате YYYY-MM-DD): ")
        end = input("Введите дату окончания (в формате YYYY-MM-DD): ")
        period = None
    else:
        print("Неверный выбор. Попробуйте снова.")
        return

    threshold = float(input("Введите порог колебаний в процентах (например, 5 для 5%): "))
    export_filename = input("Введите имя файла для экспорта данных (без расширения): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, start=start, end=end, period=period)

    if stock_data.empty:
        print("Ошибка: Данные не были загружены.")
        return

    # Рассчитываем RSI и MACD
    stock_data = dd.calculate_rsi(stock_data)  # Добавляем расчёт RSI
    stock_data = dd.calculate_macd(stock_data)  # Добавляем расчёт MACD

    # Уведомление о сильных колебаниях
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Вывод средней цены
    dd.calculate_and_display_average_price(stock_data)

    # Добавляем скользящее среднее
    stock_data = dd.add_moving_average(stock_data)

    # Экспорт данных и параметров пользователя
    user_inputs = {
        "Ticker": ticker,
        "Start": start,
        "End": end,
        "Period": period,
        "Threshold": threshold
    }
    dd.export_data_to_csv(stock_data, export_filename, user_inputs)

    # Построение и сохранение графика
    graph_filename = f"{ticker}_chart.png"
    dplt.create_and_save_plot(stock_data, ticker, period if period else f"{start}_to_{end}", filename=graph_filename)


if __name__ == "__main__":
    main()
