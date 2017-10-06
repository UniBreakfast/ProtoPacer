# Класс простейшего парсера текста: одна строка


def o_comb_regns(regns_x_x, str_len=None):
    for i in range(len(regns_x_x)):
        if type(regns_x_x[i]) is not int and type(regns_x_x[i]) is not list:
            raise TypeError ("regns_x_x[" + str(i) +"] must be int type or list of int and not " + str(type(regns_x_x[i])))
        elif type(regns_x_x[i]) is int:
            regns_x_x[i] = [regns_x_x[i]]
        else:
            for j in range(len(regns_x_x[i])):
                if type(regns_x_x[i][j]) is not int:
                    raise TypeError("regns_x_x[" + str(i) + "][" + str(j) + "] must be int type and not " + str(
                        type(regns_x_x[i][j])))
    for j in range(len(regns_x_x)):
        for i in range(len(regns_x_x) - 1):
            if regns_x_x[i][-1] + 1 >= regns_x_x[i + 1][0]:
                if regns_x_x[i][-1] < regns_x_x[i + 1][-1]:
                    regns_x_x[i][-1] = regns_x_x[i + 1][-1]
                    del regns_x_x[i + 1]
                    break
                else:
                    del regns_x_x[i + 1]
                    break
    if str_len != None:
        for i in range(len(regns_x_x)):
            if regns_x_x[i][0]>=str_len:
                del regns_x_x[i:]
                break
            elif regns_x_x[i][-1]>=str_len:
                regns_x_x[i][-1]= str_len - 1
    return regns_x_x

def o_inv_regns(regns_x_x, str_len):
    if len(regns_x_x) == 0:
        return [[0, str_len-1]]
    regns_x_x = o_comb_regns(regns_x_x)
    inv_regions_x_x = []
    if regns_x_x[0][0] > 0:
        inv_regions_x_x.append([0, regns_x_x[0][0] - 1])
    for i in range(len(regns_x_x)-1):
        inv_regions_x_x.append([regns_x_x[i][-1] + 1, regns_x_x[i + 1][0] - 1])
    if regns_x_x[-1][-1] + 1 < str_len:
        inv_regions_x_x.append([regns_x_x[-1][-1] + 1, str_len - 1])
    return inv_regions_x_x

def o_incr_list_of_pos(a_list, num):
    for i in range(len(a_list)):
        if type(a_list[i]) is int:
            a_list[i] += num
        elif type(a_list[i]) is list:
            o_incr_list_of_pos(a_list[i], num)




