# *******************************************************
import telebot as tg
import time
from random import choice as rnd
# *******************************************************
token = '0000000000:xxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxx0'
bot = tg.TeleBot(token)
# *******************************************************
rndtasks = ['Захватить мир', 'Выучить Python', 'Использовать Pyhton, чтобы захватить мир', 'Начать следующую фазу плана']
idfordicts = []
idforfirstrun = []
info = '''
Для передачи мне необходимого запроса просто нажмите на соответствующую команду и следуйте дальнейшим инстукциям!

Блок прямых команд:
Нажмите - /info - 
и я напечатаю данное сообщение с блоком команд еще раз.
Нажмите - /show -
и я выведу на экран все задачи на заданную дату.
Нажмите - /showall -
и я выведу список всех задач.
Нажмите - /add -
и я добавлю новую задачу (Если хотите добавить случайную задачу, то когда я уточню у вас дату добавления, напишите мне "Что-нибудь на твой выбор!" 
Или же воспользуйтесь стандартной командой для этого,
нажав - /random - и я добавлю на сегодня случайную задачу).
Отметить задачу выполненной (или удалить ее) вы можете с помощью нажатия на команду 
- /done - После выбора даты у вас будет возможность отредактировать список имеющихся задач на эту дату.
'''
# *******************************************************
def sms(message, msge):
    bot.send_message(message.chat.id, msge)
# *******************************************************
def echo(msg, ansr):
    vrmtransform = lambda x: time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(x))
    print("{" + vrmtransform(msg.date) + "}", str(msg.chat.id) + ":", msg.text)
    print("{" + vrmtransform(msg.date) + "}", " ", "to", str(msg.chat.id), ":", ansr)
# *******************************************************
@bot.message_handler(commands=['start'])
def start(message):
    global idforfirstrun
    if message.chat.id not in idforfirstrun:
        reg(message)
        sms(message, "Здравствуйте! Так как это наше с вами знакомство, хочу вас немного проконсультировать на счет моих функций и возможностей.")
        time.sleep(1)
        sms(message, "На данный момент в мой функционал входят различные команды по управлению списком задач пользователя.")
        time.sleep(1)
        sms(message, "Я могу создавать, удалять и выводить задачи. Подробнее вы можете ознакомиться с моими возможностями в блоке команд, вызываемом по нажатию на /info или же по вводу такой комбинации в чат. Обязательно ознакомьтесь с ним!")
        time.sleep(1)
        sms(message, "Мой интерфейс был разработан так, чтобы индивидуально общаться с каждым пользователем. А также я могу взаимодейстовать с вами через простой диалог.")
        time.sleep(1)
        sms(message, "Я все еще не так хорошо понимаю человеческую речь, как хотелось бы, но я буду очень стараться! Надеюсь на ваше понимание!")
        time.sleep(1)
        sms(message, "На этом все! Желаю вам приятных впечатлений от работы со мной!")
    else:
        sms(message, "Вы опять хотите начать со вступления? ")
        time.sleep(1)
        sms(message, "Я все же рекомендую вам ознакомиться с ним в истории нашей с вами переписки.")
        time.sleep(1)
        sms(message, "Также, если вы любите использовать блок команд, предлагаю нажать на /info.")
    answer = "Вывод стартовой инструкции пользователю..."
    echo(message, answer)

def reg(message):
    global idfordicts, idforfirstrun
    chatid = str(message.chat.id)
    todos = "todos" + chatid        # регистрация нового ИД по номеру чата
    globals()[f"{todos}"] = dict()  # создание пустого словаря с именем ИД + todos
    idfordicts.append(eval(todos))  # добавление созданного словаря в общую библиотеку словарей (глобал вызов)
    idforfirstrun.append(message.chat.id)
# *******************************************************
def add_todo(dateforusertodoinquiry, taskforusertodoinquiry, message):
    chatid = str(message.chat.id)
    todos = "todos" + chatid
    dateforusertodoinquiry = dateforusertodoinquiry.lower()
    if eval(todos).get(dateforusertodoinquiry) is not None:
        eval(todos)[dateforusertodoinquiry].append(taskforusertodoinquiry)
    else:
        eval(todos)[dateforusertodoinquiry] = [taskforusertodoinquiry]
