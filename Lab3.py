import sqlite3
import random

# Фаззификация
def fuzzify_conditions(hour, n_people, natural_light):
    # Определение времени суток
    time_of_day = ''
    level_of_natural_light = ''
    if 6 <= hour < 12:
        time_of_day = 'Утро'
    elif 12 <= hour < 17:
        time_of_day = 'День'
    elif 17 <= hour < 22:
        time_of_day = 'Вечер'
    else:
        time_of_day = 'Ночь'
    # Присутствие людей
    presence_of_people = 'Да' if n_people != 0 else 'Нет'
    # Уровень естественного освещения
    if natural_light <= 10:
        level_of_natural_light = 'Нет'
    elif 10 < natural_light <= 30:
        level_of_natural_light = 'Низкий'
    elif 30 < natural_light <= 70:
        level_of_natural_light = 'Средний'
    elif 70 < natural_light <= 100:
        level_of_natural_light = 'Высокий'

    return time_of_day, presence_of_people, level_of_natural_light

# Получение действий по правилам
def get_lighting_action(time_of_day, presence_condition, natural_light_level_condition):
    conn = sqlite3.connect('smart_home.db')
    cursor = conn.cursor()
    query = '''
    SELECT lighting_state FROM LightingRules 
    WHERE time_of_day_id = ? AND presence_of_people_id = ? AND level_of_natural_light_id = ?
    '''
    cursor.execute(query, (time_of_day, presence_condition, natural_light_level_condition))
    result = cursor.fetchone()
    conn.close()

    # Проверка возращаемого значения
    if result is not None:
        return result[0]
    else:
        return None


# Симуляция
def simulate_lighting():

    hour = random.randint(0, 23)  # Случайный час
    n_people = random.randint(0, 10)  # Количество человек
    natural_light = 0

    if 6 <= hour < 12:  # Утреннее естественное освещение
        natural_light = random.randint(0, 90)
    elif 12 <= hour < 17:  # Дневное естественное освещение
        natural_light = random.randint(20, 100)
    elif 17 <= hour < 22:  # Вечернее естественное освещение
        natural_light = random.randint(0, 70)
    else:  # Ночное естественное освещение
        natural_light = random.randint(0, 10)

    print(f'Время - {hour}\nКоличество людей - {n_people}\nУровень естественного освещения - {natural_light}')

    # Фаззификация
    time_of_day, presence_condition, natural_light_level_condition = fuzzify_conditions(hour, n_people, natural_light)

    lighting_action = get_lighting_action(time_of_day, presence_condition, natural_light_level_condition)

    if lighting_action is not None:
        print(f"Действие по управлению освещением: {lighting_action} освещение.")
    else:
        print("Нет данных для управления освещением.")


# Основная программа
if __name__ == "__main__":
    num_simulations = 10
    for i in range(num_simulations):
        print(f'СЦЕНАРИЙ {i + 1}')
        simulate_lighting()
