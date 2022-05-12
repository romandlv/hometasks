# + + + библиотеки
import re
import requests as rq
from bs4 import BeautifulSoup as bs
import time
import subprocess
# + + + функции
def kolvo_zn_p_zpt(num, zn=0):
    return f"{num:.{zn}f}"  # превращает число в строку, быть осторожным лучше заменить на округление
    # а это оставить для печатной формы, чтобы .0 превращать в .00

def proverka_vvoda(chek_prav_option, text): # проверяет правильно ли ввел ответ пользователь
    print("Результат поиска верный? (Введите + или - в ответ)")
    while True:
        rezult = input("Ваш выбор: ")
        if rezult == "+":
            print("Замечательно, продолжим.")
            chek_prav_option = True
            break
        elif rezult == "-":
            print(f"Хм.. тогда прошу вас проверить {text}, и я попробую поискать еще раз.")
            break
        else:
            print("А что вы ввели? Попробуйте еще раз... ")
            continue
    return chek_prav_option

def str_to_num_transform(x): # занимается преобразованием строк в флоат с коррекцией точек и запятых при вводе пользователем разных типов
    num_transform = x
    num_transform_list = num_transform.split()
    y = len(num_transform_list)
    i = 1
    while i != y:
        num_transform_list[0] = num_transform_list[0] + num_transform_list[i]
        i += 1
    if "," in num_transform_list[0]:
        x = float(num_transform_list[0].replace(',', '.'))
    else:
        x = float(num_transform_list[0])
    return x

def list_iterator(lst, n): # эта функция берет список подготовленный для деления по шесть элементов для того, чтобы создать
        return [lst[i:i + n] for i in range(0, len(lst), n)] # новый список где каждый элемент это спискок из 6 элементов первоначального списка

# + + + переменные
internet = False
rejim_vibran = False
rejim_on_line = False
chek_prav_option1 = False
chek_prav_option2 = False
antidemp_koef = 0.25
specifikaciya = []
telef_org = None
okopfus = "Конфиденциальные данные"
ogrnip_org = None
kpp_org = None
ogrn_org = None
# + + + параметры
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.72"
}
# + + + + + + + + + + + Начало программы + + + + + + + + + + +
intro = """+ ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++gen+1+++version+013++++++ +
+                                                                                                           +
+                                   Module for Automatic Intelligence -                                     +
+                                           помощник по заполнению контрактов                               +
+                                                                                                           +
+ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++by+SQR++++++ +"""
# + + +
new_str = " "
print(intro)
print("Приветствую! ")
time.sleep(1)
print(new_str)
print("Я помогу вам заполнить контракт. Пожалуйста, следуйте дальнейшим инструкциям.")
time.sleep(1)
print("Но перед этим я проверю интернет соединение, пожалуйста, подождите...")

