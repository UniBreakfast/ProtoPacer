# Возвращает путь к файлу
from os.path import abspath

# Позволит запрашивать пароль, не показывая, что вводит пользователь.
# from getpass import win_getpass as password_input

# Позволит получать от ОС текущую дату.
from datetime import date
today=date.today

# Позволит обрабатывать текстовый файл, находя и изменяя в нём нужные данные.
from dataparser import *



PATH = (abspath(__file__))
file_to_parse = DataParser(PATH)
Endeavors=[]  # Список с объектами класса Стремлений
error_giving_line = -1  # Строка файла с данными, при обработке которой возникла ошибка

# сокращённые print и input посредством pp, pg, it, ig для частоиспользуемых форм вывода.
def pp(text):  # Упрощённый print() для реплик пэйсера
    print(" ~PACER~  " + text)


def pg(text):  # Упрощённый print() для реплик гостя
    print("  гость:  " + text)


def ig(text=None):  # Упрощённый input() для реплик гостя
    return input("  гость:  ")


def it(text=None):  # Упрощённый input() для реплик Тута
    return input("    Тут:  ")

# Функция, предлагающая варианты на выбор и возвращающая выбор пользователя
def choose_from(num, proposition):
    """|
       * Функция, предлагающая варианты на выбор и возвращающая выбор пользователя.
         num - количество вариантов. proposition - текст с вариантами на выбор.
    """
    while True:
        pp(proposition)
        try:
            choice = int(it())
            if choice == num:
                return -1
            elif choice-1 in range(num):
                return choice
        except:
            pass
        pp("Просто введи цифру от 1 до " + str(num))

# Класс Стремлений
class Endeavor:
    def __init__(self, full_name, short_name, details, endeavor_type, create_date, activities=None):
        self.full_name = full_name
        self.short_name = short_name
        self.details = details
        self.endeavor_type = endeavor_type
        self.create_date = create_date
        self.activities = activities

    def __str__(self):
        if self.activities == None:
            return "Cтремление: "+self.full_name+" ("+self.short_name+") - это "+self.endeavor_type+" (c "+str(self.create_date)\
                    +") Детали: "+self.details
        else:
            return "Cтремление: "+self.full_name+" ("+self.short_name+") - это "+self.endeavor_type+" (c "+str(self.create_date)\
                    +") Детали: "+self.details+" Для этого нужно: "+', '.join(self.activities)+"."
# TestEndeavor=Endeavor("Ложиться спать до девяти вечера", "Сон21", "Если я буду вовремя ложиться спать, то буду гораздо"+
#                     " здоровее и эффективнее.", "+привычка", today(), ["Планировать день", "Не есть после шести"])
# print(str(TestEndeavor)) Test
# Устаревшая функция, создававшая Стремление со слов пользователя
def new_endeavor():
    while True:
        pp('Сформулируй своё Стремление в форме ответа на вопрос "Что сделать?" (в одну строчку). Это будет полным названием.')
        full_name=it()
        if full_name != '':
            break
        else:
            pp("Это обязательный пункт!")
    while True:
        pp('Теперь определимся с кратким названием (можно то же, но без пробелов и с понятными сокращениями в словах).')
        short_name=it()
        if short_name != '':
            break
        else:
            pp("Это обязательный пункт!")
    pp('Напиши немного детальнее о сути этого Стремления (можно несколько предложений).')
    details=it()
    if details=='':
        pp("Ладно, детальное описание можно и потом добавить...")
    endeavor_type=["мечта", "цель", "желание", "задача", "навык", "+привычка", "-привычка", "проблема", "гирька"][choose_from(9, 'Наконец выбери тип данного Стремления: мечта (1), цель (2), желание (3),\nзадача (4), навык (5), нужная привычка (6), вредная привычка (7), проблема (8), "гирька" (9)')-1]
    create_date=today()
    pp("Я готов записать такое Стремление:\n        Название:    "+full_name+"\nКраткое название:    "+short_name+"\n          Детали:    "+details+"\nТип:    "+endeavor_type+"       Дата добавления:    "+str(create_date))
    choice = choose_from(2, "Подтвердить и сохранить (1) или Сбросить и забыть (2)?")
    if choice == 1:
        Endeavors.append(Endeavor(full_name, short_name, details, endeavor_type, create_date))
    else:
        pp("Проехали...")

