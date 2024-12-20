import numpy as np
import matplotlib.pyplot as plt

# Определение трапециевидной функции принадлежности
def trapezoidal_mf(x, a, b, c, d):

    #:param x: Точки, для которых вычисляется функция принадлежности.
    #:param a: Левая граница начала возрастания функции.
    #:param b: Левая верхняя граница (где функция равна 1).
    #:param c: Правая верхняя граница (где функция равна 1).
    #:param d: Правая граница окончания убывания функции.
    #:return: Значение функции принадлежности в точках x.

    if x < a: # Точки вне функции
        return 0
    elif x >= a and x < b: # Точки - функция возрастает
        return (x - a) / (b - a)
    elif x >= b and x < c: # Точки - функция стабильна
        return 1
    elif x >= c and x <= d: # Точки - функция убывает
        if c == d: # Функция оканчивается в точке d
            return 1
        else:
            return (d - x) / (d - c) # Точки - функция убывает
    else:
        return 0


# Нечеткое множество для кредитного рейтинга
credit_rating = {
    'Низкий': (1, 1, 100, 200),
    'Средний': (200, 400, 600, 700),
    'Высокий': (700, 800, 900, 950),
    'Премиальный': (950, 980, 999, 999)
}

# Нечеткое множество для уровня риска
risk_level = {
    'Опасный': (1, 1, 100, 150),
    'Рискованный': (140, 400, 590, 600),
    'Приемлемый': (590, 800, 900, 905),
    'Безопасный': (890, 950, 999, 999)
}


while True:
    try:
        credit_score = float(input("Введите кредитный рейтинг (число от 1 до 999): "))
        if 1 <= credit_score <= 999:
            break
        else:
            print("Кредитный рейтинг должен быть в диапазоне от 1 до 999.")
    except ValueError:
        print("Некорректный ввод. Пожалуйста, введите число.")


# Трапециевидные функции для кредитного рейтинга
membership_degrees_credit = {}
for rating, params in credit_rating.items():
    membership_degrees_credit[rating] = trapezoidal_mf(credit_score, *params) 

print("\nСтепень принадлежности к нечетким множествам кредитного рейтинга:")
for rating, degree in membership_degrees_credit.items():
    print(f" {rating}: {degree:.2f}")

# Трапециевидные функции для уровня риска
membership_degrees_risk = {}
for level, params in risk_level.items():
    membership_degrees_risk[level] = trapezoidal_mf(credit_score, *params)

print("\nСтепень принадлежности к нечетким множествам уровня риска:")
for level, degree in membership_degrees_risk.items():
    print(f" {level}: {degree:.2f}")

x = np.linspace(1, 999, 500)

# График - Нечеткие множества кредитного рейтинга
plt.figure(figsize=(15, 4))
for rating, params in credit_rating.items():
    y = [trapezoidal_mf(val, *params) for val in x]
    plt.plot(x, y, label=rating)
plt.plot([credit_score, credit_score], [0, max(membership_degrees_credit.values())], 'k--', label='Заданный кредит рейтинг')
plt.xlabel("Кредитный рейтинг")
plt.ylabel("Степень принадлежности")
plt.title("Нечеткие множества кредитного рейтинга")
plt.legend(bbox_to_anchor=(1, 1))
plt.grid(True)
plt.show()



# График - Нечеткие множества уровня риска
plt.figure(figsize=(15, 4))
for level, params in risk_level.items():
    y = [trapezoidal_mf(val, *params) for val in x]
    plt.plot(x, y, label=level)
plt.plot([credit_score, credit_score], [0, max(membership_degrees_risk.values())], 'k--', label='Заданный кредит рейтинг')
plt.xlabel("Уровень риска")
plt.ylabel("Степень принадлежности")
plt.title("Нечеткие множества уровня риска")
plt.legend(bbox_to_anchor=(1, 1))
plt.grid(True)
plt.show()

