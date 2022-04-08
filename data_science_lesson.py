# # Скачивание файла (подставить свою ссылку)
# !wget -O "weather.xls.gz" "http://93.90.217.252/download/files.synop/27/27612.01.01.2016.18.10.2021.1.0.0.ru.utf8.00000000.xls.gz"
# # Распаковка архива
# !gzip -df "weather.xls.gz"
# !pip install --upgrade xlrd
# ДЗ:

# 1) Протестировать качество модели DecisionTreeRegressor + cos(день в году)

# 2) Поиграть с признаками - добавить больше признаков в модель (sin, sin & cos, dayofyear & cos и т.п.)


import matplotlib.pyplot as plt
import pandas as pd
# Подключаем библиотеку с математическими функциями
import numpy as np
# Считываем Excel-таблицу в переменную data, удаляем первые 6 строк комментарией
data = pd.read_excel('weather.xls', skiprows=6)
# Удаляем пропуски
data = data[data['T'].notna()]
# Преобразуем российский формат дат для дальнейшего анализа
data['date'] = pd.to_datetime(data['Местное время в Москве (ВДНХ)'], dayfirst=True)

# # Распечатаем первые 10 строк таблицы
# data.head(10)
# # Атрибут объекта - список колонок
# data.columns
# # Pandas DataFrame (наша data) - это таблицы, которые хранятся по столбцам, 
# # т.е. если мы хотим получить данные о температуре в строке 15, 
# # мы в квадратных скобках пишем сначала название колонки, потом номер строки
# print('Температура в строке 15 =', data['T'][15])
# data['T']
# # Гистограмма - график, который показывает, сколько раз встречалось то или иное значние
# data['T'].hist()

# Строим график с помощью функции из библиотеки matplotlib (загрузили ее с коротким именем plt)
plt.figure(figsize=(20, 5))
plt.plot(data['date'], data['T'], color='blue', label='Data')
plt.legend()

# Задание 1
# Приблизить график аномалии в 2017 году (например, обрезать с ноября 2016 по март 2017)

condition1 = data['date'] > '2016-10-01'
data_short1 = data[condition1]

condition2 = data_short1['date'] < '2017-03-01'
data_short2 = data_short1[condition2]

plt.figure(figsize=(20, 5))
plt.plot(data_short2['date'], data_short2['T'], color='blue', label='Data')
plt.legend()

# 2) вариант в одну строку
condition = (data['date'] < '2017-03-01') & (data['date'] > '2016-10-01')
data_short = data[condition]

plt.figure(figsize=(20, 5))
plt.plot(data_short['date'], data_short['T'], color='blue', label='Data')
plt.legend()

# 3) вариант в одну строку с помощью функции between
data_short = data[data['date'].between('2016-10-01', '2017-03-01')]

plt.figure(figsize=(20, 5))
plt.plot(data_short['date'], data_short['T'], color='blue', label='Data')
plt.legend()

# ****************************************************************************8
# Линейная регрессия (LinearRegression) Посмотрим на данные глазами, подумаем, на какую функцию похож график, автоматически инструментами ML подберем коэффициенты функции так, чтобы графики совпали.
# Дерево решений (DecisionTree) Построим альтернативную модель, которая строит ступенчатую функцию, и сравним численно, какая модель лучше годится для прогноза.
# Чтобы обучить модель (любую), нужно пройти 2 предварительные стадии:

# Сгенерировать новые признаки (если нужно)
# Разделить данные на 2 выборки (2 набора записей) - для обучения модели и для тестирования

# Сгенерируем новый признак: день в году
data['dayofyear'] = data['date'].dt.dayofyear

# Новый признак: косинус от дня в году.
# Период [1, 366] перегоним в период [0, 2*pi] (подгоняем косинусоиду по ширине)
# день в году в радианах = (dayofyear - 1) / 366 * 2*pi
# косинус от дня в году = cos(день в году в радианах из диапазона 0 до 2*pi)

data['cos_dayofyear'] = np.cos((data['dayofyear'] - 1 ) / 366 * 2 * np.pi)
plt.plot(data['cos_dayofyear'])
plt.plot(data['T'])

# data_train - обучающая выборка
# data_test - тестовая выборка

data_train = data[data['date'] < '2020-01-01']
data_test = data[data['date'] >= '2020-01-01']

plt.plot(data_train['date'], data_train['T'], color='blue')
plt.plot(data_test['date'], data_test['T'], color='gray')

