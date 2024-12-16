import os
import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, start=None, end=None, period=None):
    """
    Загружает данные акций с Yahoo Finance.
    :param ticker: Тикер акции
    :param start: Дата начала в формате 'YYYY-MM-DD'
    :param end: Дата окончания в формате 'YYYY-MM-DD'
    :param period: Предустановленный период (например, '1mo', '1d')
    :return: DataFrame с историческими данными
    """
    stock = yf.Ticker(ticker)

    if start and end:
        print(f"Загрузка данных для {ticker} с {start} по {end}...")
        data = stock.history(start=start, end=end)
    elif period:
        print(f"Загрузка данных для {ticker} за период {period}...")
        data = stock.history(period=period)
    else:
        print("Ошибка: необходимо указать либо период, либо даты начала и окончания.")
        return pd.DataFrame()

    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия за заданный период.
    :param data: DataFrame с колонкой 'Close'
    """
    if 'Close' in data.columns:
        average_price = data['Close'].mean()
        print(f"Средняя цена закрытия за период: {average_price:.2f}")
    else:
        print("Колонка 'Close' отсутствует в данных.")


def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет пользователя, если колебания цены превышают заданный порог.
    :param data: DataFrame с колонкой 'Close'
    :param threshold: Процент порога для колебаний
    """
    if 'Close' in data.columns:
        max_price = data['Close'].max()
        min_price = data['Close'].min()
        fluctuation = ((max_price - min_price) / min_price) * 100

        if fluctuation > threshold:
            print(f"Внимание! Колебания цены составляют {fluctuation:.2f}%, что превышает порог {threshold}%.")
        else:
            print(f"Колебания цены составляют {fluctuation:.2f}%, что ниже порога {threshold}%.")
    else:
        print("Колонка 'Close' отсутствует в данных.")


def export_data_to_csv(data, filename, user_inputs):
    """
    Экспортирует данные и параметры пользователя в CSV файл.
    :param data: DataFrame с данными акций
    :param filename: Имя файла для сохранения
    :param user_inputs: Словарь с запросами пользователя (например, тикер, период, порог)
    """
    if not filename.endswith('.csv'):
        filename += '.csv'

    # Папка для сохранения
    folder = "exported_data"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    # Добавляем параметры пользователя в файл
    metadata = pd.DataFrame([user_inputs])
    metadata.to_csv(file_path, index=False)

    # Сохраняем данные акций
    data.to_csv(file_path, mode='a', index=False)
    print(f"Данные и параметры пользователя успешно сохранены в файл {file_path}")


def calculate_rsi(data, window=14):
    """
    Рассчитывает RSI (индекс относительной силы) для данных акций.
    :param data: DataFrame с колонкой 'Close'
    :param window: Длина окна для расчёта RSI (по умолчанию 14)
    :return: DataFrame с добавленным столбцом 'RSI'
    """
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Рассчитывает MACD и сигнальную линию.
    :param data: DataFrame с колонкой 'Close'
    :param short_window: Период короткого скользящего среднего (по умолчанию 12)
    :param long_window: Период длинного скользящего среднего (по умолчанию 26)
    :param signal_window: Период сигнальной линии (по умолчанию 9)
    :return: DataFrame с добавленными столбцами 'MACD' и 'Signal_Line'
    """
    data['EMA12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data
