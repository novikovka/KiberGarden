from aiogram import F, Router, types
from aiogram.types import BufferedInputFile
from datetime import datetime
from collections import defaultdict
import io
import matplotlib.pyplot as plt
from database import get_token_by_telegram_id, get_sensor_data

router = Router()


def average_per_hour(times, values):
    """
    Усреднение значений по часам
    times: список datetime
    values: список чисел
    Возвращает два списка: часы (0-23) и средние значения
    """
    temp_dict = defaultdict(list)
    for t, v in zip(times, values):
        temp_dict[t.hour].append(v)

    hours = sorted(temp_dict.keys())
    avg_values = [sum(temp_dict[h]) / len(temp_dict[h]) for h in hours]
    return hours, avg_values


def create_24h_plot_from_current_hour(times, values, title, ylabel):
    hours, avg_values = average_per_hour(times, values)

    now = datetime.now()
    current_hour = now.hour

    # формируем списки для 24 часов начиная с current_hour
    sorted_hours = [(current_hour + i) % 24 for i in range(24)]
    sorted_values = [avg_values[hours.index(h)] if h in hours else None for h in sorted_hours]

    plt.figure(figsize=(10, 5))
    plt.plot(range(24), sorted_values, marker='o')
    plt.title(title)
    plt.xlabel('Время (часы)')
    plt.ylabel(ylabel)
    plt.grid(True)

    # Подписи оси X с текущего часа
    plt.xticks(range(24), [f"{h}" for h in sorted_hours])

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf


@router.message(F.text.lower() == "графики")
async def send_graphs(message: types.Message):
    token = await get_token_by_telegram_id(message.from_user.id)
    if not token:
        await message.answer("Теплица для вашего аккаунта не найдена.")
        return

    types_sensors = {
        "Влажность воздуха": "HUMIDITY_AIR",
        "Влажность почвы": "HUMIDITY_SOIL",
        "Температура": "TEMPERATURE"
    }

    ylabel_mapping = {
        "HUMIDITY_AIR": "Значения влажности воздуха, %",
        "HUMIDITY_SOIL": "Значения влажности почвы, %",
        "TEMPERATURE": "Значения температуры, °C"
    }

    for title, sensor_type in types_sensors.items():
        times, values = await get_sensor_data(token, sensor_type)
        if not times:
            await message.answer(f"Нет данных для {title}")
            continue

        buf = create_24h_plot_from_current_hour(
            times, values,
            title=title,
            ylabel=ylabel_mapping[sensor_type]
        )
        buf.seek(0)
        photo_bytes = buf.read()
        photo_file = BufferedInputFile(photo_bytes, filename=f"{sensor_type}.png")

        await message.answer_photo(photo=photo_file, caption=title)