# Для того, чтобы обучить модель, нужно еще раз разделить выборку 
# на фичи (признаки, features, X) и таргет (целевую переменную, которую прогнозируем, target, y)
# 2 датасета train-test х 2 features-target - создаем 4 переменных: 
# X_train, y_train, X_test, y_test
# 
# 
# Мы будем делать прогноз только на одном факторе - номере дня в году data['dayofyear']
# Но модель ожидает, что ей на вход придет двумерная таблица с многими факторами - 
# поэтому создаем из колонки date['T'] полноценную таблицу pandas DataFrame
X_train = pd.DataFrame()
X_train['cos_dayofyear'] = data_train['cos_dayofyear']

X_test = pd.DataFrame()
X_test['cos_dayofyear'] = data_test['cos_dayofyear']
# "y" оставляем столбцом, как есть
y_train = data_train['T']
y_test = data_test['T']

# 1 модель: Линейная регрессия (Linear Regression)
# Будем с ее помощью подгонять коэффициент при косинусе так, чтобы растянуть его в высоту до уровня наших данных

# z=acos(dayofyear) + b
from sklearn.linear_model import LinearRegression
# Создаем пустой объект со случайными a и b, которые пока не описывают наши данные
model = LinearRegression()
# Возвращаемся к подготовительному шагу - разделяем x (cos_dayofyear) и y (data['T'])
# Получаем 2 таблицы X_train, X_test и 2 столбца y_train, y_test
X_train = pd.DataFrame()
X_train['cos_dayofyear'] = data_train['cos_dayofyear']
X_test = pd.DataFrame()
X_test['cos_dayofyear'] = data_test['cos_dayofyear']

y_train = data_train['T']
y_test = data_test['T']

# Обучаем модель: подгоняем модель по данным X_train и говорим "правильные ответы" - y_train
model.fit(X_train, y_train)

# Посмотрим, какую мат. модель построила регрессия по данным, поэтому распечатаем 
# прогноз для тренировочных данных

# Прогноз на данных, которые модель еще не видела
pred_test = model.predict(X_test)

# Распечатаем графики
plt.plot(data_train['date'], data_train['T'], color='blue')
plt.plot(data_test['date'], data_test['T'], color='gray')
plt.plot(data_test['date'], pred_test, color='yellow')

# Проверяем качество численно

# mean_absolute_error - средняя сумма отклонений (меньше -> лучше)

from sklearn.metrics import mean_absolute_error

print('Средняя ошибка на тестовой выборке =', mean_absolute_error(y_test, pred_test))

# Собираем все шаги воедино

# Новый признак: косинус от дня в году
data['cos_dayofyear'] = np.cos((data['dayofyear'] - 1) / 366 * 2 * np.pi)

# Заново переразбиваем датасет на train-test, чтобы изменения применились
data_train = data[data['date'] < '2020-01-01']
data_test = data[data['date'] >= '2020-01-01']

# Из train-test формируем X_train, X_test
X_train = pd.DataFrame()
X_train['cos_dayofyear'] = data_train['cos_dayofyear']  # X
X_test = pd.DataFrame()
X_test['cos_dayofyear'] = data_test['cos_dayofyear']
# "y" оставляем прежним
y_train = data_train['T']
y_test = data_test['T']

# Создаем модель и обучаем ее
model = LinearRegression()
model.fit(X_train, y_train)

# Делаем прогноз
pred_train = model.predict(X_train)
pred_test = model.predict(X_test)

# Печатаем графики
plt.figure(figsize=(20, 5))
plt.scatter(data_train['date'], y_train, label='Data train')
plt.scatter(data_test['date'], y_test, label='Data test')
plt.scatter(data_train['date'], pred_train, label='Predict train')
plt.scatter(data_test['date'], pred_test, label='Predict test')
plt.legend()

# Смотрим на величину ошибки
print('Средняя ошибка на обучающей выборке =', mean_absolute_error(y_train, pred_train))
print('Средняя ошибка на тестовой выборке =', mean_absolute_error(y_test, pred_test))

# 1) LinearRegression + cos_dayofyear
# Средняя ошибка на обучающей выборке = 4.273310125395435
# Средняя ошибка на тестовой выборке = 4.578715441934872

# 2 Модель: Дерево решений (Decision Tree)
# http://www.r2d3.us/visual-intro-to-machine-learning-part-1/
from sklearn.tree import DecisionTreeRegressor

# 2) Decision Tree + dayofyear
data['dayofyear'] = data['date'].dt.dayofyear

data_train = data[data['date'] < '2020-01-01']
data_test = data[data['date'] >= '2020-01-01']

