from datetime import date
today=date.today


def pp(text):  # Упрощённый print() для реплик пэйсера
    print("  PACER:  " + text)


def ig(text=None):  # Упрощённый input() для реплик гостя
    return input("  гость:  ")


def it(text=None):  # Упрощённый input() для реплик Тута
    return input("    Тут:  ")


def choose_from(num, proposition):
    pp(proposition)
    try:
        choice = int(it())
        if choice == num:
            return -1
        elif choice-1 in range(num):
            return choice
        else:
            pp("Просто введи цифру от 1 до "+ str(num))
            return choose_from(num, proposition)
    except:
        pp("Просто введи цифру от 1 до "+ str(num))
        return choose_from(num, proposition)


class Endeavor:
    def __init__(self, full_name, short_name, details, endeavor_type, create_date):
        self.full_name = full_name
        self.short_name = short_name
        self.details = details
        self.endeavor_type = endeavor_type
        self.create_date = create_date


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


def read_stored_data(record_type):
    with open('PacerData.txt', 'r', encoding='utf-8') as file:
        pacerData = file.readlines()
        record_type_dict = {"Endeavors" : "/  Cтремления  \\(())", "Activities" : "/  Действия  \\[[]]", "ActiveQuests" : "/  Квесты  \\{{}}"}
        for i in range(len(pacerData)):
            if pacerData[i].find(record_type_dict[record_type][:-4]) != -1:
                break
        i+=1
        for i in range(i, len(pacerData)):
            if pacerData[i].find("*") == -1 and pacerData[i].find(record_type_dict[record_type][-4:-2]) != -1:
                full_name=pacerData[i][:pacerData[i].find(record_type_dict[record_type][-4:-2])-3]
                short_name=pacerData[i][pacerData[i].find(record_type_dict[record_type][-4:-2])+2:pacerData[i].find(record_type_dict[record_type][-2:])]
                details=pacerData[i+1].strip()
                endeavor_type=pacerData[i][pacerData[i].find(record_type_dict[record_type][-2:])+5:pacerData[i].find("   от")]
                create_date=date(int(pacerData[i][pacerData[i].find("   от")+6:pacerData[i].find("   от")+10]), int(pacerData[i][pacerData[i].find("   от")+11:pacerData[i].find("   от")+13]), int(pacerData[i][pacerData[i].find("   от")+14:pacerData[i].find("   от")+16]))
                Endeavors.append(Endeavor(full_name, short_name, details, endeavor_type, create_date))
            elif pacerData[i][0] == "_":
                break


class Activity:
    def __init__(self, full_name, short_name, amount, diff, usef):
        self.full_name=full_name
        self.short_name=short_name
        self.amount=amount
        self.diff=diff
        self.usef=usef


class ActiveQuest:
    def __init__(self, full_name, short_name, amount, actual_diff, usef, start_date):
        pass


print("\n   Вас приветствует PACER\n")
pp("Представьтесь пожалуйста")
user = "Тут" # пропускаем проверку для отладки
# user = ig()
if user == "Тут":
    pp("Тут, если это правда ты, докажи, введя пароль.")
    password = "Не морочь мне голову, пасер." # быстрый проход без пароля
    # password = ig()
    if password == "Не морочь мне голову, пасер.":
        pp("Ладно, прости. Заходи, Тут. Рад тебя видеть!")
        Endeavors=[]
        while True:
            print()
            choice = choose_from(7, "Мы с тобой можем заняться твоими Стремлениями (1), Действиями (2) или Квестами (3).\nМожем поговорить о твоей Вере_В_Себя (4). Можем посмотреть Статистику (5).\nИли можешь просто Отчитаться по текущим заданиям (6). Или выйти (7).")
            if choice == 1:
                while True:
                    choice = choose_from(2, "Мне пока ничего не известно о твоих Стремлениях.\nРасскажешь мне про Стремление, которое ты хочешь Добавить (1)?\nИли пока Отложим (2) и займёмся чем-то другим?")
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
                        pacerData[0]=pacerData[0].replace(str(BBCprev), str(BBC))
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
    else:
        pp("Вон отсюда, самозванец!")
else:
    pp("Понятия не имею, кто вы. Всего хорошего.")
