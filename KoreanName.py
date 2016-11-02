# -*- coding:utf-8 -*-
import hanja
import chardet

chosung = [2, 4, 2, 3, 6, 5, 4, 4, 8, 2, 4, 1, 3, 6, 4, 3, 4, 4, 3]
jungsung = [2, 3, 3, 4, 2, 3, 3, 4, 2, 4, 5, 3, 3, 2, 4, 5, 3, 3, 1, 2, 1]
jongsung = [0, 2, 4, 4, 2, 5, 5, 3, 5, 7, 9, 9, 7, 9, 9, 8, 4, 4, 6, 2, 4, 1, 3, 4, 3, 4, 4, 3]

def write_count_character(name):
    data = unicode(name, "UTF-8")
    result = []
    i=0
    for letter in data:
        if hanja.Hangul.is_hangul(letter):
            cho = hanja.Hangul.separate(letter)[0]
            jung = hanja.Hangul.separate(letter)[1]
            jong = hanja.Hangul.separate(letter)[2]
            write_count = chosung[cho] + jungsung[jung] + jongsung[jong]
            result.insert(i, write_count)
            i += 1
        else:
            print "한글 에러"
            return
    return result


def love_score(from_name, to_name):
    if len(from_name) == 0 or len(to_name) == 0:
        print "이름 확인하세요."
        return
    elif len(from_name) != len(to_name):
        print "두사람 이름 길이는 같아야해요"
        return
    else:
        count_from_name = write_count_character(from_name)
        count_to_name = write_count_character(to_name)
        return love_score_test(from_name, count_from_name, to_name, count_to_name), love_score_test(to_name, count_to_name, from_name, count_from_name)


def love_score_test(from_name, count_from_name, to_name, count_to_name):
    love_array = []
    for i in range(0, len(count_from_name)):
        love_array.append(count_from_name[i])
        love_array.append(count_to_name[i])
    print love_array

    while len(love_array) > 2:
        temp_array=[]
        for i in range(0, len(love_array)-1):
            score = (love_array[i] + love_array[i+1]) % 10
            temp_array.insert(i, score)
        love_array = temp_array
        print love_array
    result = love_array[0] * 10 + love_array[1]
    print from_name, "->", to_name, ":", result
    return result

def flower_star_heaven_hell(name):
    count_from_name = write_count_character(name)
    total = 0
    for i in count_from_name:
        total += i
    mod = total % 4
    if mod == 0:
        return "지옥"
    elif mod == 1:
        return "꽃나라"
    elif mod == 2:
        return "별나라"
    elif mod == 3:
        return "천당"

# name1 = raw_input("첫번째 사람 이름은: ")
# name2 = raw_input("두번째 사람 이름은: ")
# result = love_score(name1, name2)
#
# while True:
#     print "당신의 미래는? 꽃나라, 별나라, 천당, 지옥 중 한 곳으로!!"
#     name1 = raw_input("당신의 이름은 무엇인가요: ")
#     print flower_star_heaven_hell(name1)