# *******************************************************
@bot.message_handler(commands=['info'])
def instructions(message):
    sms(message, info)
    answer = "Вывод инструкций пользователю по запросу"
    echo(message, answer)
# *******************************************************
@bot.message_handler(commands=['add'])
def addtask(message):
    if message.chat.id not in idforfirstrun:
        reg(message)
    inf = bot.send_message(message.chat.id, 'На какую дату вы бы хотели назначить задачу?')
    bot.register_next_step_handler(inf, addtaskquestiondate)

def addtaskquestiondate(message):
    dateforusertodoinquiry = message.text
    message.text = ""
    inf = bot.send_message(message.chat.id, f'Какую задачу хотите назначить на {dateforusertodoinquiry}?')
    bot.register_next_step_handler(inf, addtaskquestiontask, message.text, dateforusertodoinquiry)

def addtaskquestiontask(message, value, dateforusertodoinquiry):
    taskforusertodoinquiry = message.text
    tskinqtransform = taskforusertodoinquiry.lower()
    if len(taskforusertodoinquiry) >= 3:
        if "что-нибудь на твой выбор" in tskinqtransform or "чтонибудь на твой выбор" in tskinqtransform or "что нибудь на твой выбор" in tskinqtransform or "на твой выбор" in tskinqtransform:
            taskcategory = "@ Рандомные задачи"
            taskforusertodoinquiry = rnd(rndtasks)
            taskfutdquery = taskforusertodoinquiry
            taskforusertodoinquiry = str(taskforusertodoinquiry) + " " + str(taskcategory)
            add_todo(dateforusertodoinquiry, taskforusertodoinquiry, message)
            answer = f'Задача "{taskfutdquery}" с категорией "{taskcategory}" добавлена на дату "{dateforusertodoinquiry}"!'
            sms(message, answer)
            echo(message, answer)
        else:
            taskforusertodoinquiry = message.text
            taskfutdquery = message.text
            message.text = ""
            inf = bot.send_message(message.chat.id, f'Какую категорию присвоить задаче "{taskforusertodoinquiry}"?')
            bot.register_next_step_handler(inf, addtaskquestioncategory, message.text, dateforusertodoinquiry, taskforusertodoinquiry, taskfutdquery)
    else:
        answer = 'Название введенной задачи содержит меньше трех символов. Пожалуйста, повторите попытку и введите задачу с тремя и более символами в названии:'
        userretry = bot.send_message(message.chat.id, answer)
        echo(message, answer)
        bot.register_next_step_handler(userretry, addtaskquestiontask, message.text, dateforusertodoinquiry)

def addtaskquestioncategory(message, value, dateforusertodoinquiry, taskforusertodoinquiry, taskfutdquery):
    taskcategory = "@ " + str(message.text)
    taskforusertodoinquiry = taskforusertodoinquiry + " " + taskcategory
    add_todo(dateforusertodoinquiry, taskforusertodoinquiry, message)
    answer = f'Задача "{taskfutdquery}" с категорией "{taskcategory}" добавлена на дату "{dateforusertodoinquiry}"!'
    sms(message, answer)
    echo(message, answer)
# *******************************************************
@bot.message_handler(commands=['random'])
def randomtask(message):
    if message.chat.id not in idforfirstrun:
        reg(message)
    taskforusertodoinquiry = rnd(rndtasks)
    taskcategory = "@ Рандомные задачи"
    timeoftoday = time.strftime("%d.%m.%Y")
    add_todo(f'{timeoftoday}', taskforusertodoinquiry + " " + taskcategory, message)
    answer = f'Задача "{taskforusertodoinquiry}" с категорией "{taskcategory}" добавлена на Сегодня: {timeoftoday} года!'
    sms(message, answer)
    echo(message, answer)
# *******************************************************
@bot.message_handler(commands=['done'])
def donetasks(message):
    if message.chat.id not in idforfirstrun:
        reg(message)
    trig = donetaskstool
    msg = "Выберите одну из них и напишите ее мне!"
    showtaskstool(message, trig, msg)