# Громоздкая функция, читавшая файл
def read_stored_data(record_type):
    num_of_rec_found = 0
    try:
        error_giving_line = -1
        with open('PacerData.txt', 'r', encoding='utf-8') as file:
            pacerData = file.readlines()
            record_type_dict = {"Endeavors" : "/  Cтремления  \\(())", "Activities" : "/  Действия  \\[[]]", "ActiveQuests" : "/  Квесты  \\{{}}"}
            for i in range(len(pacerData)):
                error_giving_line = i
                if pacerData[i].find(record_type_dict[record_type][0:-4]) != -1:
                    break
            i+=1
            for i in range(i, len(pacerData)):
                error_giving_line = i
                if pacerData[i].find("*") == -1 and pacerData[i].find(record_type_dict[record_type][-4:-2]) != -1 and pacerData[i].find(record_type_dict[record_type][-2:]) != -1 and pacerData[i].find("   от ") != -1:
                    full_name=pacerData[i][:pacerData[i].find(record_type_dict[record_type][-4:-2])-3]
                    short_name=pacerData[i][pacerData[i].find(record_type_dict[record_type][-4:-2])+2:pacerData[i].find(record_type_dict[record_type][-2:])]
                    details=pacerData[i+1].strip()
                    endeavor_type=pacerData[i][pacerData[i].find(record_type_dict[record_type][-2:]):pacerData[i].find("   от")]
                    create_date=date(int(pacerData[i][pacerData[i].find("   от")+6:pacerData[i].find("   от")+10]), int(pacerData[i][pacerData[i].find("   от")+11:pacerData[i].find("   от")+13]), int(pacerData[i][pacerData[i].find("   от")+14:pacerData[i].find("   от")+16]))
                    Endeavors.append(Endeavor(full_name, short_name, details, endeavor_type, create_date))
                    num_of_rec_found+=1
                elif pacerData[i][:3] == "___":
                    break
            return num_of_rec_found
    except:
        pp("ОШИБКА! файл с данными отсутствует или данные имеют неправильный формат в районе строки "+str(error_giving_line+1)+".")
        return num_of_rec_found

# Незаконченный класс Действий
class Activity:
    def __init__(self, full_name, short_name, amount, diff, usef):
        self.full_name=full_name
        self.short_name=short_name
        self.amount=amount
        self.diff=diff
        self.usef=usef


class Quest:
    def __init__(self, full_name, short_name, amount, actual_diff, usef, start_date):
        pass

###############################################################################################################

# INI = 'ProtoPacer0.ini'
# if not file_to_parse.is_it_there('f', INI):
#     with open(INI, 'w', encoding="utf-8") as file:
#         file.writelines(['[известные пользователи]\n','\n','[конец]'])
#
# file_to_parse.name = abspath(INI)
# users_y1 = file_to_parse.where_is_it("[известные пользователи]")[0][0]+1
# users_y2 = file_to_parse.where_is_it("[", start_line=users_y1)[0][0]
# users_in_INI = file_to_parse.where_is_it(': ', start_line=users_y1, fin_line=users_y2)
# num_of_users = len(users_in_INI)
# user_dic = {}
# for u in range(num_of_users):
#     user_dic[file_to_parse.grab_it_there(SOL_to_coords(users_in_INI[u]))] = file_to_parse.grab_it_there(coords_to_EOL(users_in_INI[u]))
#
# def main():
#     pass
#
#
#
# print("\n   Вас приветствует PACER - игровой органайзер, задающий темп!\n")
# pp("Представьтесь пожалуйста")
# user = "Тут" # Заглушка: пропускаем ввод имени пользователя, по умолчанию считаем, что введено "Тут"
# # user = ig()
# pg("Тут")
# if user == "Тут":
#     pp(user+", если это правда ты, докажи, введя пароль.")
#     password = "*********" # Заглушка: пропускаем ввод и проверку пароля.
#     # password = ig()
#     pg("*********")
#     if password == "*********":
#         pp("Ладно, прости. Заходи, "+user+". Рад тебя видеть!")
#         file_to_parse = DataParser(user_dic[user])
#         while True:
#             print("\n            1. Стремления\n            2. Действия\n            3. Квесты\n            4. Вера В Себя  ( 115 )\n            5. Статистика\n            6. Отчитаться  ( 2 / 5 )\n            7. Выйти\n")
#             choice = choose_from(7, "Мы с тобой можем заняться твоими Стремлениями (1), Действиями (2) или Квестами (3).\nМожем поговорить о твоей Вере_В_Себя (4). Можем посмотреть Статистику (5).\nИли ты можешь просто Отчитаться по текущим заданиям (6). Или выйти (7).")
#             if choice == 1:
#                 num_of_Endeavors = read_stored_data("Endeavors")
#                 if  num_of_Endeavors > 0:
#                     pp("Знаешь, сколько твоих Стремлений у меня уже записано? "+str(num_of_Endeavors)+".")
#                     print(Endeavors[7].endeavor_type)
#                 else:
#                     while True:
#                         choice = choose_from(2, "Мне пока ничего не известно о твоих Стремлениях.\nРасскажешь мне про Стремление, которое ты хочешь Добавить (1)?\nИли пока Отложим (2) и займёмся чем-то другим?")
#                         if choice == 1:
#                             new_endeavor()
#                         elif choice == -1:
#                             break
#             elif choice == 2:
#                 pass
#             elif choice == 3:
#                 pass
#             elif choice == 4:
#                 try:
#                     with open('PacerData.txt', 'r+', encoding='utf-8') as file:
#                         pacerData = file.readlines()
#                         BBCprev = int(pacerData[0][pacerData[0].find(" ВВС = ") + len(" ВВС = "):])
#                         pp("Насколько мне известно, твоя нынешняя Вера_В_Себя равняется " + str(BBCprev))
#                         pp("Как она изменилась с прошлого раза?")
#                         BBC = BBCprev + int(it())
#                         pp("Тогда теперь твоя Вера_В_Себя составляет " + str(BBC))
#                         file.seek(0)
#                         file.truncate()
#                         pacerData[0]=pacerData[0].replace(str(BBCprev), str(BBC))
#                         file.writelines(pacerData)
#                 except:
#                     pp("Похоже что-то не так с файлом с данными...")
#             elif choice == 5:
#                 pass
#             elif choice == 6:
#                 pass
#             elif choice == -1:
#                 pp("Всего хорошего!")
#                 exit()
#     else:
#         pp("Вон отсюда, самозванец!")
# else:
#     pp("Понятия не имею, кто вы. Всего хорошего.")


