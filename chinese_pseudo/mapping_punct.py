# -*- coding: utf-8 -*-
import re

# 正则表达式匹配拼音
#pattern = r'([a-zA-ZüÜǖǘǚǜāáǎàīíǐìēéěèōóǒòūúǔùüɡɡāáǎàōóǒòēéěèīíǐìūúǔùüǖǘǚǜêê̄ếê̌ềm̄ḿm̀ńňǹẑĉŝŋĀÁǍÀŌÓǑÒĒÉĚÈĪÍǏÌŪÚǓÙÜǕǗǙǛÊÊ̄ẾÊ̌ỀM̄ḾM̀ŃŇǸẐĈŜŊ❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴])'

# 特殊字符

symbols = r'[çøłŋʃʒɪʌəθðɒβϕκπΩδ⅓℅⌘▲▼ⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]'

def chinesepun2englishpun(string):
    # E_pun = u',.!?[]()<>""\'~:@#$¥%'
    # C_pun = u'，。！？【】（）《》“”‘~：＠＃＄￥％'
    # table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    # string = string.translate(table)
    # string = string.replace('…', '...')
    # #string = string.replace('/', '\\')
    # return string

    #E_pun = u',,.!?[]()<>""\'~:\'-@#$¥%'
    #C_pun = u'、，。！？【】（）《》“”‘~：’—＠＃＄￥％'
    #table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    #string = string.translate(table)
    #string = string.replace('…', '...')
    #string = string.replace('/', '\\')
    #return string

    E_pun = u'•••,!?“”[][][]()()<><>‘~:::----@#$￥%||;=/~aaeeno2福出内'
    C_pun = u'·•●，！？「」【】〖〗［］（）〔〕〈〉＜＞\'~：ː∶—－─­＠＃＄￥％｜∣；＝／～ɑàéëñö₂褔岀內'
    #print(len(E_pun), len(C_pun))
    table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    string = string.translate(table)
    #string = string.replace('…', '...')
    #string = re.sub(r'\s+', '', string)
    string = re.sub(symbols,"", string)
    #string = string.replace('/', '\\')

    return string