def donetaskstool(message):
    chatid = str(message.chat.id)
    todos = "todos" + chatid
    dateforusertodoinquiry = message.text.lower()
    if dateforusertodoinquiry in eval(todos):
        tasks = ''
        taskcount = 1
        for i in eval(todos)[dateforusertodoinquiry]:
            tasks += f"[{taskcount}] + {i}\n"
            taskcount += 1
        sms(message, tasks)
        echo(message, "Пользователю высланы списки задач по запросу")
        inf = bot.send_message(message.chat.id, "Пожалуйста, пришлите мне номер задачи, которую следует отметить выполненной. Вы также можете прислать несколько номеров через запятую!")
        bot.register_next_step_handler(inf, donetaskstoolfordone, taskcount, dateforusertodoinquiry)
    else:
        sms(message, 'Такой даты нет. Проверьте, пожалуйста, правильность написания и вызовите команду /show еще раз. Символ -> писать не нужно!')
        echo(message, "Пользователю не высланы списки задач. Введенной даты нет в списках.")

def donetaskstoolfordone(message, numbers, dateoftask):
    chatid = str(message.chat.id)
    todos = "todos" + chatid
    dateforusertodoinquiry = dateoftask
    countnooftask = message.text
    taskcounter = numbers
    listofnumresfromuser = countnooftask.split(",")
    listofnumresfromuser = [x.rstrip(" ").lstrip(" ") for x in listofnumresfromuser]
    listofnumresfromuser = list(filter(None, listofnumresfromuser))
    listforif = list(range(1, taskcounter))
    listforif = list(map(str, listforif))
    checktask = any(map(listforif.__contains__, listofnumresfromuser))
    if checktask == True:
        taskcounter -= 1
        for i in listofnumresfromuser:
            try:
                i = int(i)
            except ValueError:
                sms(message, f"{i} - такого номера нет. Это вообще не номер, проверьте ввод, пожалуйста!")
                continue
            if i >= 1 and i <= taskcounter:
                o = i - 1
                sms(message, f'Готово! Задача "{eval(todos)[dateforusertodoinquiry][o]}" отмечена выполненной!')
                eval(todos)[dateforusertodoinquiry].pop(o)
                echo(message, "Задачи пользователя были отмечены выполненными.")
                if len(eval(todos)[dateforusertodoinquiry]) == 0:
                    del eval(todos)[dateforusertodoinquiry]
            else:
                sms(message, f"{i} - такого номера задачи нет в списке, проверьте правильность ввода!")
    else:
        sms(message, 'Такого номера нет, проверьте правильность ввода! Нужно прислать в ответ число, соответствующее номеру задачи.')
        echo(message, "Пользователю не прислал имеющийся номер задач в списке. Команда прекращена.")
# *******************************************************
@bot.message_handler(commands=['show'])
def showtasks(message):
    if message.chat.id not in idforfirstrun:
        reg(message)
    trig = showtaskcheck
    msg = "Выберите одну из них, напишите мне ее или же напишите несколько через запятую."
    showtaskstool(message, trig, msg)

def showtaskstool(message, trigger, inform):
    chatid = str(message.chat.id)
    todos = "todos" + chatid
    if len(eval(todos)) != 0:
        sms(message, "Пожалуйста, выберите дату. ")
        time.sleep(1)
        sms(message, "Сейчас проверю список доступных... ")
        time.sleep(1)
        sms(message, f"Готово! \nВам доступны следующие даты: ")
        time.sleep(1)
        taskdates = ""
        for eachdate in eval(todos):
            taskdates += f'-> {eachdate}\n'
        sms(message, taskdates)
        echo(message, taskdates)
        time.sleep(1)
        inf = bot.send_message(message.chat.id, inform)
        bot.register_next_step_handler(inf, trigger)
    else:
        sms(message, "Ваш список задач пуст! Добавьте туда что-нибудь!")

