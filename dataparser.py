class DataParser:
    """|
       * Класс с методами для чтения/записи данных в текстовый файл
         с определённой разметкой и форматированием текста.
         При создании объекта класса принимает аргументом имя файла
         с путём или без. Требуемый формат: C:/Folder/folder/example.txt
         Расширение может быть другим, но формат должен быть простой текст.
         Второй аргумент - символ начала строки комментария, опционален.
         Если он не указан, методы класса DataParser будут игнорировать строки,
         начинающиеся со *
    """
    def __init__(self, file_name, commentline_symbol='*'):
        self.name = file_name
        if len(commentline_symbol) != 1:
            raise ValueError ("commentline_symbol should be one symbol exactly")
        else:
            self.commentary = commentline_symbol


    def is_it_there(self, what_type, sample):
        """|
           * Метод is_it_there проверяет наличие образца sample типа what_type...
           "f" - (think "file") файла с именем sample по указанному пути (в той же папке),
           "b" - (think "block") блока (sample - лист из нескольких строк подряд) в указанном файле,
           "l" - (think "line") линии (sample - строчка целиком) в указанном файле,
           "s" - (think "string") строки (sample - искомых фрагмент строки) в указанном файле.
            Возвращает True или False.
        """

        if what_type == 'f':
            if sample == self.name[self.name.rfind("/")+1:]:
                try:
                    open(self.name).close()
                    return True
                except:
                    return False
            else:
                path = self.name
                path = path[:path.rfind("/") + 1]
                try:
                    open(path+sample).close()
                    return True
                except:
                    return False

        elif what_type =='b':
            with open(self.name, 'r', encoding='utf-8') as file:
                file_as_list = [line.strip() for line in file]
                sample = [line.strip() for line in sample]
                len_s = len(sample)
                len_f = len(file_as_list)
                if len_s > len_f:
                    return False
                for j in range(len_f):
                    if sample[0] == file_as_list[j]:
                        for i in range(1,len_s):
                            if sample[i] != file_as_list[j+i]:
                                break
                            if i == len_s-1:
                                return True
                return False

        elif what_type =='l':
            with open(self.name, 'r', encoding='utf-8') as file:
                file_as_list = [line.strip() for line in file]
                sample = sample.strip()
                if sample in file_as_list:
                    return True
                return False

        elif what_type =='s':
            with open(self.name, 'r', encoding='utf-8') as file:
                file_as_list = [line.strip() for line in file]
                len_f = len(file_as_list)
                sample = sample.strip()
                for j in range(len_f):
                    if sample in file_as_list[j] and file_as_list[j][0] != self.commentary:
                        return True
                return False

        else:
            raise ValueError("unexpected what_type parameter, use 'f','b','l' or 's'")


    def where_is_it(self, sample, sample2=None, start_line=0, fin_line=-1):
        """|
           * Метод находит в файле вхождения строчного фрагмента текста sample (если не задан sample2)
             или строчного фрагмента текста находящегося между sample и sample2 (в одной строке).
             Возвращает список вхождений, где каждое вхождение описано вложенным списком из значений:
             y - номер строки, x1 - позиция первого символа, x2 - позиция символа за последним. Нумерация с нуля.
             [ [y, x1, x2], [..., ..., ...], ... ]
             start_line и fin_line - могут сужать диапазон поиска до участка между этими строками [...)
        """
        sample = str(sample)
        list_of_pos = []
        with open(self.name, 'r', encoding='utf-8') as file:
            file_as_list = [line.strip() for line in file]
            # sample = sample.strip()
            len_s = len(sample)
            if fin_line == -1:
                fin_line = len(file_as_list)

            if sample2 == None:
                for j in range(start_line,fin_line):
                    if file_as_list[j].find(sample) != -1 and file_as_list[j][0] != self.commentary:
                        i = 0
                        while i <= len(file_as_list[j]) - len_s:
                            if file_as_list[j].find(sample, i) != -1:
                                x1 = file_as_list[j].find(sample, i)
                                x2 = x1 + len_s
                                list_of_pos.append([j, x1, x2])
                                i = x2
                            else:
                                break

            else:
                len_s2 = len(sample2)
                for j in range(start_line,fin_line):
                    if file_as_list[j].find(sample) != -1 and file_as_list[j].find(sample2) != -1 and file_as_list[j][0] != self.commentary:
                        i = 0
                        while i <= len(file_as_list[j]) - len_s - len_s2:
                            if file_as_list[j].find(sample, i) != -1 and file_as_list[j].find(sample2, i+len_s) != -1:
                                x1 = file_as_list[j].find(sample, i) + len_s
                                x2 = file_as_list[j].find(sample2, i+len_s)
                                list_of_pos.append([j, x1, x2])
                                i = x2 + len_s2
                            else:
                                break
        if len(list_of_pos) == 0:
            return None
        return list_of_pos

# D = DataParser('C:/Users/Администратор/Documents/GitHub/ProtoPacer/PacerData.txt')
# print(D.where_is_it("((", "))"))
    def grab_it_there(self, coords):
        """|
           * Метод возвращает строку (или список строк), находящийся в обрабатываемом файле в указанном месте.
             координаты должны быть в формате [y, x1, x2], где
             y - номер строки, x1 - позиция первого символа, x2 - позиция символа за последним.
             Или в формате [y1, y2], где
             y1 - номер первой интересующей строки, а y2 - номер строки за последней.
             Нумерация с нуля.
        """
        with open(self.name, 'r', encoding='utf-8') as file:
            file_as_list = [line.strip() for line in file]

            if len(coords) == 3:
                y, x1, x2 = coords
                if x2 == -1:
                    return file_as_list[y][x1:]
                else:
                    return file_as_list[y][x1:x2]

            elif len(coords) == 2:
                y1, y2 = coords
                if y2-y1 == 1:
                    return file_as_list[y1][0]
                else:
                    return file_as_list[y1:y2]

            else:
                raise ValueError ("incorrect range")

def SOL_to_coords(coords):
    return [coords[0], 0, coords[1]]

def coords_to_EOL(coords):
    return [coords[0], coords[2], -1]