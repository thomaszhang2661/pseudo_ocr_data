# -*- coding: utf-8 -*-
import re
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

    E_pun = u',!?[][]()<>‘ ~:-@#$￥%|;=-'
    C_pun = u'，！？【】［］（）〈〉\'~：—＠＃＄￥％｜；＝－'
    table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    string = string.translate(table)
    string = string.replace('…', '...')
    string = re.sub(r'\s+', '', string)
    #string = string.replace('/', '\\')
    return string