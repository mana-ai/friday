import re
import jieba


dict_word_digit = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8,
                   '九': 9, '十': 10, '百': 100, '千': 1000, '万': 10000,
                   '０': 0, '１': 1, '２': 2, '３': 3, '４': 4, '５': 5, '６': 6, '７': 7, '８': 8, '９': 9,
                   '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '拾': 10, '佰': 100,
                   '仟': 1000, '萬': 10000,
                   '亿': 100000000}


def cn_to_digits(sentence, extract=False):
    """
    this function will change all Chinese num character into digits
    if extract set True, then will only return number
    :param sentence:
    :param extract:
    :return:
    """
    def single_to_digit(a):
        count = 0
        result = 0
        tmp = 0
        billion = 0
        while count < len(a):
            tmp_chr = a[count]
            # print tmpChr
            tmp_num = dict_word_digit.get(tmp_chr, None)
            # 如果等于1亿
            if tmp_num == 100000000:
                result += tmp
                result = result * tmp_num
                # 获得亿以上的数量，将其保存在中间变量Billion中并清空result
                billion = billion * 100000000 + result
                result = 0
                tmp = 0
            # 如果等于1万
            elif tmp_num == 10000:
                result += tmp
                result = result * tmp_num
                tmp = 0
            # 如果等于十或者百，千
            elif tmp_num >= 10:
                if tmp == 0:
                    tmp = 1
                result += tmp_num * tmp
                tmp = 0
            # 如果是个位数
            elif tmp_num is not None:
                tmp = tmp * 10 + tmp_num
            count += 1
        result += tmp
        result += billion
        return result
    p = re.findall(r'[零一二两三四五六七八九十百千万０１２３４５６７８９壹贰叁肆伍陆柒捌玖拾佰仟萬亿]+', sentence)
    converted_digits = []
    for w in p:
        r = single_to_digit(w)
        converted_digits.append(r)
    for i, w in enumerate(p):
        sentence = sentence.replace(w, str(converted_digits[i]))
    if extract:
        return converted_digits
    else:
        return sentence


def digits_to_cn(sentence, extract=False):
    """
    this method will convert a sentence contains digits into Chinese number characters.
    :param sentence:
    :param extract:
    :return:
    """
    def single_to_cn(num):
        words = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        if isinstance(num, int):
            length = len(str(num))
        else:
            length = len(num)
            num = int(num)
        if length == 1:
            return words[num]
        elif length == 2:
            tens_w = num // 10
            digits_w = num % 10
            if digits_w == 0:
                if tens_w == 1:
                    return '十'
                else:
                    return words[tens_w] + '十'
            else:
                if tens_w == 1:
                    return '十' + words[digits_w]
                else:
                    return words[tens_w] + '十' + words[digits_w]
        elif length == 3:
            hundreds_w = num // 100
            tens_w = (num - hundreds_w * 100) // 10
            digits_w = num % 10
            if hundreds_w == 0:
                if tens_w == 0:
                    return words[digits_w]
                else:
                    return words[tens_w] + words[digits_w]
            else:
                return words[hundreds_w] + '百' + words[tens_w] + '十' + words[digits_w]
        elif length == 4:
            thousands_w = num // 1000
            hundreds_w = (num - thousands_w * 1000) // 100
            tens_w = (num - thousands_w * 1000 - hundreds_w * 100) // 10
            digits_w = num % 10

            return '{0}{1}{2}{3}{4}{5}{6}'.format(
                words[thousands_w],
                '千' if thousands_w != 0 else '',
                words[hundreds_w],
                '百' if hundreds_w != 0 else '',
                words[tens_w],
                '十' if tens_w != 0 else '',
                words[digits_w],
            )

            # if thousands_w == 0:
            #     if hundreds_w == 0:
            #         if tens_w == 0:
            #             return words[digits_w]
            #         else:
            #             return words[tens_w] + words[digits_w]
            #     else:
            #         return words[hundreds_w] + words[tens_w] + words[digits_w]
            # else:
            #     if hundreds_w == 0:
            #         if tens_w == 0:
            #             return words[thousands_w] + '千' + words[digits_w]
            #         else:
            #             return words[tens_w] + words[digits_w]
            #     else:
            #         return words[thousands_w] + '千' + words[hundreds_w] + '百' + words[tens_w] + '十' + words[digits_w]

    p = re.findall(r'[0-9]+', sentence)
    converted_ws = []
    for n in p:
        r = single_to_cn(n)
        converted_ws.append(r)
    for i, w in enumerate(p):
        sentence = sentence.replace(w, converted_ws[i])
    if extract:
        return converted_ws
    else:
        return sentence


if __name__ == "__main__":
    res = cn_to_digits('十二点的时候喊我起床, 十四点的时候六十八但是还是一和二去洗澡')
    print(res)

    res = digits_to_cn('明天12点的时候喊我，1加1等于多少，8乘以64是多少')
    print(res)