class ParseLine:

    def __init__(self, line_of_text):
        self.data = line_of_text


  ### def regions_form
  ###            _combine
  ###            _invert
  ###            _shift
  ### def find_substring    (char, string, all or certain occurance by number)
  ###         _pairs        (certain pair by number, all pairs, bulk)
  ### def read_by_pos   (from, till, from-till)
  ###         _after    (certain occurance of substring by number)
  ###         _before
  ###         _between      (certain pair by number, all pairs)
  ###         _around       (certain occurance of delimiter by number, all delimiters)
  ### def count_substrings  (number of occurances)
  ###          _pairs
  ### def check_occurance       (it is there - True, False)
  ###          _pair_empty      (certain pair is empty - True, False)
  ### def del_by_pos    (from, till, from-till)
    #        _substring
    #        _after     (certain occurance of substring by number)
    #        _before
    #        _between      (certain pair by number, pairs)
    # def ins_at_pos
    #        _after     (certain occurance of substring by number)
    #        _before
    #        _inside_pair   (all or certain occurance by number)
    # def write_at_pos  (over previous)
    #          _after   (certain occurance of substring by number)
    #          _before
    # def replace_substring   (char, string, all or certain occurance by number)
    #            _all_after
    #            _all_before
    #            _after_delim   (certain delim by number)
    #            _before_delim
    #            _inside_pair   (all or certain occurance by number)

    def regions_form(self, *regions):
        regions = [*regions]
        if regions == [None]: return

        min_depth = 4; max_depth = 0
        for i in range(len(regions)):
            if type(regions[i]) is list:
                max_depth = 1 if max_depth < 1 else max_depth
                for j in range(len(regions[i])):
                    if type(regions[i][j]) is list:
                        max_depth = 2 if max_depth < 2 else max_depth
                        for k in range(len(regions[i][j])):
                            if type(regions[i][j][k]) is list:
                                max_depth = 3 if max_depth < 3 else max_depth
                                for l in range(len(regions[i][j][k])):
                                    if type(regions[i][j][k][l]) is not int or l>1:
                                        raise TypeError("incorrect region")
                                    else: min_depth = 3 if min_depth > 3 else min_depth
                            elif type(regions[i][j][k]) is not int or k>1:
                                raise TypeError("incorrect region")
                            else: min_depth = 2 if min_depth > 2 else min_depth
                    elif type(regions[i][j]) is not int:
                        raise TypeError("incorrect region")
                    else: min_depth = 1 if min_depth > 1 else min_depth
            elif type(regions[i]) is not int:
                raise TypeError("incorrect region")
            else: min_depth = 0 if min_depth > 0 else min_depth

        if max_depth == 1 and len(regions[0]) == 2:
            return regions
        elif min_depth == max_depth == 3 and len(regions[0][0]) == 2:
            for i in range(len(regions[0])):
                if len(regions[0][i]) != 2 or len(regions[0][i][0]) != 2 or len(regions[0][i][1]) != 2:
                    raise TypeError("incorrect region")
                regions[0][i][0] = regions[0][i][0][-1]
                regions[0][i][1] = regions[0][i][-1][0]
            return regions[0]

        elif min_depth == 2 and len(regions) == 1:
            regions = regions[0]

        elif min_depth == 3 and len(regions) == 1 and len(regions[0]) == 1 and len(regions[0][0]) != 1:
            regions = regions[0][0]

        else:
            formed = []
            for i in range(len(regions)):
                if type(regions[i]) is int:
                    formed.append([regions[i], regions[i] + 1])
                else:
                    if len(regions[i]) == 1:
                        for j in range(len(regions[i])):
                            if type(regions[i][j]) is int:
                                formed.append([regions[i][j], regions[i][j] + 1])
                    else:
                        for j in range(len(regions[i])):
                            formed.append([regions[i][j][0], regions[i][j][1]])
            return formed

        return regions

    def regions_combine(self, *regions):
        regions = self.regions_form(*regions)
        if regions == None: return
        regions.sort()
        for j in range(len(regions)-1):
            for i in range(len(regions)-1):
                if regions[i][-1] >= regions[i+1][0]:
                    if regions[i][-1] < regions[i+1][-1]:
                        regions[i][-1] = regions[i + 1][-1]
                        del regions[i + 1]
                        break
                    else:
                        del regions[i + 1]
                        break
        if len(self.data) != 0:
            for i in range(len(regions)):
                if regions[i][0] >= len(self.data):
                    del regions[i:]
                    break
                elif regions[i][-1] > len(self.data):
                    regions[i][-1] = len(self.data)
        return regions

    def regions_invert(self, *regions):
        regions = self.regions_combine(*regions)
        if regions is None: return
        if len(regions) == 0:
            return [0, len(self.data)]
        inv_regions = []
        if regions[0][0] > 0:
            inv_regions.append([0, regions[0][0]])
        for i in range(len(regions) - 1):
            inv_regions.append([regions[i][-1], regions[i + 1][0]])
        if regions[-1][-1] < len(self.data):
            inv_regions.append([regions[-1][-1], len(self.data)])
        return inv_regions

    def regions_shift(self, regions, shift):
        for i in range(len(regions)):
            if type(regions[i]) is list:
                for j in range(len(regions[i])):
                    if type(regions[i][j]) is list:
                        for k in range(len(regions[i][j])):
                            if type(regions[i][j][k]) is list:
                                for l in range(len(regions[i][j][k])):
                                    if type(regions[i][j][k][l]) is int:
                                        if l == 0 or len(regions[i][j][k]) != 2: regions[i][j][k][l] += shift[0]
                                        else: regions[i][j][k][l] += shift[-1]
                            elif type(regions[i][j][k]) is int:
                                if k == 0 or len(regions[i][j]) != 2: regions[i][j][k] += shift[0]
                                else: regions[i][j][k] += shift[-1]
                    elif type(regions[i][j]) is int:
                        if j == 0 or len(regions[i]) != 2: regions[i][j] += shift[0]
                        else: regions[i][j] += shift[-1]
            elif type(regions[i]) is int:
                if i == 0 or len(regions) != 2: regions[i] += shift[0]
                else: regions[i] += shift[-1]
        return regions



    def find_substrings(self, sub, num=None):

        if num is None:
            xe = 0; seq_pos = []
            while True:
                xb = self.data.find(sub, xe)
                if xb == -1: break
                xe = xb + len(sub)
                seq_pos.append([xb, xe])
            if len(seq_pos) == 0: seq_pos = None

        elif num >= 0:
            xe = 0
            for n in range(num+1):
                xb = self.data.find(sub, xe)
                if xb == -1: break
                xe = xb + len(sub)
            seq_pos = [[xb, xe]] if xb != -1 else None

        elif num < 0:
            xb = len(self.data)
            for n in range(abs(num)):
                xb = self.data.rfind(sub, 0, xb)
                if xb == -1: break
                xe = xb + len(sub)
            seq_pos = [[xb, xe]] if xb != -1 else None

        return seq_pos

    def find_pairs(self, sub1, sub2, num=None):

        if num is None:
            x2e = step = 0; pair_pos = []
            while True:
                x2b = self.data.find(sub2, x2e)
                if x2b == -1: break
                x2e = x2b + len(sub2)
                x1b = self.data.rfind(sub1, step, x2b)
                if x1b == -1: continue
                x1e = x1b + len(sub1)
                pair_pos.append([[x1b, x1e], [x2b, x2e]])
                step = x2e
            if len(pair_pos) == 0: pair_pos = None

        elif num >= 0:
            x2e = step = 0; n = 0; pair_pos = []
            while n < num+1:
                x2b = self.data.find(sub2, x2e)
                if x2b == -1: break
                x2e = x2b + len(sub2)
                x1b = self.data.rfind(sub1, step, x2b)
                if x1b == -1: continue
                x1e = x1b + len(sub1)
                pair_pos=[[[x1b, x1e], [x2b, x2e]]]
                step = x2e
                n += 1
            pair_pos = [[[x1b, x1e], [x2b, x2e]]] if x2b != -1 else None


        elif num < 0:
            step = x1b = len(self.data); n = 0; pair_pos = []
            while n > num:
                x1b = self.data.rfind(sub1, 0, x1b)
                if x1b == -1: break
                x1e = x1b + len(sub1)
                x2b = self.data.find(sub2, x1e, step)
                if x2b == -1: continue
                x2e = x2b + len(sub2)
                pair_pos=[[[x1b, x1e], [x2b, x2e]]]
                step = x1b
                n -= 1
            pair_pos = [[[x1b, x1e], [x2b, x2e]]] if x1b != -1 else None

        return pair_pos



    def read_by_pos(self, pos):
        if type(pos[0]) is int:
            return self.data[pos[0]:pos[-1]]
        else:
            return [self.read_by_pos(j) for i,j in enumerate(pos)]

    def read_after(self, sub, num=0):
        pos = self.find_substrings(sub, num)
        if not pos is None:
            return self.data[pos[-1][-1]:]

    def read_before(self, sub, num=0):
        pos = self.find_substrings(sub, num)
        if not pos is None:
            return self.data[:pos[0][0]]

    def read_between_pairs(self, sub1, sub2, num=None):
        pos = self.find_pairs(sub1, sub2, num)
        if not pos is None:
            return [self.read_by_pos([j[0][-1], j[-1][0]]) for i,j in enumerate(pos)]

    def read_around(self, delim, num=None):
        pos = self.find_substrings(delim, num)
        pos = self.regions_invert(pos)
        if not pos is None:
            return self.read_by_pos(pos)



    def count_substrings(self, sub):
        pos = self.find_substrings(sub)
        if not pos is None:
            return len(pos)

    def count_pairs(self, sub1, sub2):
        pos = self.find_pairs(sub1, sub2)
        if not pos is None:
            return len(pos)



    def check_occurance(self, sub, pos):
        if type(pos) is not list: pos = [pos]
        return self.data.startswith(sub, pos[0])

    def check_pair_empty(self, sub1, sub2, num=None):
        if not num is None:
            pos = self.find_pairs(sub1, sub2, num)
            if not pos is None:
                return pos[0][0][-1] == pos[0][-1][0]
        else:
            pos = self.find_pairs(sub1, sub2, num)
            return [j[0][-1] == j[-1][0] for i,j in enumerate(pos)]



    def del_by_pos(self, pos, really=False):
        if really:
            try: self.data = self.data[:pos[0]] + self.data[pos[1]:]
            except: return None
            else: return "Done"
        elif not really:
            return self.data[:pos[0]] + self.data[pos[1]:]

    def del_substring (self, sub, num=None):
        pos = find_substrings(sub, num)



    # def o_comb_regns(self, regns_x_x):
    #     if len(regns_x_x) == 2 and type(regns_x_x[0]) is int and type(regns_x_x[1]) is int:
    #         regns_x_x = [regns_x_x]
    #
    #     for i in range(len(regns_x_x)):
    #         # if type(regns_x_x[i]) is not int and type(regns_x_x[i]) is not list:
    #         #     raise TypeError(
    #         #         "regns_x_x[" + str(i) + "] must be int type or list of int and not " + str(type(regns_x_x[i])))
    #         elif type(regns_x_x[i]) is int:
    #             regns_x_x[i] = [regns_x_x[i]]
    #         # else:
    #             # for j in range(len(regns_x_x[i])):
    #             #     if type(regns_x_x[i][j]) is not int:
    #             #         raise TypeError("regns_x_x[" + str(i) + "][" + str(j) + "] must be int type and not " + str(
    #             #             type(regns_x_x[i][j])))
    #     for j in range(len(regns_x_x)):
    #         for i in range(len(regns_x_x) - 1):
    #             if regns_x_x[i][-1] + 1 >= regns_x_x[i + 1][0]:
    #                 if regns_x_x[i][-1] < regns_x_x[i + 1][-1]:
    #                     regns_x_x[i][-1] = regns_x_x[i + 1][-1]
    #                     del regns_x_x[i + 1]
    #                     break
    #                 else:
    #                     del regns_x_x[i + 1]
    #                     break
    #     if len(self.data) != 0:
    #         for i in range(len(regns_x_x)):
    #             if regns_x_x[i][0] >= len(self.data):
    #                 del regns_x_x[i:]
    #                 break
    #             elif regns_x_x[i][-1] >= len(self.data):
    #                 regns_x_x[i][-1] = len(self.data) - 1
    #     return regns_x_x

    def o_inv_regns(self, regns_x_x):
        if len(regns_x_x) == 0:
            return [[0, len(self.data) - 1]]
        regns_x_x = self.o_comb_regns(regns_x_x)
        inv_regions_x_x = []
        if regns_x_x[0][0] > 0:
            inv_regions_x_x.append([0, regns_x_x[0][0] - 1])
        for i in range(len(regns_x_x) - 1):
            inv_regions_x_x.append([regns_x_x[i][-1] + 1, regns_x_x[i + 1][0] - 1])
        if regns_x_x[-1][-1] + 1 < len(self.data):
            inv_regions_x_x.append([regns_x_x[-1][-1] + 1, len(self.data) - 1])
        return inv_regions_x_x



    # def o_find_pos_x_of_chr(self, chr):
    #     if type(chr) is not str:
    #         raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
    #     elif len(chr) != 1:
    #         raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
    #     else:
    #         chr_pos_x = self.data.find(chr)
    #     if chr_pos_x == -1:
    #         return None
    #     else:
    #         return chr_pos_x

    def o_find_pos_x_of_chrs(self, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            chr_pos_x = self.data.find(chr)
            if chr_pos_x == -1:
                return None
            else:
                chrs_pos_x = []
                while chr_pos_x != -1:
                    chrs_pos_x.append(chr_pos_x)
                    chr_pos_x = self.data.find(chr, chr_pos_x + 1)
                return chrs_pos_x

    def o_find_pos_x_of_chrs_bulk(self, chrs_list):
        if type(chrs_list) is not list:
            raise TypeError ("chrs_list must be list type and not " + str(type(chr)))
        elif len(chrs_list) == 0:
            raise ValueError ("chrs_list must contain at least 1 item")
        else:
            chrs_pos_x = []
            for i in range(len(chrs_list)):
                if type(chrs_list[i]) is not str:
                    raise TypeError ("chrs_list[" + str(i) +"] (characters) must be string type and not " + str(type(chrs_list[i])))
                elif len(chrs_list[i]) != 1:
                    raise ValueError ("chrs_list[" + str(i) +"] (characters) must be a string 1 char long and not " + str(len(chrs_list[i])))
                else:
                    chrs_i_pos_x = self.o_find_pos_x_of_chrs(chrs_list[i])
                    if chrs_i_pos_x != None:
                        chrs_pos_x += chrs_i_pos_x
            chrs_pos_x.sort()
            return chrs_pos_x

    # def o_find_pos_x_x_of_seq(self, seq):
    #     if type(seq) is not str:
    #         raise TypeError ("seq (sequence) must be string type and not " + str(type(seq)))
    #     elif len(seq) == 0:
    #         raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
    #     else:
    #     seq_pos_x_first = self.data.find(seq)
    #     if seq_pos_x_first == -1:
    #         return None
    #     else:
    #         seq_pos_x_last = seq_pos_x_first + len(seq) - 1
    #         return [seq_pos_x_first, seq_pos_x_last]

    def o_find_pos_x_x_of_seqs(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not " + str(type(seq)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            seq_pos_x_first = self.data.find(seq)
            if seq_pos_x_first == -1:
                return None
            else:
                seqs_pos_x_x = []
                while seq_pos_x_first != -1:
                    seq_pos_x_last = seq_pos_x_first + len(seq) - 1
                    seqs_pos_x_x.append([seq_pos_x_first, seq_pos_x_last])
                    seq_pos_x_first = self.data.find(seq, seq_pos_x_last + 1)
                return seqs_pos_x_x

    # def o_find_pos_x_x_of_seqs_bulk(self, seqs_list):
    #     if type(seqs_list) is not list:
    #         raise TypeError ("seqs_list must be list type and not " + str(type(chr)))
    #     elif len(seqs_list) == 0:
    #         raise ValueError ("seqs_list must contain at least 1 item")
    #     else:
    #     seqs_pos_x = []
    #     for i in range(len(seqs_list)):
    #         if type(seqs_list[i]) is not str:
    #             raise TypeError ("seqs_list[" + str(i) +"] (sequences) must be string type and not " + str(type(seqs_list[i])))
    #         elif len(seqs_list[i]) == 0:
    #             raise ValueError ("seqs_list[" + str(i) +"] (sequences) must be a string at least 1 char long and not 0")
    #         else:
    #         seqs_i_pos_x_x = self.o_find_pos_x_x_of_seqs(seqs_list[i])
    #         if seqs_i_pos_x_x != None:
    #             seqs_pos_x += seqs_i_pos_x_x
    #     seqs_pos_x.sort()
    #     return seqs_pos_x

    def o_find_pos_x_x_of_pairs_chr1_chr2(self, chr1, chr2):
        if type(chr1) is not str:
            raise TypeError("chr1 (character) must be string type and not " + str(type(chr1)))
        elif len(chr1) != 1:
            raise ValueError("chr1 (character) must be a string 1 char long and not " + str(len(chr1)))
        elif type(chr2) is not str:
            raise TypeError("chr2 (character) must be string type and not " + str(type(chr2)))
        elif len(chr2) != 1:
            raise ValueError("chr2 (character) must be a string 1 char long and not " + str(len(chr2)))
        elif chr1 == chr2:
            raise ValueError("chr1 and chr2 must be to different characters")
        else:
            chrs1_pos_x = self.o_find_pos_x_of_chrs(chr1)
            chrs2_pos_x = self.o_find_pos_x_of_chrs(chr2)
            if chrs1_pos_x == None and chrs2_pos_x == None:
                raise ValueError("there is neither chr1 (character) nor chr2 in the string")
            elif chrs1_pos_x == None:
                raise ValueError("there is no chr1 (character) in the string")
            elif chrs2_pos_x == None:
                raise ValueError("there is no chr2 (character) in the string")
            else:
                pairs_pos = []
                pairs_pos_r = []
                for i in range(len(chrs1_pos_x)):
                    pair = [chrs1_pos_x[0], chrs2_pos_x[-1]+1]
                    for j in range(len(chrs2_pos_x)):
                        if chrs1_pos_x[i] < chrs2_pos_x[j] and chrs2_pos_x[j]-chrs1_pos_x[i] < pair[1]-pair[0]:
                            pair = [chrs1_pos_x[i], chrs2_pos_x[j]]
                    if pair[1] - pair[0] < chrs2_pos_x[-1]+1 - chrs1_pos_x[0]:
                        pairs_pos_r.append(pair)
                pairs_pos_l = []
                for j in range(len(chrs2_pos_x)):
                    pair = [chrs1_pos_x[0], chrs2_pos_x[-1]+1]
                    for i in range(len(chrs1_pos_x)):
                        if chrs1_pos_x[i] < chrs2_pos_x[j] and chrs2_pos_x[j]-chrs1_pos_x[i] < pair[1]-pair[0]:
                            pair = [chrs1_pos_x[i], chrs2_pos_x[j]]
                    if pair[1] - pair[0] < chrs2_pos_x[-1]+1 - chrs1_pos_x[0]:
                        pairs_pos_l.append(pair)
                for k in range(len(pairs_pos_r)):
                    if pairs_pos_r[k] in pairs_pos_l:
                        pairs_pos.append(pairs_pos_r[k])
                if len(pairs_pos) == 0:
                    return None
                else:
                    return pairs_pos

    def o_find_pos_x_x_of_pairs_seq1_seq2(self, seq1, seq2):
        if type(seq1) is not str:
            raise TypeError("seq1 (sequence) must be string type and not " + str(type(seq1)))
        elif len(seq1) == 0:
            raise ValueError("seq1 (sequence) must be a string at least 1 char long and not 0")
        elif type(seq2) is not str:
            raise TypeError("seq2 (sequence) must be string type and not " + str(type(seq2)))
        elif len(seq2) == 0:
            raise ValueError("seq1 (sequence) must be a string at least 1 char long and not 0")
        elif seq1 == seq2:
            raise ValueError("seq1 and seq2 must be to different sequences")
        else:
            seqs1_pos_x_x = self.o_find_pos_x_x_of_seqs(seq1)
            seqs2_pos_x_x = self.o_find_pos_x_x_of_seqs(seq2)
            if seqs1_pos_x_x == None and seqs2_pos_x_x == None:
                raise ValueError("there is neither seq1 (sequence) nor seq2 in the string")
            elif seqs1_pos_x_x == None:
                raise ValueError("there is no seq1 (sequence) in the string")
            elif seqs2_pos_x_x == None:
                raise ValueError("there is no seq2 (sequence) in the string")
            else:
                pairs_pos_x_x = []
                pairs_pos_r = []
                for i in range(len(seqs1_pos_x_x)):
                    pair = [seqs1_pos_x_x[0], [seqs2_pos_x_x[-1][0]+1, seqs2_pos_x_x[-1][-1]+1]]
                    for j in range(len(seqs2_pos_x_x)):
                        if seqs1_pos_x_x[i][-1] < seqs2_pos_x_x[j][0] and seqs2_pos_x_x[j][0]-seqs1_pos_x_x[i][-1] < pair[1][0]-pair[0][-1]:
                            pair = [seqs1_pos_x_x[i], seqs2_pos_x_x[j]]
                    if pair[1][0]-pair[0][-1] < seqs2_pos_x_x[-1][0]+1 - seqs1_pos_x_x[0][-1]:
                        pairs_pos_r.append(pair)
                pairs_pos_l = []
                for j in range(len(seqs2_pos_x_x)):
                    pair = [seqs1_pos_x_x[0], [seqs2_pos_x_x[-1][0]+1, seqs2_pos_x_x[-1][-1]+1]]
                    for i in range(len(seqs1_pos_x_x)):
                        if seqs1_pos_x_x[i][-1] < seqs2_pos_x_x[j][0] and seqs2_pos_x_x[j][0]-seqs1_pos_x_x[i][-1] < pair[1][0]-pair[0][-1]:
                            pair = [seqs1_pos_x_x[i], seqs2_pos_x_x[j]]
                    if pair[1][0]-pair[0][-1] < seqs2_pos_x_x[-1][0]+1 - seqs1_pos_x_x[0][-1]:
                        pairs_pos_l.append(pair)
                for k in range(len(pairs_pos_r)):
                    if pairs_pos_r[k] in pairs_pos_l:
                        pairs_pos_x_x.append(pairs_pos_r[k])
                if len(pairs_pos_x_x) == 0:
                    return None
                else:
                    return pairs_pos_x_x



    def o_read_chr_at_pos_x(self, pos_x):
        if type(pos_x) is not int:
            raise TypeError ("pos_x (position in line) must be int type and not " + str(type(pos_x)))
        elif pos_x >= len(self.data):
            raise IndexError ("there is no such position to look, max is " + str(len(self.data)-1) +" and not " + str(pos_x))
        elif pos_x <= -len(self.data)-1:
            raise IndexError ("there is no such position to look, min is " + str(-len(self.data)) +" and not " + str(pos_x))
        else:
            return self.data[pos_x]



    def o_chr_at_pos_x(self, chr, pos_x):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be string 1 chr long and not " + str(len(chr)))
        elif type(pos_x) is not int:
            raise TypeError ("pos_x (position in line) must be int type and not " + str(type(pos_x)))
        elif pos_x >= len(self.data):
            raise IndexError ("there is no such position to look, max is " + str(len(self.data)-1) +" and not " + str(pos_x))
        elif pos_x <= -len(self.data) - 1:
            raise IndexError ("there is no such position to look, min is " + str(-len(self.data)) + " and not " + str(pos_x))
        else:
            return self.o_read_chr_at_pos_x(pos_x) == chr

    def o_seq_on_pos_x_x(self, seq, pos_x_first, pos_x_last):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not " + str(type(seq)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            return self.o_read_seq_on_pos_x_x(pos_x_first, pos_x_last) == seq



    def o_read_chr2_aft_chr1(self, chr1):
        if type(chr1) is not str:
            raise TypeError ("chr1 (character) must be string type and not " + str(type(chr1)))
        elif len(chr1) != 1:
            raise ValueError ("chr1 (character) must be a string 1 char long and not " + str(len(chr1)))
        else:
            chr1_pos_x = self.data.find(chr1)
            if chr1_pos_x == -1:
                raise ValueError ("there is no such chr1 (character) in the string")
            elif chr1_pos_x + 1 == len(self.data):
                return None
            else:
                chr2_pos_x = chr1_pos_x + 1
                return self.o_read_chr_at_pos_x(chr2_pos_x)

    def o_read_chrs2_aft_chrs1(self, chr1):
        if type(chr1) is not str:
            raise TypeError ("chr1 (character) must be string type and not " + str(type(chr1)))
        elif len(chr1) != 1:
            raise ValueError ("chr1 (character) must be a string 1 char long and not " + str(len(chr1)))
        else:
            chrs1_pos_x = self.o_find_pos_x_of_chrs(chr1)
            if chrs1_pos_x == None:
                raise ValueError ("there is no such chr1 (character) in the string")
            elif chrs1_pos_x[0] + 1 == len(self.data):
                return None
            else:
                chrs2=[]
                for i in range(len(chrs1_pos_x)):
                    if chrs1_pos_x[i] + 1 != len(self.data):
                        chrs2.append(self.o_read_chr_at_pos_x(chrs1_pos_x[i] + 1))
                return chrs2

    def o_read_chr_aft_seq(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not "+str(type(symbol)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            seq_pos_x_x = self.o_find_pos_x_x_of_seq(seq)
            if seq_pos_x_x == None:
                raise ValueError ("there is no such seq (sequence) in the string")
            elif seq_pos_x_x[1] + 1 == len(self.data):
                return None
            else:
                chr_pos_x = seq_pos_x_x[1] + 1
                return self.o_read_chr_at_pos_x(chr_pos_x)

    def o_read_chrs_aft_seqs(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not "+str(type(symbol)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            seqs_pos_x_x = self.o_find_pos_x_x_of_seqs(seq)
            if seqs_pos_x_x == None:
                raise ValueError ("there is no such seq (sequence) in the string")
            elif seqs_pos_x_x[0][1] + 1 == len(self.data):
                return None
            else:
                chrs=[]
                for i in range(len(seqs_pos_x_x)):
                    if seqs_pos_x_x[i][1] + 1 != len(self.data):
                        chrs.append(self.o_read_chr_at_pos_x(seqs_pos_x_x[i][1] + 1))
                return chrs



    def o_read_chr0_bef_chr1(self, chr1):
        if type(chr1) is not str:
            raise TypeError("chr1 (character) must be string type and not " + str(type(chr1)))
        elif len(chr1) != 1:
            raise ValueError("chr1 (character) must be a string 1 char long and not " + str(len(chr1)))
        else:
            chr1_pos_x = self.o_find_pos_x_of_chr(chr1)
            if chr1_pos_x == None:
                raise ValueError("there is no such chr1 (character) in the string")
            elif chr1_pos_x == 0:
                return None
            else:
                chr0_pos_x = chr1_pos_x - 1
                return self.o_read_chr_at_pos_x(chr0_pos_x)

    def o_read_chrs0_bef_chrs1(self, chr1):
        if type(chr1) is not str:
            raise TypeError("chr1 (character) must be string type and not " + str(type(chr1)))
        elif len(chr1) != 1:
            raise ValueError("chr1 (character) must be a string 1 char long and not " + str(len(chr1)))
        else:
            chrs1_pos_x = self.o_find_pos_x_of_chrs(chr1)
            if chrs1_pos_x == None:
                raise ValueError("there is no such chr1 (character) in the string")
            elif chrs1_pos_x[-1] == 0:
                return None
            else:
                chrs0 = []
                for i in range(len(chrs1_pos_x)):
                    if chrs1_pos_x[i] != 0:
                        chrs0.append(self.o_read_chr_at_pos_x(chrs1_pos_x[i] - 1))
                return chrs0

    def o_read_chr_bef_seq(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not "+str(type(symbol)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            seq_pos_x_x = self.o_find_pos_x_x_of_seq(seq)
            if seq_pos_x_x == None:
                raise ValueError ("there is no such seq (sequence) in the string")
            elif seq_pos_x_x[0] == 0:
                return None
            else:
                return self.o_read_chr_at_pos_x(seq_pos_x_x[0] - 1)

    def o_read_chrs_bef_seqs(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not "+str(type(symbol)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            seqs_pos_x_x = self.o_find_pos_x_x_of_seqs(seq)
            if seqs_pos_x_x == None:
                raise ValueError ("there is no such seq (sequence) in the string")
            elif seqs_pos_x_x[-1][0] == 0:
                return None
            else:
                chrs=[]
                for i in range(len(seqs_pos_x_x)):
                    if seqs_pos_x_x[i][0] != 0:
                        chrs.append(self.o_read_chr_at_pos_x(seqs_pos_x_x[i][0] - 1))
                return chrs



    def o_read_seq_aft_chr(self, chr, seq_len):
        if seq_len == 1:
            return self.o_read_chr2_aft_chr1(chr)
        elif type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        elif type(seq_len) is not int:
            raise TypeError ("seq_len (sequence length) must be int type and not " + str(type(seq_len)))
        elif seq_len <= 0:
            raise ValueError ("seq_len (sequence length) must be positive")
        else:
            chr_pos_x = self.data.find(chr)
            if chr_pos_x == -1:
                raise ValueError ("there is no such chr (character) in the string")
            elif chr_pos_x + seq_len >= len(self.data):
                raise IndexError ("there is only " + str(len(self.data)-chr_pos_x-1) +" characters after " + chr + " and not " + str(seq_len))
            else:
                return self.o_read_seq_on_pos_x_x(chr_pos_x + 1, chr_pos_x + seq_len)

    def o_read_seqs_aft_chrs(self, chr, seqs_len):
        if seqs_len == 1:
            return self.o_read_chrs2_aft_chrs1(chr)
        elif type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        elif type(seqs_len) is not int:
            raise TypeError ("seqs_len (sequence length) must be int type and not " + str(type(seqs_len)))
        elif seqs_len <= 0:
            raise ValueError ("seqs_len (sequence length) must be positive")
        else:
            chrs_pos_x = self.o_find_pos_x_of_chrs(chr)
            if chrs_pos_x == None:
                raise ValueError ("there is no such chr (character) in the string")
            elif chrs_pos_x[0] + seqs_len >= len(self.data):
                raise IndexError ("there is maximum " + str(len(self.data)-chrs_pos_x[0]-1) +" characters after " + chr + " and not " + str(seqs_len))
            else:
                seqs=[]
                for i in range(len(chrs_pos_x)):
                    if chrs_pos_x[i] + seqs_len < len(self.data):
                        seqs.append(self.o_read_seq_on_pos_x_x(chrs_pos_x[i] + 1, chrs_pos_x[i] + seqs_len))
                    else:
                        seqs.append(self.o_read_all_from_pos_x(chrs_pos_x[i] + 1))
                return seqs

    def o_read_seq2_aft_seq1(self, seq1, seq2_len):
        if seq2_len == 1:
            return self.o_read_chr_aft_seq(seq1)
        elif type(seq1) is not str:
            raise TypeError ("seq1 (sequence) must be string type and not " + str(type(seq1)))
        elif len(seq1) == 0:
            raise ValueError ("seq1 (sequence) must be a string at least 1 char long and not 0")
        elif type(seq2_len) is not int:
            raise TypeError ("seq2_len (sequence length) must be int type and not " + str(type(seq2_len)))
        elif seq2_len <= 0:
            raise ValueError ("seq2_len (sequence length) must be positive")
        else:
            seq1_pos_x_x = self.o_find_pos_x_x_of_seq(seq1)
            if seq1_pos_x_x == None:
                raise ValueError ("there is no such seq1 (sequence) in the string")
            elif seq1_pos_x_x[1] + seq2_len >= len(self.data):
                raise IndexError ("there is only " + str(len(self.data)-seq1_pos_x_x[1]-1) +" characters after " + seq1 + " and not " + str(seq2_len))
            else:
                return self.o_read_seq_on_pos_x_x(seq1_pos_x_x[1] + 1, seq1_pos_x_x[1] + seq2_len)

    def o_read_seqs2_aft_seqs1(self, seq1, seqs2_len):
        if seqs2_len == 1:
            return self.o_read_chrs_aft_seqs(seq1)
        elif type(seq1) is not str:
            raise TypeError ("seq1 (sequence) must be string type and not " + str(type(seq1)))
        elif len(seq1) == 0:
            raise ValueError ("seq1 (sequence) must be a string at least 1 char long and not 0")
        elif type(seqs2_len) is not int:
            raise TypeError ("seqs2_len (sequence length) must be int type and not " + str(type(seqs2_len)))
        elif seqs2_len <= 0:
            raise ValueError ("seqs2_len (sequence length) must be positive")
        else:
            seqs1_pos_x_x = self.o_find_pos_x_x_of_seqs(seq1)
            if seqs1_pos_x_x == None:
                raise ValueError ("there is no such seq1 (sequence) in the string")
            elif seqs1_pos_x_x[0][1] + seqs2_len >= len(self.data):
                raise IndexError ("there is maximum " + str(len(self.data)-seqs1_pos_x_x[0][1]-1) +" characters after " + seq1 + " and not " + str(seqs2_len))
            else:
                seqs2=[]
                for i in range(len(seqs1_pos_x_x)):
                    if seqs1_pos_x_x[i][1] + seqs2_len < len(self.data):
                        seqs2.append(self.o_read_seq_on_pos_x_x(seqs1_pos_x_x[i][1] + 1, seqs1_pos_x_x[i][1] + seqs2_len))
                    else:
                        seqs2.append(self.o_read_all_from_pos_x(seqs1_pos_x_x[i][1] + 1))
                return seqs2



    def o_read_seq_bef_chr(self, chr, seq_len):
        if seq_len == 1:
            return self.o_read_chr0_bef_chr1(chr)
        elif type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        elif type(seq_len) is not int:
            raise TypeError ("seq_len (sequence length) must be int type and not " + str(type(seq_len)))
        elif seq_len <= 0:
            raise ValueError ("seq_len (sequence length) must be positive")
        else:
            chr_pos_x = self.o_find_pos_x_of_chr(chr)
            if chr_pos_x == None:
                raise ValueError ("there is no such chr (character) in the string")
            elif chr_pos_x - seq_len < 0:
                raise IndexError ("there is only " + str(chr_pos_x) +" characters before " + chr + " and not " + str(seq_len))
            else:
                return self.o_read_seq_on_pos_x_x(chr_pos_x - seq_len, chr_pos_x - 1)

    def o_read_seqs_bef_chrs(self, chr, seqs_len):
        if seqs_len == 1:
            return self.o_read_chrs2_aft_chrs1(chr)
        elif type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        elif type(seqs_len) is not int:
            raise TypeError ("seqs_len (sequence length) must be int type and not " + str(type(seqs_len)))
        elif seqs_len <= 0:
            raise ValueError ("seqs_len (sequence length) must be positive")
        else:
            chrs_pos_x = self.o_find_pos_x_of_chrs(chr)
            if chrs_pos_x == None:
                raise ValueError ("there is no such chr (character) in the string")
            elif chrs_pos_x[-1] - seqs_len < 0:
                raise IndexError ("there is maximum " + str(chrs_pos_x[-1]) +" characters before " + chr + " and not " + str(seqs_len))
            else:
                seqs=[]
                for i in range(len(chrs_pos_x)):
                    if chrs_pos_x[i] - seqs_len > 0:
                        seqs.append(self.o_read_seq_on_pos_x_x(chrs_pos_x[i] - seqs_len, chrs_pos_x[i] - 1))
                    else:
                        seqs.append(self.o_read_all_up_to_incl_pos_x(chrs_pos_x[i] - 1))
                return seqs

    def o_read_seq0_bef_seq1(self, seq1, seq0_len):
        if seq0_len == 1:
            return self.o_read_chr_bef_seq(seq1)
        elif type(seq1) is not str:
            raise TypeError("seq1 (sequence) must be string type and not " + str(type(seq1)))
        elif len(seq1) == 0:
            raise ValueError("seq1 (sequence) must be a string at least 1 char long and not 0")
        elif type(seq0_len) is not int:
            raise TypeError("seq0_len (sequence length) must be int type and not " + str(type(seq0_len)))
        elif seq0_len <= 0:
            raise ValueError("seq0_len (sequence length) must be positive")
        else:
            seq1_pos_x_x = self.o_find_pos_x_x_of_seq(seq1)
            if seq1_pos_x_x == None:
                raise ValueError ("there is no such seq1 (sequence) in the string")
            elif seq1_pos_x_x[0] - seq0_len < 0:
                raise IndexError ("there is only " + str(seq1_pos_x_x[0]) +" characters before " + seq1 + " and not " + str(seq0_len))
            else:
                return self.o_read_seq_on_pos_x_x(seq1_pos_x_x[0] - seq0_len, seq1_pos_x_x[0] - 1)

    def o_read_seqs0_bef_seqs1(self, seq1, seqs0_len):
        if seqs0_len == 1:
            return self.o_read_chrs_bef_seqs(seq1)
        elif type(seq1) is not str:
            raise TypeError ("seq1 (sequence) must be string type and not " + str(type(seq1)))
        elif len(seq1) == 0:
            raise ValueError ("seq1 (sequence) must be a string at least 1 char long and not 0")
        elif type(seqs0_len) is not int:
            raise TypeError ("seqs0_len (sequence length) must be int type and not " + str(type(seqs0_len)))
        elif seqs0_len <= 0:
            raise ValueError ("seqs0_len (sequence length) must be positive")
        else:
            seqs1_pos_x_x = self.o_find_pos_x_x_of_seqs(seq1)
            if seqs1_pos_x_x == None:
                raise ValueError ("there is no such seq1 (sequence) in the string")
            elif seqs1_pos_x_x[-1][0] - seqs0_len < 0:
                raise IndexError ("there is maximum " + str(seqs1_pos_x_x[-1][0]) +" characters before " + seq1 + " and not " + str(seqs0_len))
            else:
                seqs0=[]
                for i in range(len(seqs1_pos_x_x)):
                    if seqs1_pos_x_x[i][0] - seqs0_len > 0:
                        seqs0.append(self.o_read_seq_on_pos_x_x(seqs1_pos_x_x[i][0] - seqs0_len, seqs1_pos_x_x[i][0] - 1))
                    else:
                        seqs0.append(self.o_read_all_up_to_incl_pos_x(seqs1_pos_x_x[i][0] - 1))
                return seqs0



    def o_read_all_aft_last_chr(self, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            chrs_pos_x = self.o_find_pos_x_of_chrs(chr)
            if chrs_pos_x == None:
                raise ValueError("there is no such chr (character) in the string")
            else:
                chr_pos_x = chrs_pos_x[-1]
                if chr_pos_x + 1 == len(self.data):
                    return None
                else:
                    return self.data[chr_pos_x+1:]

    def o_read_all_aft_last_seq(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not "+str(type(seq)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            seqs_pos_x_x = self.o_find_pos_x_x_of_seqs(seq)
            if seqs_pos_x_x == None:
                raise ValueError("there is no such seq (sequence) in the string")
            else:
                seq_pos_x_x = seqs_pos_x_x[-1]
                if seq_pos_x_x[1] + 1 == len(self.data):
                    return None
                else:
                    return self.data[seq_pos_x_x[1]+1:]

    def o_read_all_aft_first_chr(self, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            chr_pos_x = self.o_find_pos_x_of_chr(chr)
            if chr_pos_x == None:
                raise ValueError("there is no such chr (character) in the string")
            else:
                if chr_pos_x + 1 == len(self.data):
                    return None
                else:
                    return self.data[chr_pos_x+1:]

    def o_read_all_aft_first_seq(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not "+str(type(seq)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            seq_pos_x_x = self.o_find_pos_x_x_of_seq(seq)
            if seq_pos_x_x == None:
                raise ValueError("there is no such seq (sequence) in the string")
            else:
                if seq_pos_x_x[1] + 1 == len(self.data):
                    return None
                else:
                    return self.data[seq_pos_x_x[1]+1:]



    def o_read_all_bef_first_chr(self, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            chr_pos_x = self.o_find_pos_x_of_chr(chr)
            if chr_pos_x == None:
                raise ValueError("there is no such chr (character) in the string")
            elif chr_pos_x == 0:
                return None
            else:
                return self.data[:chr_pos_x]

    def o_read_all_bef_first_seq(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not "+str(type(symbol)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 char long and not 0")
        else:
            seq_pos_x_x = self.o_find_pos_x_x_of_seq(seq)
            if seq_pos_x_x == None:
                raise ValueError("there is no such seq (sequence) in the string")
            elif seq_pos_x_x[0] == 0:
                return None
            else:
                return self.data[:seq_pos_x_x[0]]

    def o_read_all_bef_last_chr(self, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            chrs_pos_x = self.o_find_pos_x_of_chrs(chr)
            if chrs_pos_x == None:
                raise ValueError("there is no such chr (character) in the string")
            else:
                chr_pos_x = chrs_pos_x[-1]
                if chr_pos_x == 0:
                    return None
                else:
                    return self.data[:chr_pos_x]

    def o_read_all_bef_last_seq(self, seq):
        if type(seq) is not str:
            raise TypeError ("seq (sequence) must be string type and not "+str(type(seq)))
        elif len(seq) == 0:
            raise ValueError ("seq (sequence) must be a string at least 1 symbol long and not 0")
        else:
            seqs_pos_x_x = self.o_find_pos_x_x_of_seqs(seq)
            if seqs_pos_x_x == None:
                raise ValueError("there is no such seq (sequence) in the string")
            else:
                seq_pos_x_x = seqs_pos_x_x[-1]
                if seq_pos_x_x[0] == 0:
                    return None
                else:
                    return self.data[:seq_pos_x_x[0]]



    def o_read_all_betw_pairs_chr1_chr2(self, chr1, chr2):
        if type(chr1) is not str:
            raise TypeError("chr1 (character) must be string type and not " + str(type(chr1)))
        elif len(chr1) != 1:
            raise ValueError("chr1 (character) must be a string 1 char long and not " + str(len(chr1)))
        elif type(chr2) is not str:
            raise TypeError("chr2 (character) must be string type and not " + str(type(chr2)))
        elif len(chr2) != 1:
            raise ValueError("chr2 (character) must be a string 1 char long and not " + str(len(chr2)))
        elif chr1 == chr2:
            raise ValueError("chr1 and chr2 must be to different characters")
        else:
            pairs_pos_x = self.o_find_pos_x_x_of_pairs_chr1_chr2(chr1, chr2)
            seqs = []
            for i in range(len(pairs_pos_x)):
                if pairs_pos_x[i][1] - pairs_pos_x[i][0] > 2:
                    seqs.append(self.o_read_seq_on_pos_x_x(pairs_pos_x[i][0] + 1, pairs_pos_x[i][1] - 1))
                elif pairs_pos_x[i][1] - pairs_pos_x[i][0] == 2:
                    seqs.append(self.data[pairs_pos_x[i][0]+1])
            if len(seqs) == 0:
                return None
            else:
                return seqs

    def o_read_all_betw_pairs_seq1_seq2(self, seq1, seq2):
        if type(seq1) is not str:
            raise TypeError("seq1 (sequence) must be string type and not " + str(type(seq1)))
        elif len(seq1) == 0:
            raise ValueError("seq1 (sequence) must be a string at least 1 char long and not 0")
        elif type(seq2) is not str:
            raise TypeError("seq2 (sequence) must be string type and not " + str(type(seq2)))
        elif len(seq2) == 0:
            raise ValueError("seq1 (sequence) must be a string at least 1 char long and not 0")
        elif seq1 == seq2:
            raise ValueError("seq1 and seq2 must be to different sequences")
        else:
            pairs_pos_x_x = self.o_find_pos_x_x_of_pairs_seq1_seq2(seq1, seq2)
            seqs = []
            for i in range(len(pairs_pos_x_x)):
                if pairs_pos_x_x[i][1][0] - pairs_pos_x_x[i][0][-1] > 2:
                    seqs.append(self.o_read_seq_on_pos_x_x(pairs_pos_x_x[i][0][-1] + 1, pairs_pos_x_x[i][1][0] - 1))
                elif pairs_pos_x_x[i][1][0] - pairs_pos_x_x[i][0][-1] == 2:
                    seqs.append(self.data[pairs_pos_x_x[i][0][-1]+1])
            if len(seqs) == 0:
                return None
            else:
                return seqs



    def o_read_all_from_pos_x(self, pos_x):
        if type(pos_x) is not int:
            raise TypeError ("pos_x (position) must be int type and not " + str(type(pos_x)))
        elif pos_x >= len(self.data):
            raise IndexError ("there is no such position to look, max is " + str(len(self.data)-1) +" and not " + str(pos_x))
        elif pos_x <= -len(self.data)-1:
            raise IndexError ("there is no such position to look, min is " + str(-len(self.data)) +" and not " + str(pos_x))
        else:
            return self.data[pos_x:]

    def o_read_all_up_to_incl_pos_x(self, pos_x):
        if type(pos_x) is not int:
            raise TypeError ("pos_x (position) must be int type and not " + str(type(pos_x)))
        elif pos_x >= len(self.data):
            raise IndexError ("there is no such position to look, max is " + str(len(self.data)-1) +" and not " + str(pos_x))
        elif pos_x <= -len(self.data)-1:
            raise IndexError ("there is no such position to look, min is " + str(-len(self.data)) +" and not " + str(pos_x))
        else:
            return self.data[:pos_x + 1]



    def o_read_seq_on_pos_x_x(self, pos_x_first, pos_x_last):
        if type(pos_x_first) is not int:
            raise TypeError ("pos_x_first (position) must be int type and not " + str(type(pos_x_first)))
        elif pos_x_first >= len(self.data):
            raise IndexError ("there is no such pos_x_first (position) to look, max is " + str(len(self.data)-1) +" and not " + str(pos_x_first))
        elif pos_x_first <= -len(self.data)-1:
            raise IndexError ("there is no such pos_x_first (position) to look, min is " + str(-len(self.data)) +" and not " + str(pos_x_first))
        elif type(pos_x_last) is not int:
            raise TypeError ("pos_x_last (position) must be int type and not " + str(type(pos_x_last)))
        elif pos_x_last >= len(self.data):
            raise IndexError ("there is no such pos_x_last (position) to look, max is " + str(len(self.data) - 1) + " and not " + str(pos_x_last))
        elif pos_x_last <= -len(self.data) - 1:
            raise IndexError ("there is no such pos_x_last (position) to look, min is " + str(-len(self.data)) + " and not " + str(pos_x_last))
        # elif pos_x_first == pos_x_last or pos_x_first + len(self.data) == pos_x_last or pos_x_first == pos_x_last + len(self.data):
        #     raise ValueError ("pos_x_first and pos_x_last must be different positions")
        elif pos_x_first >= 0 and pos_x_last >= 0:
            if pos_x_first > pos_x_last:
                raise ValueError ("incorrect range between pos_x_last (position) and pos_x_first")
            else:
                return self.data[pos_x_first:pos_x_last + 1]
        elif pos_x_first < 0 and pos_x_last < 0:
            if pos_x_first > pos_x_last:
                raise ValueError ("incorrect range between pos_x_last (position) and pos_x_first")
            else:
                return self.data[pos_x_first:pos_x_last + 1]
        elif pos_x_first >= 0 and pos_x_last < 0:
            if pos_x_first > pos_x_last + len(self.data):
                raise ValueError ("incorrect range between pos_x_last (position) and pos_x_first")
            else:
                return self.data[pos_x_first:pos_x_last + 1]
        elif pos_x_first < 0 and pos_x_last >= 0:
            if pos_x_first + len(self.data) > pos_x_last:
                raise ValueError ("incorrect range between pos_x_last (position) and pos_x_first")
            else:
                return self.data[pos_x_first:pos_x_last + 1]

    def o_read_seqs_on_pos_x_x_bulk(self, all_pos_x_x):
        all_pos_x_x = o_comb_regns(all_pos_x_x)
        seqs=[]
        for i in range(len(all_pos_x_x)):
            seqs.append(self.o_read_seq_on_pos_x_x(all_pos_x_x[i][0], all_pos_x_x[i][-1]))
        return seqs



    def o_read_all_around_delims(self, delim):
        delims_pos_x = self.o_find_pos_x_x_of_seqs(delim)
        seqs = self.o_read_all_around_positions_x_x(delims_pos_x)
        if len(seqs) == 0:
            return None
        else:
            return seqs

    def o_read_all_around_delims_bulk(self, delims):
        delims_pos_x = self.o_find_pos_x_x_of_seqs_bulk(delims)
        seqs = self.o_read_all_around_positions_x_x(delims_pos_x)
        if len(seqs) == 0:
            return None
        else:
            return seqs

    def o_read_all_around_positions_x_x(self, all_pos_x_x):
        all_pos_x_x = self.o_comb_regns(all_pos_x_x)
        seqs=[]
        inv_pos_x_x = self.o_inv_regns(all_pos_x_x)
        return self.o_read_seqs_on_pos_x_x_bulk(inv_pos_x_x)



    def o_w_report(func):
        def wrapper(*args):
            try:
                func(*args)
            except:
                return None
            else:
                return "Done"
        return wrapper



    def o_show_del_seq(self, seq):
        return show_del_all_on_pos_x_x(self.o_find_pos_x_x_of_seq(seq))

    @ o_w_report
    def o_do_del_seq(self, seq):
        self.data = self.o_show_del_seq(seq)

    def o_show_del_seqs(self, seq):
        return show_del_all_on_pos_x_x(self.o_find_pos_x_x_of_seqs(seq))

    @ o_w_report
    def o_do_del_seqs(self, seq):
        self.data = self.o_show_del_seqs(seq)

    def o_show_del_all_from_pos_x(self, pos_x):
        return self.data[:pos_x]

    @ o_w_report
    def o_do_del_all_from_pos_x(self, pos_x):
        self.data = self.o_show_del_all_from_pos_x(pos_x)

    def o_show_del_all_up_to_incl_pos_x(self, pos_x):
        return self.data[pos_x + 1:]

    @ o_w_report
    def o_do_del_all_up_to_incl_pos_x(self, pos_x):
        self.data = self.o_show_del_all_up_to_incl_pos_x(pos_x)

    def o_show_del_all_on_pos_x_x(self, pos_x_x):
        return self.data[:pos_x_x[0]] + self.data[pos_x_x[-1] + 1:]

    @ o_w_report
    def o_do_del_all_on_pos_x_x(self, pos_x_x):
        self.data = self.o_show_del_all_on_pos_x_x(pos_x_x)



    def o_show_del_all_aft_seq(self, seq):
        return self.data[:self.data.index(seq) + len(seq)]

    @ o_w_report
    def o_do_del_all_aft_seq(self, seq):
        self.data = self.o_show_del_all_aft_seq(seq)

    def o_show_del_all_bef_seq(self, seq):
        pos_x = self.o_find_pos_x_x_of_seq(seq)[0] - 1
        if pos_x > 0:
            return self.o_show_del_all_up_to_incl_pos_x(pos_x)
        else:
            return self.data

    @ o_w_report
    def o_do_del_all_bef_seq(self, seq):
        self.data = self.o_show_del_all_bef_seq(seq)

    def o_show_del_all_betw_seq1_seq2(self, seq1, seq2):
        seq1_pos_x_x = self.o_find_pos_x_x_of_seq(seq1)
        seq2_pos_x_x = self.o_find_pos_x_x_of_seq(seq2)
        if seq1_pos_x_x[-1]+1 < seq2_pos_x_x[0]:
            pos_x_x = [seq1_pos_x_x[-1]+1, seq2_pos_x_x[0]-1]
            return ''.join(self.o_read_seqs_on_pos_x_x_bulk(self.o_inv_regns(pos_x_x)))
        else:
            return self.data

    @ o_w_report
    def o_do_del_all_betw_seq1_seq2(self, seq1, seq2):
        self.data = self.o_show_del_all_betw_seq1_seq2(seq1, seq2)

    def o_show_del_all_betw_pairs_seq1_seq2(self, seq1, seq2):
        seqs_pos_x_x = self.o_find_pos_x_x_of_pairs_seq1_seq2(seq1, seq2)
        seqs_to_del_pos_x_x = []
        if len(seqs_pos_x_x) == 0:
            return self.data
        for i in range(len(seqs_pos_x_x)):
            if seqs_pos_x_x[i][1][0]-1 - (seqs_pos_x_x[i][0][-1]+1) > 0:
                seqs_to_del_pos_x_x.append([seqs_pos_x_x[i][0][-1]+1, seqs_pos_x_x[i][1][0]-1])
        return ''.join(self.o_read_seqs_on_pos_x_x_bulk(self.o_inv_regns(seqs_to_del_pos_x_x)))

    @ o_w_report
    def o_do_del_all_betw_pairs_seq1_seq2(self, seq1, seq2):
        self.data = self.o_show_del_all_betw_pairs_seq1_seq2(seq1, seq2)



    def o_show_write_seq_in_at_pos_x(self, pos_x, seq):
        return self.data[:pos_x] + seq + self.data[pos_x:]

    @ o_w_report
    def o_do_write_seq_in_at_pos_x(self, pos_x, seq):
        self.data = self.o_show_write_seq_in_at_pos_x(pos_x, seq)

    def o_show_write_seq_over_at_pos_x(self, pos_x, seq):
        return self.data[:pos_x] + seq + self.data[pos_x+len(seq):]

    @ o_w_report
    def o_do_write_seq_over_at_pos_x(self, pos_x, seq):
        self.data = self.o_show_write_seq_over_at_pos_x(pos_x, seq)



    def o_show_write_seq0_in_bef_seq1(self, seq1, seq0):
        seq1_pos_x = self.data.index(seq1)
        return self.data[:seq1_pos_x] + seq0 + self.data[seq1_pos_x:]

    @ o_w_report
    def o_do_write_seq0_in_bef_seq1(self, seq1, seq0):
        self.data = self.o_show_write_seq0_in_bef_seq1(seq1, seq0)

    def o_show_write_seq2_in_aft_seq1(self, seq1, seq2):
        seq1_pos_x = self.data.index(seq1) + len(seq1)
        return self.data[:seq1_pos_x] + seq2 + self.data[seq1_pos_x:]

    @ o_w_report
    def o_do_write_seq2_in_aft_seq1(self, seq1, seq2):
        self.data = self.o_show_write_seq2_in_aft_seq1(seq1, seq2)

    def o_show_write_seq2_over_aft_seq1(self, seq1, seq2):
        seq1_pos_x = self.data.index(seq1) + len(seq1)
        return self.data[:seq1_pos_x] + seq2 + self.data[seq1_pos_x+len(seq2):]

    @ o_w_report
    def o_do_write_seq2_over_aft_seq1(self, seq1, seq2):
        self.data = self.o_show_write_seq2_over_aft_seq1(seq1, seq2)



    def o_show_rplace_seq1_w_seq2(self, seq1, seq2):
        seq1_pos_x = self.data.index(seq1)
        return self.data[:seq1_pos_x] + seq2 + self.data[seq1_pos_x+len(seq1):]

    @ o_w_report
    def o_do_rplace_seq1_w_seq2(self, seq1, seq2):
        self.data = self.o_show_rplace_seq1_w_seq2(seq1, seq2)



    def o_show_rplace_seqs1_w_seqs2(self, seq1, seq2):
        seqs1_pos_x_x = self.o_find_pos_x_x_of_seqs(seq1)
        inv_pos_x_x = self.o_inv_regns(seqs1_pos_x_x)
        show = seq2.join(self.o_read_seqs_on_pos_x_x_bulk(inv_pos_x_x))
        if seqs1_pos_x_x[0][0] == 0:
            show = seq2+show
        if seqs1_pos_x_x[-1][-1] == len(self.data)-1:
            show = show+seq2
        return show

    @ o_w_report
    def o_do_rplace_seqs1_w_seqs2(self, seq1, seq2):
        self.data = self.o_show_rplace_seqs1_w_seqs2(seq1, seq2)



    def o_show_rplace_all_aft_seq1_w_seq2(self, seq1, seq2):
        seq1_pos_x = self.data.index(seq1)
        return self.data[:seq1_pos_x+len(seq1)]+seq2

    @ o_w_report
    def o_do_rplace_all_aft_seq1_w_seq2(self, seq1, seq2):
        self.data = self.o_show_rplace_all_aft_seq1_w_seq2(seq1, seq2)

    def o_show_rplace_all_bef_seq1_w_seq0(self, seq1, seq0):
        seq1_pos_x = self.data.index(seq1)
        return seq0+self.data[seq1_pos_x:]

    @ o_w_report
    def o_do_rplace_all_bef_seq1_w_seq0(self, seq1, seq0):
        self.data = self.o_show_rplace_all_bef_seq1_w_seq0(seq1, seq0)

    def o_show_rplace_all_betw_pair_seq1_seq3_w_seq2(self, seq1, seq3, seq2):
        selfdata=self.data
        seqs_pair_pos_x_x = self.o_find_pos_x_x_of_pairs_seq1_seq2(seq1, seq3)[0]
        seqs2_pos_x_x = [seqs_pair_pos_x_x[0][1]+1, seqs_pair_pos_x_x[-1][0]-1]
        self.o_do_del_all_on_pos_x_x(seqs2_pos_x_x)
        self.o_do_write_seq_in_at_pos_x(seqs2_pos_x_x[0], seq2)
        show=self.data
        self.data=selfdata
        return show

    @ o_w_report
    def o_do_rplace_all_betw_pair_seq1_seq3_w_seq2(self, seq1, seq3, seq2):
        self.data = self.o_show_rplace_all_betw_pair_seq1_seq3_w_seq2(seq1, seq3, seq2)

    def o_show_rplace_all_betw_pairs_seqs1_seqs3_w_seqs2(self, seq1, seq3, seq2):
        selfdata=self.data
        seqs_pairs_pos_x_x = self.o_find_pos_x_x_of_pairs_seq1_seq2(seq1, seq3)
        self.o_do_del_all_betw_pairs_seq1_seq2(seq1, seq3)
        seqs2_pos_x_x = [each[0] + len(seq1) for each in self.o_find_pos_x_x_of_seqs(seq1 + seq3)]
        [self.o_do_write_seq_in_at_pos_x(seqs2_pos_x_x[each - 1], seq2) for each in range(len(seqs2_pos_x_x), 0, -1)]
        show=self.data
        self.data=selfdata
        return show

    @ o_w_report
    def o_do_rplace_all_betw_pairs_seqs1_seqs3_w_seqs2(self, seq1, seq3, seq2):
        self.data = self.o_show_rplace_all_betw_pairs_seqs1_seqs3_w_seqs2(seq1, seq3, seq2)



    def o_show_rplace_all_on_pos_x_x_w_seq(self, pos_x_first, pos_x_last, seq):
        return self.data[:pos_x_first]+seq+self.data[pos_x_last+1:]

    @ o_w_report
    def o_do_rplace_all_on_pos_x_x_w_seq(self, pos_x_first, pos_x_last, seq):
        self.data=self.o_show_rplace_all_on_pos_x_x_w_seq(pos_x_first, pos_x_last, seq)

    def o_show_rplace_all_from_pos_x_w_seq(self, pos_x, seq):
        return self.data[:pos_x]+seq

    @ o_w_report
    def o_do_rplace_all_from_pos_x_w_seq(self, pos_x, seq):
        self.data = self.o_show_rplace_all_from_pos_x_w_seq(pos_x, seq)

    def o_show_rplace_all_up_to_incl_pos_x_w_seq(self, pos_x, seq):
        if pos_x+1<len(self.data):
            return seq+self.data[pos_x+1:]
        else:
            return seq

    @ o_w_report
    def o_do_rplace_all_up_to_incl_pos_x_w_seq(self, pos_x, seq):
        self.data = self.o_show_rplace_all_up_to_incl_pos_x_w_seq(pos_x, seq)

    def o_show_rplace_seq_w_chrs(self, seq, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            return self.o_show_rplace_seq1_w_seq2(seq, chr * len(seq))

    @ o_w_report
    def o_do_rplace_seq_w_chrs(self, seq, chr):
        self.data = self.o_show_rplace_seq_w_chrs(seq, chr)

    def o_show_rplace_seqs_w_chrs(self, seq, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            return self.o_show_rplace_seqs1_w_seqs2(seq, chr * len(seq))

    @ o_w_report
    def o_do_rplace_seqs_w_chrs(self, seq, chr):
        self.data = self.o_show_rplace_seqs_w_chrs(seq, chr)



    def o_show_rplace_all_aft_seq_w_chrs(self, seq, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            return self.o_show_rplace_all_aft_seq1_w_seq2(seq, chr * (len(self.data) - self.data.index(seq) - len(seq)))

    @ o_w_report
    def o_do_rplace_all_aft_seq_w_chrs(self, seq, chr):
        self.data = self.o_show_rplace_all_aft_seq_w_chrs(seq, chr)

    def o_show_rplace_all_bef_seq_w_chrs(self, seq, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            return self.o_show_rplace_all_bef_seq1_w_seq0(seq, chr * self.data.index(seq))

    @ o_w_report
    def o_do_rplace_all_bef_seq_w_chrs(self, seq, chr):
        self.data = self.o_show_rplace_all_bef_seq_w_chrs(seq, chr)

    def o_show_rplace_all_betw_pair_seq1_seq2_w_chrs(self, seq1, seq2, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            selfdata = self.data
            seqs_pair_pos_x_x = self.o_find_pos_x_x_of_pairs_seq1_seq2(seq1, seq2)[0]
            seqs2_pos_x_x = [seqs_pair_pos_x_x[0][1] + 1, seqs_pair_pos_x_x[-1][0] - 1]
            self.o_do_del_all_on_pos_x_x(seqs2_pos_x_x)
            self.o_do_write_seq_in_at_pos_x(seqs2_pos_x_x[0], chr * (seqs2_pos_x_x[1] + 1 - seqs2_pos_x_x[0]))
            show = self.data
            self.data = selfdata
            return show

    @ o_w_report
    def o_do_rplace_all_betw_pair_seq1_seq2_w_chrs(self, seq1, seq2, chr):
        self.data = self.o_show_rplace_all_betw_pair_seq1_seq2_w_chrs(seq1, seq2, chr)

    def o_show_rplace_all_betw_pairs_seqs1_seqs2_w_chrs(self, seq1, seq2, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            selfdata = self.data
            seqs_pairs_pos_x_x = self.o_find_pos_x_x_of_pairs_seq1_seq2(seq1, seq2)
            self.o_do_del_all_betw_pairs_seq1_seq2(seq1, seq2)
            seqs2_pos_x_x = [each[0] + len(seq1) for each in self.o_find_pos_x_x_of_seqs(seq1 + seq2)]
            seqs2_len = [seqs_pairs_pos_x_x[each][-1][0]-1-seqs_pairs_pos_x_x[each][0][-1] for each in range(len(seqs_pairs_pos_x_x))]
            [self.o_do_write_seq_in_at_pos_x(seqs2_pos_x_x[each - 1], chr * seqs2_len[each - 1]) for each in range(len(seqs2_pos_x_x), 0, -1)]
            show = self.data
            self.data = selfdata
            return show

    @ o_w_report
    def o_do_rplace_all_betw_pairs_seqs1_seqs2_w_chrs(self, seq1, seq2, chr):
        self.data = self.o_show_rplace_all_betw_pairs_seqs1_seqs2_w_chrs(seq1, seq2, chr)



    def o_show_rplace_all_on_pos_x_x_w_chrs(self, pos_x_first, pos_x_last, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            return self.o_show_rplace_all_on_pos_x_x_w_seq(pos_x_first, pos_x_last, chr * (pos_x_last - pos_x_first + 1))

    @ o_w_report
    def o_do_rplace_all_on_pos_x_x_w_chrs(self, pos_x_first, pos_x_last, chr):
        self.data = self.o_show_rplace_all_on_pos_x_x_w_chrs(pos_x_first, pos_x_last, chr)

    def o_show_rplace_all_from_pos_x_w_chrs(self, pos_x, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            return self.o_show_rplace_all_from_pos_x_w_seq(pos_x, chr * (len(self.data) - pos_x))

    @ o_w_report
    def o_do_rplace_all_from_pos_x_w_chrs(self, pos_x, chr):
        self.data = self.o_show_rplace_all_from_pos_x_w_chrs(pos_x, chr)

    def o_show_rplace_all_up_to_incl_pos_x_w_chrs(self, pos_x, chr):
        if type(chr) is not str:
            raise TypeError ("chr (character) must be string type and not " + str(type(chr)))
        elif len(chr) != 1:
            raise ValueError ("chr (character) must be a string 1 char long and not " + str(len(chr)))
        else:
            return self.o_show_rplace_all_up_to_incl_pos_x_w_seq(pos_x, chr * (pos_x + 1))

    @ o_w_report
    def o_do_rplace_all_up_to_incl_pos_x_w_chrs(self, pos_x, chr):
        self.data = self.o_show_rplace_all_up_to_incl_pos_x_w_chrs(pos_x, chr)



########################################################################################################################

# Получаем имя файла и считываем его в идентификатор

with open('LineParser.txt', 'r', encoding='utf-8') as file:
    one_liner_from_the_file = file.read(120)

# Создаём объект класса с интересующим содержимым файла

line = ParseLine(one_liner_from_the_file)

print()
print(line.data)


print()

result = line.del_by_pos([10, 120], True)
print(result)

print(line.data)


# [[5, 8], [12, 25, 29], [[35, 50], 54, 60, [75, 80]]]


# input()


