
def LOGGING_IN():

    while  True:        <<<A>>>
        решить, что имя не введено
        while имя не введено:
            просить сказать, какое имя пользователя?

        ... когда имя введено...

        if имя знакомо (есть в INI):
            посмотреть, как называется соответствующий ему файл.
            break       >B<

        else (новый польззователь):
            if создать?:
                решить, что имя файла не выбрано
                while имя файла не выбрано:
                    спросить, как назвать файл данных?

                записать в INI имя пользователя и его файла данных.
                break       >B<

            else (не создавать):
                continue всё с начала...        >A<

    if указанного файла нет:        <<<B>>>
        сообщить и создать его.
    взять файл, соответствующий имени пользователя, и считать его в память.

    На выходе имеем: имя пользователя, имя его файла, переменную, в которую его файл считан
        и объект класса ПарсируемыйФайл, подразумевающий его файл.