X_train = pd.DataFrame()
X_train['dayofyear'] = data_train['dayofyear']  # 1) Меняем название признака
X_test = pd.DataFrame()
X_test['dayofyear'] = data_test['dayofyear'] # 2) Меняем название признака

y_train = data_train['T']
y_test = data_test['T']


model = DecisionTreeRegressor()  # 3) Меняем модель
model.fit(X_train, y_train)


pred_train = model.predict(X_train)
pred_test = model.predict(X_test)


plt.figure(figsize=(20, 5))
plt.scatter(data_train['date'], y_train, label='Data train')
plt.scatter(data_test['date'], y_test, label='Data test')
plt.scatter(data_train['date'], pred_train, label='Predict train')
plt.scatter(data_test['date'], pred_test, label='Predict test')
plt.legend()


print('Средняя ошибка на обучающей выборке =', mean_absolute_error(y_train, pred_train))
print('Средняя ошибка на тестовой выборке =', mean_absolute_error(y_test, pred_test))

# 1) LinearRegression + cos_dayofyear
# Средняя ошибка на обучающей выборке = 4.273310125395435
# Средняя ошибка на тестовой выборке = 4.578715441934872

# 2) DecisionTreeRegressor + dayofyear
# Средняя ошибка на обучающей выборке = 3.6437873063246125
# Средняя ошибка на тестовой выборке = 4.647444490245206

# Документация библиотеки, где можно посмотреть параметры модели, которые можно настраивать: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html

# Модель 2.1 Decision Tree + dayofyear + настройка параметров
# 2.1) Decision Tree + dayofyear + настройка параметров

# model = DecisionTreeRegressor(max_depth=5)  # Заменяем модель

data['dayofyear'] = data['date'].dt.dayofyear


data_train = data[data['date'] < '2020-01-01']
data_test = data[data['date'] >= '2020-01-01']


X_train = pd.DataFrame()
X_train['dayofyear'] = data_train['dayofyear']  # 1) Меняем название признака
X_test = pd.DataFrame()
X_test['dayofyear'] = data_test['dayofyear'] # 2) Меняем название признака

y_train = data_train['T']
y_test = data_test['T']


model = DecisionTreeRegressor(max_depth=6)  # 3) Меняем модель + добавляем параметр
model.fit(X_train, y_train)


pred_train = model.predict(X_train)
pred_test = model.predict(X_test)


plt.figure(figsize=(20, 5))
plt.scatter(data_train['date'], y_train, label='Data train')
plt.scatter(data_test['date'], y_test, label='Data test')
plt.scatter(data_train['date'], pred_train, label='Predict train')
plt.scatter(data_test['date'], pred_test, label='Predict test')
plt.legend()


print('Средняя ошибка на обучающей выборке =', mean_absolute_error(y_train, pred_train))
print('Средняя ошибка на тестовой выборке =', mean_absolute_error(y_test, pred_test))

# 1) LinearRegression + cos_dayofyear
# Средняя ошибка на обучающей выборке = 4.273310125395435
# Средняя ошибка на тестовой выборке = 4.578715441934872 (2-е место в рейтинге)

# 2) DecisionTreeRegressor + dayofyear
# Средняя ошибка на обучающей выборке = 3.6437873063246125
# Средняя ошибка на тестовой выборке = 4.647444490245206 (самая неточная модель)

# 2.1) DecisionTreeRegressor + dayofyear + настройка параметров
# Средняя ошибка на обучающей выборке = 3.7469198089127693
# Средняя ошибка на тестовой выборке = 4.545731192829994 (самая точная модель)


# 3 LinearRegression + sin(dayofyear)
# 3) LinearRegression + sin(dayofyear)


data['dayofyear'] = data['date'].dt.dayofyear
data['sin_dayofyear'] = np.sin((data['dayofyear'] - 1) / 366 * 2 * np.pi)
data['cos_dayofyear'] = np.cos((data['dayofyear'] - 1) / 366 * 2 * np.pi)


data_train = data[data['date'] < '2020-01-01']
data_test = data[data['date'] >= '2020-01-01']


X_train = pd.DataFrame()
X_train['sin_dayofyear'] = data_train['sin_dayofyear']  # 1) Меняем название признака
X_test = pd.DataFrame()
X_test['sin_dayofyear'] = data_test['sin_dayofyear'] # 2) Меняем название признака

y_train = data_train['T']
y_test = data_test['T']


model = LinearRegression()  # 3) Меняем модель
model.fit(X_train, y_train)


