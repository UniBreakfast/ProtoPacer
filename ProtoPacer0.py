from datetime import date
today=date.today


def pp(text):  # Упрощённый print() для реплик пэйсера
    print("  PACER:  " + text)


def ig(text=None):  # Упрощённый input() для реплик гостя
    return input("  гость:  ")


def it(text=None):  # Упрощённый input() для реплик Тута
    return input("    Тут:  ")


def ChooseFrom(num, proposition):
    pp(proposition)
    try:
        choice = int(it())
        if choice == num:
            return -1
        elif choice-1 in range(num):
            return choice
        else:
            pp("Просто введи цифру от 1 до "+ str(num))
            return ChooseFrom(num, proposition)
    except:
        pp("Просто введи цифру от 1 до "+ str(num))
        return ChooseFrom(num, proposition)


class Endeavor:
    def __init__(self, fName, sName, details, Etype, createDate):
        self.fName = fName
        self.sName = sName
        self.details = details
        self.Etype = Etype
        self.createDate = createDate


def newEndeavor():
    while True:
        pp('Сформулируй своё Стремление в форме ответа на вопрос "Что сделать?" (в одну строчку). Это будет полным названием.')
        fName=it()
        if fName != '':
            break
        else:
            pp("Это обязательный пункт!")
    while True:
        pp('Теперь определимся с кратким названием (можно то же, но без пробелов и с понятными сокращениями в словах).')
        sName=it()
        if sName != '':
            break
        else:
            pp("Это обязательный пункт!")
    pp('Напиши немного детальнее о сути этого Стремления (можно несколько предложений).')
    details=it()
    if details=='':
        pp("Ладно, детальное описание можно и потом добавить...")
    Etype=["мечта", "цель", "желание", "задача", "навык", "+привычка", "-привычка", "проблема", "гирька"][ChooseFrom(9, 'Наконец выбери тип данного Стремления: мечта (1), цель (2), желание (3),\nзадача (4), навык (5), нужная привычка (6), вредная привычка (7), проблема (8), "гирька" (9)')-1]
    createDate=today()
    pp("Я готов записать такое Стремление:\nНазвание:    "+fName+"\nКраткое название:    "+sName+"\nДетали:    "+details+"\nТип:    "+Etype+"       Дата добавления:    "+str(createDate))
    choice = ChooseFrom(2, "Подтвердить и сохранить (1) или Сбросить и забыть (2)?")
    if choice == 1:
        Endeavors.append(Endeavor(fName, sName, details, Etype, createDate))
    else:
        pp("Проеали...")


class Activity:
    def __init__(self, fName, sName, amount, diff, usef):
        self.fName=fName
        self.sName=sName
        self.amount=amount
        self.diff=diff
        self.usef=usef


class ActiveQuest:
    def __init__(self, fName, sName, amount, actualDiff, usef, startDate):
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
            choice = ChooseFrom(7, "Мы с тобой можем заняться твоими Стремлениями (1), Действиями (2) или Квестами (3).\nМожем поговорить о твоей Вере_В_Себя (4). Можем посмотреть Статистику (5).\nИли можешь просто Отчитаться по текущим заданиям (6). Или выйти (7).")
            if choice == 1:
                while True:
                    choice = ChooseFrom(2, "Мне пока ничего не известно о твоих Стремлениях.\nРасскажешь мне про Стремление, которое ты хочешь Добавить (1)?\nИли пока Отложим (2) и займёмся чем-то другим?")
                    if choice == 1:
                        newEndeavor()
                    elif choice == -1:
                        break
            elif choice == 2:
                pass
            elif choice == 3:
                pass
            elif choice == 4:
                try:
                    with open('PacerData.txt', 'r+', encoding='utf-8') as file:
                        PacerData = file.readlines()
                        BBCprev = int(PacerData[0][PacerData[0].find(" ВВС = ") + len(" ВВС = "):])
                        pp("Насколько мне известно, твоя нынешняя Вера_В_Себя равняется " + str(BBCprev))
                        pp("Как она изменилась с прошлого раза?")
                        BBC = BBCprev + int(it())
                        pp("Тогда теперь твоя Вера_В_Себя составляет " + str(BBC))
                        file.seek(0)
                        file.truncate()
                        PacerData[0]=PacerData[0].replace(str(BBCprev), str(BBC))
                        file.writelines(PacerData)
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