def showtaskcheck(message):
    chatid = str(message.chat.id)
    todos = "todos" + chatid
    dateforusertodoinquiry = message.text.lower()
    listofdatesfromuser = dateforusertodoinquiry.split(",")
    listofdatesfromuser = [x.rstrip(" ").lstrip(" ") for x in listofdatesfromuser]
    listofdatesfromuser = list(filter(None, listofdatesfromuser))
    checktask = any(map(eval(todos).__contains__, listofdatesfromuser))
    if checktask == True:
        tasks = ''
        for i in listofdatesfromuser:
            sms(message, i)
            if i != "" and i in eval(todos):
                for j in eval(todos)[i]:
                    tasks += f"+ {j}\n"
            else:
                tasks = f"Такой даты нет! Проверьте правильность ввода и, при необходимости, вызовите команду /show еще раз. Символ -> писать не нужно!.\n"
            sms(message, tasks)
            tasks = ''
        echo(message, "Пользователю высланы списки задач по запросу")
    else:
        tasks = 'Такой даты нет. Проверьте, пожалуйста, правильность написания и вызовите команду /show еще раз. Символ -> писать не нужно!'
        answer = tasks
        sms(message, answer)
        echo(message, "Пользователю не высланы списки задач. Введенной даты нет в списках.")
# *******************************************************
@bot.message_handler(commands=['showall'])
def showalltasks(message):
    if message.chat.id not in idforfirstrun:
        reg(message)
    chatid = str(message.chat.id)
    todos = "todos" + chatid
    if len(eval(todos)) != 0:
        tasks = ""
        for eachdate in eval(todos):
            sms(message, "На " + eachdate + ":")
            echo(message, eachdate)
            for eachtask in eval(todos)[eachdate]:
                tasks += f'+ {eachtask}\n'
            sms(message, tasks)
            echo(message, tasks)
            tasks = " "
    else:
        sms(message, "Ваш список задач пуст! Добавьте туда что-нибудь!")
# *******************************************************
privetstvie = ["привет", "здравствуй", "здаров", "здрась"]
zaprosspravki = ["справк", "что ты умеешь", "что ты можешь", "что можешь", "что умеешь", "твой функционал", "твои навыки", "info"]
zaprosdobzadachi = ["добав", "напоминани", "напомни", "назнач", "todo", "add", "ad", "напомни", "установи"]
zaprospokazat = ["какие", "когда", "покажи", "список", "выведи", "отобрази", "перечень", "show"]
zaprospokazatwse = ["все", "полный список", "showall"]
zaprosrandom = ["рандом", "случайную", "случайное", "на твой выбор", "random"]
zaprosdone = ["отмет", "выполнен", "сдела", "помет", "удали", "стерет", "сотри", "done"]

def is_in_list(str_, words):
    for word in words:
        if word.lower() in str_.lower():
            return True
    return False
# *******************************************************
@bot.message_handler(content_types=["text"])
def recognizing(message):
    msg = message.text.lower()
    privetstviecheck = is_in_list(msg, privetstvie)
    zaprosspravkicheck = is_in_list(msg, zaprosspravki)
    zaprosdobzadachicheck = is_in_list(msg, zaprosdobzadachi)
    zaprospokazatcheck = is_in_list(msg, zaprospokazat)
    zaprospokazatwsecheck = is_in_list(msg, zaprospokazatwse)
    zaprosrandomcheck = is_in_list(msg, zaprosrandom)
    zaprosdonecheck = is_in_list(msg, zaprosdone)
    answer = "Пустое сообщение Оо"
    if msg == None:
        sms(message, msg)
        sms(message, answer)
    elif zaprosdobzadachicheck == True:
        addtask(message)
    elif zaprospokazatwsecheck == True:
        showalltasks(message)
    elif zaprospokazatcheck == True:
        showtasks(message)
    elif zaprosrandomcheck == True:
        randomtask(message)
    elif zaprosdonecheck == True:
        donetasks(message)
    elif zaprosspravkicheck == True:
        instructions(message)
        answer = "Высланы инструкции пользователю."
    elif privetstviecheck == True:
        answer = "Приветик!"
        sms(message, answer)
    else:
        answer = "Хм... пытаюсь понять..."
        sms(message, answer)
    echo(message, answer)
# *******************************************************
bot.polling(none_stop=True, interval=3)
# *******************************************************
