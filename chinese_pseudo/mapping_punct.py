# -*- coding: utf-8 -*-
import re

# 正则表达式匹配拼音
#pattern = r'([a-zA-ZüÜāáǎàīíǐìēéěèōóǒòūúǔùüɡɡ])'

# 特殊字符
symbols = r'(["ç", "ø", "ł", "ŋ", "ʃ", "ʒ", "ɪ", "ʌ", "ə", "θ", "ð","ɒ", "β", "ϕ", "κ", "π", "Ω", "δ", "⅓", "℅", "⌘")'
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

    E_pun = u'••,!?[][]()<><>‘ ~::---@#$￥%|;=/~aaeenoII2福'
    C_pun = u'·•，！？【】［］（）〈〉＜＞\'~：ː—－­＠＃＄￥％｜；＝／～ɑàéëñöⅡ₂褔'
    table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    string = string.translate(table)
    string = string.replace('…', '...')
    string = re.sub(r'\s+', '', string)
    srting = re.sub(symbols,"", string)
    #string = string.replace('/', '\\')

    return string