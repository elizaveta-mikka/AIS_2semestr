import sqlite3

def create_database():
    conn = sqlite3.connect('smart_home.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TimeOfDay (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT UNIQUE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PresenceOfPeople (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        presence TEXT UNIQUE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS LevelOfNaturalLight (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT UNIQUE
    )''')

    # Создание таблицы LightingRules для правил
    # time_of_day - время суток (Утро/День/Вечер/Ночь/Любое)
    # presence_of_people - присутствие людей
    # level_of_natural_light - уровень естественного освещения (Нет/Низкий/Средний/Высокий)
    # lighting_state - уровень освещенности (Нет/Минимальный/Средний/Максимальный)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS LightingRules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_of_day_id INTEGER,
        presence_of_people_id INTEGER,
        level_of_natural_light_id INTEGER,
        lighting_state TEXT CHECK(lighting_state IN ('Нулевое', 'Минимальное', 'Среднее', 'Максимальное')),
        FOREIGN KEY (time_of_day_id) REFERENCES TimeOfDay(id),
        FOREIGN KEY (presence_of_people_id) REFERENCES PresenceOfPeople(id),
        FOREIGN KEY (level_of_natural_light_id) REFERENCES LevelOfNaturalLight(id)
    )''')
    conn.commit()
    return conn, cursor

# Формирование правил
def insert_lighting_rules(cursor):
    rules_data = [

        ('Утро', 'Нет', 'Нет', 'Нулевое'),
        ('Утро', 'Нет', 'Низкий', 'Нулевое'),
        ('Утро', 'Нет', 'Средний', 'Нулевое'),
        ('Утро', 'Нет', 'Высокий', 'Нулевое'),
        ('Утро', 'Да', 'Нет', 'Максимальное'),
        ('Утро', 'Да', 'Низкий', 'Среднее'),
        ('Утро', 'Да', 'Средний', 'Минимальное'),
        ('Утро', 'Да', 'Высокий', 'Нулевое'),

        ('День', 'Нет', 'Низкий', 'Нулевое'),
        ('День', 'Нет', 'Средний', 'Нулевое'),
        ('День', 'Нет', 'Высокий', 'Нулевое'),
        ('День', 'Да', 'Низкий', 'Среднее'),
        ('День', 'Да', 'Средний', 'Минимальное'),
        ('День', 'Да', 'Высокий', 'Нулевое'),

        ('Вечер', 'Нет', 'Нет', 'Нулевое'),
        ('Вечер', 'Нет', 'Низкий', 'Нулевое'),
        ('Вечер', 'Нет', 'Средний', 'Нулевое'),
        ('Вечер', 'Да', 'Нет', 'Максимальное'),
        ('Вечер', 'Да', 'Низкий', 'Среднее'),
        ('Вечер', 'Да', 'Средний', 'Минимальное'),

        ('Ночь', 'Нет', 'Нет', 'Нулевое'),
        ('Ночь', 'Да', 'Нет', 'Среднее'),
    ]

    time_of_day_data = [('Утро',), ('День',), ('Вечер',), ('Ночь',)]
    cursor.executemany('INSERT OR IGNORE INTO TimeOfDay (time) VALUES (?)', time_of_day_data)

    # Данные для присутствия людей
    presence_of_people_data = [('Нет',), ('Да',)]
    cursor.executemany('INSERT OR IGNORE INTO PresenceOfPeople (presence) VALUES (?)', presence_of_people_data)

    # Данные для уровня естественного освещения
    level_of_natural_light_data = [('Нет',), ('Низкий',), ('Средний',), ('Высокий',)]
    cursor.executemany('INSERT OR IGNORE INTO LevelOfNaturalLight (level) VALUES (?)', level_of_natural_light_data)

    cursor.executemany(
        'INSERT INTO LightingRules (time_of_day_id, presence_of_people_id, level_of_natural_light_id, lighting_state) VALUES (?, ?, ?, ?)',
        rules_data)

def main():
    conn, cursor = create_database()
    insert_lighting_rules(cursor)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
