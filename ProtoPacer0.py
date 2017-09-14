def pp(text):  # Упрощённый print() для реплик пэйсера
    print("  PACER:  " + text)


def ig(text=None):  # Упрощённый input() для реплик гостя
    return input("  гость:  ")


def it(text=None):  # Упрощённый input() для реплик Тута
    return input("    Тут:  ")


class Endeavor:
    def __init__(self, fName, sName, details, type):
        self.fName = fName
        self.sName = sName
        self.details = details
        self.type = type


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
        pp("Ладно, прости. Заходи, Тут. Рад тебя видеть!\n")
        try:
            while True:
                choice = input("  PACER:  Мы с тобой можем заняться твоими Стремлениями (1), Действиями (2) или Квестами (3).\nМожем поговорить о твоей Вере_В_Себя (4). Можем посмотреть Статистику (5).\nИли можешь просто Отчитаться по текущим заданиям (6). Или выйти (7).\n    Тут:  ")
                if choice in ("1","2","3","4","5","6","7"):
                    choice = int(choice)
                    if choice == 1:
                        pass
                    elif choice == 2:
                        pass
                    elif choice == 3:
                        pass
                    elif choice == 4:
                        file = open('PacerData.txt', 'r+', encoding='utf-8')
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
                        file.close()
                    elif choice == 5:
                        pass
                    elif choice == 6:
                        pass
                    elif choice == 7:
                        pp("Всего хорошего!")
                        exit()
                else:
                    pp("Просто введи цифру от 1 до 7")
                    continue
        except IndexError:
            pp("Файла нет или он пустой?")
    else:
        pp("Вон отсюда, самозванец!")
else:
    pp("Понятия не имею, кто вы. Всего хорошего.")