while rejim_vibran != True:
    print(new_str)
    try:
        subprocess.check_call(["ping", "77.88.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("Сетевое подключение работает. Продолжить в режиме онлайн или перейти к оффлайн режиму? ")
        internet = True
    except subprocess.CalledProcessError:
        print("Кажется, ваш компьютер не подключен к интернету. Проверить еще раз или перейти к оффлайн версии?")

    time.sleep(1)
    if internet == True:
        print("""Введите

    + ...................если хотите продолжить,
    - ............если хотите перейти в оффлайн
    """)
    else:
        print("""Введите

    + ..........если хотите проверить соединение,
    - .............если хотите перейти в оффлайн
    """)

    vibor_rejima = input("Ваш выбор:")
    if vibor_rejima == "-":
        rejim_on_line = False
        rejim_vibran = True
    elif vibor_rejima == "+":
        if internet == True:
            rejim_on_line = True
            rejim_vibran = True

if rejim_on_line == True:
    print("Онлайн режим активирован. ")
else:
    print("Оффлайн режим активирован. ")

print(new_str)
print("Итак, приступим.")
time.sleep(1)
print("Первое, что мне понадобится, это номер. ")

if rejim_on_line == True: # Пользователь выбрал парсить данные из интернета, а не вводить лично - 1я глобал опция ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    while chek_prav_option1 != True:
        nomer_zakup = input("Введите его здесь: ")
        url = f'Конфиденциальные данные={nomer_zakup}'
        r = rq.get(url, timeout=10, headers=headers)
        html = bs(r.content, "html.parser")
        object_zakup = html.find(text=re.compile("объект")).next_element.next_element.text.strip()
        print("Найдена закупка: " + object_zakup)
        chek_prav_option1 = proverka_vvoda(chek_prav_option1, "номер закупки")

    # Запросы к страничке карточки электронного аукциона после одобрения варианта

    # object_zakup = object_zakup
    ikz = html.find(text=re.compile("ИКЗ")).text.strip()
    smp_preimuzhj = html.find("span", text=re.compile("ч. 3 ст. 30 Закона"))
    cena_maksimal = html.find("span", text=re.compile("аксимальная")).next_element.next_element.next_element.text.strip()
    obespech_proc = html.find("span", text=re.compile("азмер обеспечения исполнения")).next_element.next_element.next_element.text.strip()
    obespech_proc = int(obespech_proc.replace(" ", "").replace("%", "").strip())
    kbk = html.find("div", id=re.compile("budgetTableInnerHtml")).find("table", class_="blockInfo__table tableBlock").find("td", class_="table__row-item normal-text tableBlock__col_left").get_text().strip()


    # После чего переход к страничке результатов торгов и запросы к ней

    url_sub = f'Конфиденциальные данные={nomer_zakup}'
    r_sub = rq.get(url_sub, timeout=10, headers=headers)
    html_sub = bs(r_sub.content, "html.parser")
    data_results = html_sub.find(text=re.compile("Дата")).next_element.next_element.text.strip()
    data_results_list = data_results.split()

    if html_sub.find(text=re.compile("обедитель")) != None:
        ck_predv = html_sub.find(text=re.compile("обедитель")).next_element.next_element.text.strip()
    else:
        ck_predv = html_sub.find("div", id=re.compile("supplier-def-result-participant-table")) \
            .find("table", class_="blockInfo__table tableBlock").find("tbody").find("td") \
            .next_element.next_element.next_element.next_element.next_element.next_element.text.strip()

    print("""Теперь, пожалуйста, введите ИНН контрагента, например: > 7725403923 <,
т.к. я не могу получить данные защищенные ЭЦП изнутри сайта РТС.
Пока...
    """)

    while chek_prav_option2 != True:
        inn_org = input("Ожидаю ввод тут: ")
        url_inn = f'Конфиденциальные данные={inn_org}'
        r_inn = rq.get(url_inn, timeout=10, headers=headers)
        html_inn = bs(r_inn.content, "html.parser")
        data_results_inn = html_inn.find("a", text=re.compile("№")).text.strip()
        data_results_inn = data_results_inn.split(" ")
        url_inn_respond = f'Конфиденциальные данные={data_results_inn[1]}'
        r_inn_respond = rq.get(url_inn_respond, timeout=10, headers=headers)
        html_inn_respond = bs(r_inn_respond.content, "html.parser")
        imya_org = html_inn_respond.find(text=re.compile("Участник закупки")).get_text().strip().lower().title()
        print("Найден контрагент: " + imya_org)
        chek_prav_option2 = proverka_vvoda(chek_prav_option2, "ИНН участника")

    # Запросы к страничке организации после одобрения варианта

    ip_ooo = html_inn_respond.find(text=re.compile("Тип участника закупки")).next_element.next_element.get_text().strip() # переписать условие на поиск ООО в тексте
    if "ридическ" in ip_ooo:
        UR_lic = True
        sokr_imya_org = html_inn_respond.find(text=re.compile("окращенное наименование")).next_element.next_element.get_text().strip()
        inn_org = html_inn_respond.find(text=re.compile("ИНН")).next_element.next_element.get_text().strip()
        kpp_org = html_inn_respond.find(text=re.compile("КПП")).next_element.next_element.get_text().strip()
        ogrn_org = html_inn_respond.find(text=re.compile("ОГРН")).next_element.next_element.get_text().strip()
        smp_prover = html_inn_respond.find(text=re.compile("частник закупки является субъектом")).next_element.next_element.next_element.get_text().strip()
        ur_adres_org = html_inn_respond.find(text=re.compile("места нахождения")).next_element.next_element.get_text().strip()
        ur_adres_org = ur_adres_org.lower().title()
        fio_gendir = html_inn_respond.find("tbody", class_="tableBlock__body").find("td", class_="tableBlock__col").text
        fio_gendir = fio_gendir.lower().title()
        doljn_gendir = html_inn_respond.find("tbody", class_="tableBlock__body").find("td", class_="tableBlock__col").next_element.next_element.next_element.text
        doljn_gendir = doljn_gendir.lower().title()
        pcht_adres_org = html_inn_respond.find(text=re.compile("очтовый адрес")).next_element.next_element.get_text().strip()
        pcht_adres_org= pcht_adres_org.lower().title()
        email_org = html_inn_respond.find(text=re.compile("дрес электронной почты")).next_element.next_element.get_text().strip()
        telef_org = html_inn_respond.find(text=re.compile("онтактный телефон")).next_element.next_element.get_text().strip()
    elif "ндивидуальный" in ip_ooo:
        UR_lic = False
        fio_gendir = imya_org.lower().title()
        sokr_imya_org = "ИП " + fio_gendir
        imya_org = "Индивидуальный предприниматель " + fio_gendir
        inn_org = html_inn_respond.find(text=re.compile("ИНН")).next_element.next_element.get_text().strip()  # ??
        ogrnip_org = html_inn_respond.find(text=re.compile("ОГРНИП")).next_element.next_element.get_text().strip()
        ogrnip_org_data = html_inn_respond.find(text=re.compile("ата регистрации индивидуального предпринимателя")).next_element.next_element.get_text().strip()
        email_org = html_inn_respond.find(text=re.compile("дрес электронной почты")).next_element.next_element.get_text().strip()
        try:
            smp_prover = html_inn_respond.find(text=re.compile("частник закупки является субъектом")).next_element.next_element.next_element.get_text().strip()
        except:
            smp_prover = False
    else:
        print("Искомый контрагент, скорее всего, физическое лицо или присутствует ошибка в алгоритме поиска даннных.")
        time.sleep(1)
        print("Пожалуйста закройте программу и выберите режим оффлайн для ручного заполнения реквизитов.")

    url_pechat_form = f'Конфиденциальные данные={nomer_zakup}'
    r_pechat_form = rq.get(url_pechat_form, timeout=10, headers=headers)
    html_pechat_form = bs(r_pechat_form.content, "html.parser")
    tablitca_cen = html_pechat_form.find("table", class_="table font9").find_all('td', style=None)

    for i in tablitca_cen:  # добавить из всех строк и столбцов таблицы данные о товарах услугах или работах и их ценах в список
        info = i.text.strip()
        if info != "":
            specifikaciya.append(info)

    for i in specifikaciya:  # цикл для того чтобы поубирать пробелы из цифр в другой кодировке
        if "\xa0" in i:
            specifikaciya[specifikaciya.index(i)] = specifikaciya[specifikaciya.index(i)].replace('\xa0', '')

    spisok_cen_objecta_zakup = list_iterator(specifikaciya, 6)  # полученный список преобразован в список из списков по 6 элементов, которые являют собой данные об одной позиции

# КОНЕЦ 1ой ГЛОБАЛЬНОЙ ОПЦИИ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
else:  # Пользователь выбрал вводить данные лично, а не парсить из интернета - 2я глобал опция ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    print("В разработке.")
# КОНЕЦ 2ой ГЛОБАЛЬНОЙ ОПЦИИ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Сбор доп инфы

print("Итак, основная информация собрана. ")
time.sleep(1)
print("Теперь - давайте пройдемся по нюансам заключения и доп. сведениям.")
print(new_str)
time.sleep(1)
print("Начнем с подписантов:")
time.sleep(1)
print(new_str)
podpisant1 = "Конфиденциальные данные"
print(f"""Формулировка:
>>> {podpisant1} <<<
    является верной на текущий момент?
""")
podpisant1_chek = input("+/-: ")  # обработчик исключений на ввод + ввод для корректировки цикл
if podpisant1_chek == "+":
    print("Отлично, теперь касательно второго подписанта.")
else:
    print("Что-то изменилось? Тогда введите, пожалуйста, корректную информацию.")
    podpisant1 = input("Ввод: ")

if UR_lic == True:  # обработчик исключений на ввод + ввод для корректировки цикл
    podpisant2 = f"в лице {doljn_gendir} {fio_gendir}, действующего на основании Устава"
else:
    podpisant2 = f"в лице Индивидуального предпринимателя {fio_gendir}, действующего на основании ОГРНИП: {ogrnip_org} от {ogrnip_org_data} года"

print(f"""Формулировка:
>>> {podpisant2} <<<
получена из формы верно?
""")
podpisant2_chek = input("+/-: ")  # обработчик исключений на ввод + ввод для корректировки цикл

if podpisant2_chek == "+":
    print("Отлично!")
else:
    print("Введите, пожалуйста, корректную информацию.")
    podpisant2 = input("Ввод: ")
    print("Отлично!")

time.sleep(1)
# 0000000000000000000000000000000000000000000000000000000000000000000000
print("Перейдите по любой из следующих ссылок, для получения дополнительных реквизитов компании.")
url_inn1 = f'Конфиденциальные данные{inn_org}'
# Конфиденциальные данные
url_inn2 = f"Конфиденциальные данные{inn_org}"
url_inn3 = f"Конфиденциальные данные{inn_org}&search_inactive=0"
print(url_inn1)
print(url_inn2)
print(url_inn3)
okpo = input("Введите ОКПО организации: ")
oktmo = input("Введите ОКТМО организации: ")
okopf = input("Введите ОКОПФ организации: ")
url_inn4 = "Конфиденциальные данные"
print("На сайте Конфиденциальные данные посмотрите в заявке участника его банковские реквизиты:")
print(url_inn4)
rasch_schet = input("Введите расчетный счет организации: ")
korr_schet = input("Введите корр. счет организации: ")
imya_banka = input("Введите название банка организации: ")
bik = input("Введите БИК банка организации: ")
time.sleep(1)
# 0000000000000000000000000000000000000000000000000000000000000000000000
print("Далее - приступим к формированию Цены контракта.")
print(new_str)
time.sleep(1)
print("Подскажите, будет ли увеличение цены контракта до НМЦК?")
time.sleep(1)
print("""
В ответ введите один из следующих символов:
        + (что значит - да, доводим до НМЦК)
        - (что значит - нет, не доводим)
        * (что значит - доводим, но частично (сумма меняется в пределах НМЦК)
        """)
ck_vbr = input("Ваш выбор: ")

if ck_vbr == "-":
    ck = ck_predv
elif ck_vbr == "*":
    ck = input("Тогда введите, пожалуйста, цену контракта (числом без пробелов с копейками после запятой): ")  # ввод чисел без пробелов проблема
elif ck_vbr == "+":
    ck = cena_maksimal
else:
    ck = 0
    print("Тут мог быть цикл")

# начало расчета суммы контракта и спецификации

ck = str_to_num_transform(ck)
cena_maksimal = str_to_num_transform(cena_maksimal)
ck_predv = str_to_num_transform(ck_predv)

print(new_str)
time.sleep(1)
print("Подскажите, является ли организация плательщиком НДС?")
time.sleep(1)
url_inn5 = f'Конфиденциальные данные'
print("Кстати, это проверить еще можно с помощью поиска вот тут: " + url_inn5)
print("""
Но вернемся к вопросу: 
    + значит да, контрагент платит 20% НДС;
    - значит нет, конрагент на упрощенной системе налогообложения
""")
time.sleep(1)
nds_vbr = input("Ваш выбор: ")

if nds_vbr == "-":
    nds = "Без НДС"
    ysn = True
elif nds_vbr == "+":
    nds = ck * 20 / 120
    nds = round(nds, 2)
    ysn = False
else:
    print("Что это значит? Попробуйте еще раз...")  # написать цикл

koefauk = ck_predv / cena_maksimal
obespech_gk = ck * (obespech_proc / 100)
obespech_gk = round(obespech_gk, 2)
print(new_str)
print("Угу. Спасибо за сведения! ")
time.sleep(1)
print("Теперь я проведу обобщение, структурирование и анализ собранной информации...")
time.sleep(5)
print("Готово!")
time.sleep(1)
print("Сейчас посмотрим...")
time.sleep(1)
print(new_str)
print("Так...\nВот, что было мной найдено по введенным данным:")
print(new_str)
print("1. " + "Наименование закупки: " + object_zakup)
print("2. " + "ИКЗ: " + ikz)
print("3. " + "Подписант 1: " + podpisant1)
print("4. " + "Подписант 2: " + podpisant2)
print("5. " + f'Протокол подведения итогов № {nomer_zakup}')
print("6. " + f'от {data_results_list[0]} г.')
print("НМЦК: ", cena_maksimal, " ₽")
print("7. " + "Цена контракта: ", ck, " ₽")

if ysn == True:
    print("8. " + "None" + " (контракт не предусматривает расчет НДС)")
else:
    print("8. " + "НДС: ", nds, " ₽")

print("9. " + "КБК для данной закупки будет необходимо отразить в Контракте следующим: " + kbk)

if smp_preimuzhj != None:
    smp_check = True
    shtraf = ck * 0.01
    shtraf = round(shtraf, 2)
    print("Анализ показал, что закупка проводилась среди СМП, поэтому штрафы рассчитывались как 1% от цены контракта. ")
    if shtraf > 5000.0:
        shtraf = 5000.0
    elif shtraf < 1000.0:
        shtraf = 1000.0
else:
    smp_check = False
    shtraf = cena_maksimal * 0.1  # ПЕРЕПРОВЕРИТЬ КАК НЕ У СМП СЧИТАЕТСЯ ШТРАФ!!!!!
    shtraf = round(shtraf, 2)
    print("Анализ показал, что закупка не проводилась среди СМП, поэтому штраф рассчитывался как 10% от НМЦК.  ")

print("10. " + f"В связи с чем, штраф для контрагента по условиям контракта составит: {shtraf} ₽")
print(new_str)
time.sleep(1)
print(f'Коэффициент ценового падения по аукциону равняется: {koefauk}')

if (1 - koefauk) > antidemp_koef and koefauk != 1.0:
    print(f"Это больше, чем {antidemp_koef}. Поэтому к закупке должны быть применены антидемпинговые меры в части обеспечения.")
    obespech_gk = obespech_gk * 1.5
    obespech_gk = round(obespech_gk, 2)
    antidemp = True
else:
    antidemp = False
    print("К закупке антидемпинговые меры в части обеспечения не применяются.")

print("11. " + f"Обеспечение контракта составит: {obespech_gk} ₽")

if antidemp == True:  # момент про что составляет 30% цены контракта
    print(f'    что составляет сумму из расчета {obespech_proc}% от цены, по которой заключается контракт, умноженной в 1,5 раза. ')
else:
    print(f'    что составляет сумму из расчета {obespech_proc}% от цены, по которой заключается контракт. ')

print(new_str)
time.sleep(1)
print("Немного информации об объекте закупки: ")
print(spisok_cen_objecta_zakup)
print(new_str)
time.sleep(1)
print("Реквизиты контрагента:")

if UR_lic == False:
    pcht_adres_org = ur_adres_org

print("12. " + "Полное наименование: " + imya_org)
print("13. " + "Сокращенный вариант: " + sokr_imya_org)
print("14. " + "Юридический адрес: " + ur_adres_org)
print("15. " + "Почтовый адрес: ", pcht_adres_org)
print("16. " + "Контактный телефон: ", telef_org)  # Ввод у ИП
print("17. " + "e-mail: " + email_org)
print("18. " + "ИНН: " + inn_org)
print("19. " + "КПП: ", kpp_org)
print("20. " + "ОГРН: ", ogrn_org)
print("21. " + "ОГРНИП: ", ogrnip_org)
print("22. " + "ОКПО: " + okpo)
print("23. " + "ОКТМО: " + oktmo)
print("24. " + "ОКОПФ: " + okopf)
print("25. " + "р/с: " + rasch_schet)
print("26. " + "к/с: " + korr_schet)
print("27. " + "Наименование банка: " + imya_banka)
print("28. " + "БИК: " + bik)

# proverochnyj_itog_spisok = [
# "place_holrer_0",
# object_zakup, ikz, podpisant1, podpisant2, nomer_zakup, data_results_list[0], ck, nds, kbk, shtraf,
# obespech_gk, imya_org, sokr_imya_org, ur_adres_org, pcht_adres_org, telef_org, email_org, inn_org,
# kpp_org, ogrn_org, ogrnip_org, okpo, oktmo, okopf, rasch_schet, korr_schet, imya_banka, bik
# ]

# Данные заказчика:
time.sleep(1)
print(f""" 
Конфиденциальные данные
""")
print(new_str)
time.sleep(1)
print("На этом моя работа окончена. ")
time.sleep(1)
print("Надеюсь, подготовленная мной информация поможет вам в работе!")
time.sleep(1)
print("Счастливо!")