def LOGGING_IN():
    global file_to_parse
    INI = __file__[:-2]+'ini'
    if not file_to_parse.is_it_there('f', INI):
        with open(INI, 'w', encoding="utf-8") as file:
            file.writelines(['[известные пользователи]\n', '\n', '[конец]'])

    file_to_parse.name = abspath(INI)
    users_y1 = file_to_parse.where_is_it("[известные пользователи]")[0][0] + 1
    users_y2 = file_to_parse.where_is_it("[", start_line=users_y1)[0][0]
    users_in_INI = file_to_parse.where_is_it(': ', start_line=users_y1, fin_line=users_y2)
    num_of_users = len(users_in_INI)
    user_dic = {}
    for u in range(num_of_users):
        user_dic[file_to_parse.grab_it_there(SOL_to_coords(users_in_INI[u]))] = file_to_parse.grab_it_there(
            coords_to_EOL(users_in_INI[u]))

    print("\n   Вас приветствует PACER - игровой органайзер, задающий темп!\n")
    pp("Представьтесь пожалуйста")
    user = "Тут"  # Заглушка: пропускаем ввод имени пользователя, по умолчанию считаем, что введено "Тут"
    # user = ig()
    pg("Тут")
    if user == "Тут":
        pp(user + ", если это правда ты, докажи, введя пароль.")
        password = "*********"  # Заглушка: пропускаем ввод и проверку пароля.
        # password = ig()
        pg("*********")
        if password == "*********":
            pp("Ладно, прости. Заходи, " + user + ". Рад тебя видеть!")
            file_to_parse = DataParser(user_dic[user])
        else:
            pp("Вон отсюда, самозванец!")
    else:
        pp("Понятия не имею, кто вы. Всего хорошего.")


def MAIN():
    while True:
        print(
            "\n            1. Стремления\n            2. Действия\n            3. Квесты\n            4. Вера В Себя  ( 115 )\n            5. Статистика\n            6. Отчитаться  ( 2 / 5 )\n            7. Выйти\n")
        choice = choose_from(7,
                             "Мы с тобой можем заняться твоими Стремлениями (1), Действиями (2) или Квестами (3).\nМожем поговорить о твоей Вере_В_Себя (4). Можем посмотреть Статистику (5).\nИли ты можешь просто Отчитаться по текущим заданиям (6). Или выйти (7).")
        if choice == 1:
            num_of_Endeavors = read_stored_data("Endeavors")
            if num_of_Endeavors > 0:
                pp("Знаешь, сколько твоих Стремлений у меня уже записано? " + str(num_of_Endeavors) + ".")
                print(Endeavors[7].endeavor_type)
            else:
                while True:
                    choice = choose_from(2,
                                         "Мне пока ничего не известно о твоих Стремлениях.\nРасскажешь мне про Стремление, которое ты хочешь Добавить (1)?\nИли пока Отложим (2) и займёмся чем-то другим?")
                    if choice == 1:
                        new_endeavor()
                    elif choice == -1:
                        break
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            try:
                with open('PacerData.txt', 'r+', encoding='utf-8') as file:
                    pacerData = file.readlines()
                    BBCprev = int(pacerData[0][pacerData[0].find(" ВВС = ") + len(" ВВС = "):])
                    pp("Насколько мне известно, твоя нынешняя Вера_В_Себя равняется " + str(BBCprev))
                    pp("Как она изменилась с прошлого раза?")
                    BBC = BBCprev + int(it())
                    pp("Тогда теперь твоя Вера_В_Себя составляет " + str(BBC))
                    file.seek(0)
                    file.truncate()
                    pacerData[0] = pacerData[0].replace(str(BBCprev), str(BBC))
                    file.writelines(pacerData)
            except:
                pp("Похоже что-то не так с файлом с данными...")
        elif choice == 5:
            pass
        elif choice == 6:
            pass
        elif choice == -1:
            pp("Всего хорошего!")
            exit()


while True:
    LOGGING_IN()

    MAIN()

