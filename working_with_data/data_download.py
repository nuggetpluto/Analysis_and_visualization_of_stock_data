import os
import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
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
