from deap import base, algorithms
from deap import creator
from deap import tools
import itertools

import random
import matplotlib.pyplot as plt
import numpy as np

# Константы задачи
n = 8 # Количество пунктов производства продуктов
k = 8 # Количество городов, нуждающихся в продуктах
np.random.seed(56)
x = [np.random.randint(100, 400) for _ in range(k)] # Количество продуктов, необходимые каждому городу
y = [np.random.randint(200, 500) for _ in range(n)] # Количество продукты, которые может произвести каждый пункт

# Константы генетического алгоритма
population_size = 300 # Размер популяции
p_crossover = 0.9 # Вероятность скрещивания
p_mutation = 0.1 # Вероятность мутации
max_generations = 50 # Максимальное количество поколений

transport_costs = np.random.randint(10, 500, size=(n, k)) # Транспортные расходы из пунктов в города

creator.create("FitnessMin", base.Fitness, weights=(-3.0, -2.0, -1.0)) # Создание класса FitnessMin для функции приспособленности (минимизация).
# Приоритет мнинимизации (в порядке убывания): недостаток продуктов, дорожные расходы, излишок продуктов.
creator.create("Individual", list, fitness=creator.FitnessMin) # Создание класса Individual.
toolbox = base.Toolbox() # Контейнер для функций, использующихся в генетическом алгоритме
toolbox.register("randomOrder", random.sample, range(n), n) # Хромосома длиной n, состоящая из неповторяющихся элементов от 0 до n
toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomOrder) # Создание особи
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator) # Создание популяции
population = toolbox.populationCreator(n=population_size)
hof = tools.HallOfFame(1) # Отбор лучшей особи


def Function_Fitness(individual): # Функция приспособленности
    cur_transport_costs = 0 # Транспортные раходы
    lack = 0 # Недостаток продуктов
    excess = 0 # Избыток продуктов
    cur_y = y.copy()
    for city, point in enumerate(individual):
        if city < k:
            cur_transport_costs += transport_costs[point][city]
            if cur_y[point] - x[city] > 0:
                excess += cur_y[point] - x[city]
                cur_y[point] = 0
            elif cur_y[point] - x[city] < 0:
                lack += cur_y[point] - x[city]
    lack *= -1
    return lack, cur_transport_costs, excess

def Inversion_mutation(individual): # Мутация инверсией
    idx1, idx2 = sorted(random.sample(range(len(individual)), 2)) # Выбор двух индексов (границы подсписка)
    individual[idx1:idx2] = reversed(individual[idx1:idx2]) # Инверсия подсписка
    return individual,


# Функции для полного перебора
def Calculate_transport_costs(route):
    cur_transport_costs = 0
    for city, point in enumerate(route):
        if city < k:
            cur_transport_costs += transport_costs[point][city]
    return cur_transport_costs


def Capacity_points(route):
    capacity = y.copy() # Объём продуктов, которым располагают пункты
    for city, point in enumerate(route):
        if capacity[point] < x[city]: # Недостаток продуктов
            return False # Имеется недостаток продуктов
        capacity[point] -= x[city]
    return True


# Генетический алгоритм
print("Генетический алгоритм")
toolbox.register("evaluate", Function_Fitness) # Подключение функции приспособленности
toolbox.register("select", tools.selTournament, tournsize=3) # Селекция по средствам турнирного отбора
# Скрещивание
#toolbox.register("mate", tools.cxOrdered) # Упорядоченное срещивание
#toolbox.register("mate", tools.cxPartialyMatched) # Частичное совпадающее скрещивание (подсписок)
toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0.5) # Частичное совпадающее скрещивание (вероятность)
# Мутация
#toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0) # Мутация перетасовкой
#toolbox.register("mutate", tools.mutFlipBit, indpb=1.0) # Мутация инвертированием битов
toolbox.register("mutate", Inversion_mutation) # Мутация инверсией

stats = tools.Statistics(lambda ind: (ind.fitness.values[0]*-3.0) + (ind.fitness.values[1]*-2.0) + (ind.fitness.values[2]*-1.0))
stats.register("max", np.max)
stats.register("avg", np.mean)
# Запуск генетического алгоритма
population, logbook = algorithms.eaSimple(population, toolbox,
                                        cxpb=p_crossover,
                                        mutpb=p_mutation,
                                        ngen=max_generations,
                                        halloffame=hof,
                                        stats=stats,
                                        verbose=True) # Вывод информации

# Алгоритм полного перебора
best_route = None
min_costs = float('inf') # Положитльеная бесконечность
min_excess = 0
for route in itertools.permutations(range(n), k): # Генерация всех возможных путей
    # (один элемент - встречается один раз)
    if Capacity_points(route): # Хватает ли продуктов всем городам
        cur_transport_costs = Calculate_transport_costs(route)
        if cur_transport_costs < min_costs:
            min_costs = cur_transport_costs
            best_route = route

# Вывод результата
# Генетический алгоритм
if best_route is not None:
    best_individual = hof.items[0]
    print("Генетический алгоритм")
    print(f"Оптимальный маршрут - {best_individual[:k]}")
    lack, tr_costs, excess = Function_Fitness(best_individual)
    print(f"Значение функции приспособленности - {np.dot(best_individual.fitness.values, (-3.0, -2.0, -1.0))}")
    print("Недостатка продуктов нет") if lack == 0 else print("Есть недостаток продуктов")
    print(f"Транспротные расходы - {tr_costs}")
    print(f"Суммарный избыток продуктов - {excess}")

    print("Полный перебор")
    print(f"Оптимальный маршрут - {list(best_route)}")
    lack, tr_costs, excess = Function_Fitness(best_route)
    print("Недостатка продуктов нет") if lack == 0 else print("Есть недостаток продуктов")
    print(f"Транспротные расходы - {tr_costs}")
    print(f"Суммарный избыток продуктов - {excess}")

    # Графиики
    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Поколение')
    plt.ylabel('Макс/средняя приспособленность')
    plt.title('Зависимость максимальной и средней приспособленности от поколения')
    plt.show()
else:
    print("Количество пунктов меньше, чем количество городов")