pred_train = model.predict(X_train)
pred_test = model.predict(X_test)


plt.figure(figsize=(20, 5))
plt.scatter(data_train['date'], y_train, label='Data train')
plt.scatter(data_test['date'], y_test, label='Data test')
plt.scatter(data_train['date'], pred_train, label='Predict train')
plt.scatter(data_test['date'], pred_test, label='Predict test')
plt.legend()


print('Средняя ошибка на обучающей выборке =', mean_absolute_error(y_train, pred_train))
print('Средняя ошибка на тестовой выборке =', mean_absolute_error(y_test, pred_test))

# 1) LinearRegression + cos_dayofyear
# Средняя ошибка на обучающей выборке = 4.273310125395435
# Средняя ошибка на тестовой выборке = 4.578715441934872 (2-е место в рейтинге)

# 2) DecisionTreeRegressor + dayofyear
# Средняя ошибка на обучающей выборке = 3.6437873063246125
# Средняя ошибка на тестовой выборке = 4.647444490245206 (самая неточная модель)

# 2.1) DecisionTreeRegressor + dayofyear + настройка параметров
# Средняя ошибка на обучающей выборке = 3.7469198089127693
# Средняя ошибка на тестовой выборке = 4.545731192829994 (самая точная модель)

plt.plot(data['date'], data['sin_dayofyear'], label='sin')
plt.plot(data['date'], data['cos_dayofyear'], label='cos')
plt.legend()

plt.plot(data['date'], data['sin_dayofyear'], label='cos')

plt.plot(data['date'], data['T'])

plt.plot(data['date'], -data['cos_dayofyear'], label='cos')

plt.plot(data['date'], -data['cos_dayofyear'], label='cos')

plt.plot(data['date'], 0.5*data['sin_dayofyear'] + 2 * data['cos_dayofyear'], label='a*sin + b*cos')
plt.legend()


plt.plot(data['date'], 2*data['sin_dayofyear'] + 0.5 * data['cos_dayofyear'], label='a*sin + b*cos')
plt.legend()

# 3) LinearRegression + sin(dayofyear)


data['dayofyear'] = data['date'].dt.dayofyear
data['sin_dayofyear'] = np.sin((data['dayofyear'] - 1) / 366 * 2 * np.pi)
data['cos_dayofyear'] = np.cos((data['dayofyear'] - 1) / 366 * 2 * np.pi)


data_train = data[data['date'] < '2020-01-01']
data_test = data[data['date'] >= '2020-01-01']


X_train = pd.DataFrame()
X_train['sin_dayofyear'] = data_train['sin_dayofyear']  # 1) Меняем название признака
X_train['cos_dayofyear'] = data_train['cos_dayofyear']  # добавляем новый признак
X_test = pd.DataFrame()
X_test['sin_dayofyear'] = data_test['sin_dayofyear'] # 2) Меняем название признака
X_test['cos_dayofyear'] = data_test['cos_dayofyear']

y_train = data_train['T']
y_test = data_test['T']


model = LinearRegression()  # 3) Меняем модель
model.fit(X_train, y_train)


pred_train = model.predict(X_train)
pred_test = model.predict(X_test)


plt.figure(figsize=(20, 5))
plt.scatter(data_train['date'], y_train, label='Data train')
plt.scatter(data_test['date'], y_test, label='Data test')
plt.scatter(data_train['date'], pred_train, label='Predict train')
plt.scatter(data_test['date'], pred_test, label='Predict test')
plt.legend()


print('Средняя ошибка на обучающей выборке =', mean_absolute_error(y_train, pred_train))
print('Средняя ошибка на тестовой выборке =', mean_absolute_error(y_test, pred_test))

# 1) LinearRegression + cos_dayofyear
# Средняя ошибка на обучающей выборке = 4.273310125395435
# Средняя ошибка на тестовой выборке = 4.578715441934872 (2-е место в рейтинге)

# 2) DecisionTreeRegressor + dayofyear
# Средняя ошибка на обучающей выборке = 3.6437873063246125
# Средняя ошибка на тестовой выборке = 4.647444490245206 (самая неточная модель)

# 2.1) DecisionTreeRegressor + dayofyear + настройка параметров
# Средняя ошибка на обучающей выборке = 3.7469198089127693
# Средняя ошибка на тестовой выборке = 4.545731192829994 (самая точная модель)

# 3) 
# Средняя ошибка на обучающей выборке = 4.018986335674868
# Средняя ошибка на тестовой выборке = 4.269466206470706
