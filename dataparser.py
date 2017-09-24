def SOL_to_coords(coords):
    return [coords[0], 0, coords[1]]


def coords_to_EOL(coords):
    return [coords[0], coords[2], -1]



class DataParser:
    """|
       * Класс с методами для чтения/записи данных в текстовом файле или в массиве строк с текстом
         с определённой разметкой и форматированием.
         При создании объекта класса принимает аргументом имя файла (с путём или без) или непосредственно лист
         строк. Требуемый формат: C:/Folder/folder/example.txt (example.txt если файл в рабочей папке)
         или ["строка1", "строка2", "строка3", ...]
         Расширение файла может быть любым, но по формату это должен быть простой текст.
         Второй аргумент - символ начала строки комментария - опционален.
         Если он не указан, методы класса DataParser будут игнорировать строки, начинающиеся со *
    """
    def __init__(self, data_source, commentline_symbol='*'):

        if 'str' in str(type(data_source)):
            self.name = data_source
            with open(data_source, 'r', encoding='utf-8') as file:
                self.data = file.readlines()
        elif 'list' in str(type(data_source)):
            self.data = data_source
            self.name = None
        else:
            raise ValueError ("data_source should be a string with a [path/]filename of a list of text-strings")

        if len(commentline_symbol) != 1:
            raise ValueError ("commentline_symbol should be one symbol exactly")
        else:
            self.commentary = commentline_symbol


    def is_it_there(self, what_type, sample):
        """|
           * Метод "это_там?" проверяет наличие образца sample типа what_type...
           "f" - (think "file") файла с именем sample по указанному пути (в той же папке),
           "b" - (think "block") блока (sample - лист из нескольких строк подряд) в указанном файле,
           "l" - (think "line") линии (sample - строчка целиком) в указанном файле,
           "s" - (think "string") строки (sample - искомых фрагмент строки) в указанном файле.
            Возвращает True или False.
        """

        if what_type == 'f':
            if self.name == None:
                try:
                    open(sample).close()
                    return True
                except:
                    return False
            elif sample == self.name[self.name.rfind("/")+1:]:
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
            if self.name != None:
                with open(self.name, 'r', encoding='utf-8') as file:
                    self.data = file.readlines()
            # sample = [line.strip() for line in sample]
            len_s = len(sample)
            len_d = len(self.data)
            if len_s > len_d:
                return False
            for j in range(len_d):
                if sample[0] == self.data[j]:
                    if len_s == 1:
                        return True
                    for i in range(1,len_s):
                        if sample[i] != self.data[j+i]:
                            break
                        if i == len_s-1:
                            return True
            return False

        elif what_type =='l':
            if self.name != None:
                with open(self.name, 'r', encoding='utf-8') as file:
                    self.data = file.readlines()
            if sample in self.data:
                return True
            else:
                return False

        elif what_type =='s':
            if self.name != None:
                with open(self.name, 'r', encoding='utf-8') as file:
                    self.data = file.readlines()
            len_d = len(self.data)
            # sample = sample.strip()
            for j in range(len_d):
                if sample in self.data[j] and self.data[j][0] != self.commentary:
                    return True
            return False

        else:
            raise ValueError("unexpected what_type parameter, use 'f','b','l' or 's' for file, block, line or string")


    def where_is_it(self, sample, sample2=None, start_line=0, fin_line=-1):
        """|
           * Метод "где_это" находит в файле вхождения строчного фрагмента текста sample (если не задан sample2)
             или строчного фрагмента текста находящегося между sample и sample2 (в одной строке).
             Возвращает список вхождений, где каждое вхождение описано вложенным списком из значений:
             y - номер строки, x1 - позиция первого символа, x2 - позиция символа за последним. Нумерация с нуля.
             [ [y, x1, x2], [..., ..., ...], ... ]
             start_line и fin_line - могут сужать диапазон поиска до участка между этими строками [...)
        """
        sample = str(sample)
        list_of_pos = []
        if self.name != None:
            with open(self.name, 'r', encoding='utf-8') as file:
                self.data = file.readlines()
        # sample = sample.strip()
        len_s = len(sample)
        if fin_line == -1:
            fin_line = len(self.data)

        if sample2 == None:
            for j in range(start_line,fin_line):
                if self.data[j].find(sample) != -1 and self.data[j][0] != self.commentary:
                    i = 0
                    while i <= len(self.data[j]) - len_s:
                        if self.data[j].find(sample, i) != -1:
                            x1 = self.data[j].find(sample, i)
                            x2 = x1 + len_s
                            list_of_pos.append([j, x1, x2])
                            i = x2
                        else:
                            break

        else:
            len_s2 = len(sample2)
            for j in range(start_line,fin_line):
                if self.data[j].find(sample) != -1 and self.data[j].find(sample2) != -1 and self.data[j][0] != self.commentary:
                    i = 0
                    while i <= len(self.data[j]) - len_s - len_s2:
                        if self.data[j].find(sample, i) != -1 and self.data[j].find(sample2, i+len_s) != -1:
                            x1 = self.data[j].find(sample, i) + len_s
                            x2 = self.data[j].find(sample2, i+len_s)
                            list_of_pos.append([j, x1, x2])
                            i = x2 + len_s2
                        else:
                            break
        # if len(list_of_pos) == 0:
        #     return None
        return list_of_pos
# D = DataParser('C:/Users/Администратор/Documents/GitHub/ProtoPacer/PacerData.txt')
# print(D.where_is_it("((", "))"))

    def is_unique(self, sample, sample2=None, start_line=0, fin_line=-1):
        """|
           * Метод "уникально_ли_это" выясняет, является ли вхождение указанного образца (или пары образцов)
           единственным таковым между строками start_line и fin_line.
        """
        if len(self.where_is_it(sample, sample2, start_line, fin_line)) == 1:
            return True
        else:
            return False


    def grab_it_there(self, coords):
        """|
           * Метод "взять_там" возвращает строку (или список строк), находящуюся в обрабатываемом файле
             в указанном месте. координаты должны быть в формате [y, x1, x2], где
             y - номер строки, x1 - позиция первого символа, x2 - позиция символа за последним.
             Или в формате [y1, y2], где
             y1 - номер первой интересующей строки, а y2 - номер строки за последней.
             Нумерация с нуля.
        """
        if self.name != None:
            with open(self.name, 'r', encoding='utf-8') as file:
                self.data = file.readlines()

        if len(coords) == 3:
            y, x1, x2 = coords
            if x2 == -1:
                return self.data[y][x1:]
            else:
                return self.data[y][x1:x2]

        elif len(coords) == 2:
            y1, y2 = coords
            if y1 >= y2:
                raise ValueError ("incorrect range")

            if y2 - y1 == 1:
                return self.data[y1][0]
            else:
                return self.data[y1:y2]

        else:
            raise ValueError ("incorrect range")


    def section_to_dic(self, start_line=0, fin_line=-1, delimiter="="):
        """|
           * Метод принимает начальную и конечную строки (номерами или значениями), между которыми построчно
             находит все пары значений, разделённые разделителем delimiter, и возвращает словарь с ними.
             Нумерация строк с нуля.
        """
        if 'str' in str(type(start_line)):
            if not self.is_unique(start_line):
                raise ValueError ("there is no start_line in data_source or it occurs more than once")
            start_line = self.where_is_it(start_line)[0][0]
        if 'str' in str(type(fin_line)):
            if not self.is_unique(fin_line):
                raise ValueError("there is no fin_line in data_source or it occurs more than once")
            fin_line = self.where_is_it(fin_line)[0][0]

        if start_line >= fin_line:
            raise ValueError("incorrect range")

        if self.name != None:
            with open(self.name, 'r', encoding='utf-8') as file:
                self.data = file.readlines()

        entries = self.where_is_it(delimiter, start_line=start_line, fin_line=fin_line)
        dic = {}
        for j in range(len(entries)):
            dic[self.grab_it_there(SOL_to_coords(entries[j]))] = self.grab_it_there(coords_to_EOL(entries[j]))[:-1]
        return dic



"""
Ещё мне нужно, чтобы dataparser умел...

    Принимать диапазон строк и возвращать из него две колонки значений, 
        разделённые известным ему разделителем, в виде словаря.
        
    Проверять уникальность записи в файле. 



"""