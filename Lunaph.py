# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 11:30:14 2021

@author: lfz
"""

import re

class PoS(object):
    def __init__(self, *, abbr, pos, pat = '.*', info = ''):
        self._abbr = abbr
        self._pos = pos
        self._pat = pat
        self._info = info
    
    @property
    def abbr(self):
        return self._abbr
    @abbr.setter
    def abbr(self, abbr):
        if abbr != '':
            if abbr == '\\':
                abbr = ''
            self._abbr = abbr
    
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, pos):
        if pos != '':
            if pos == '\\':
                pos = ''
            self._pos = pos
            
    @property
    def pat(self):
        return self._pat
    @pat.setter
    def pat(self, pat):
        if pat != '':
            if pat == '\\':
                pat = ''
            self._pat = pat
    
    @property
    def info(self):
        return self._info
    @info.setter
    def info(self, info):
        if info != '':
            if info == '\\':
                info = ''
            self._info = info
    
    def reset(self, *, abbr = '', pos = '', pat = '', info = ''):
        self.abbr = abbr
        self.pos = pos
        self.pat = pat
        self.info = info
    
    def __str__(self):
        return '\nPart of Speech:\t%s\nAbbreviation:\t%s\nInformation:\t%s\nType Pattern:\t%s' %(self.pos, self.abbr, self.info, self.pat)

class Word(object):
    def __init__(self, *, con, nat, pos = '', ipa = '', info = ''):
        self._con = con
        self._nat = nat
        self._pos = pos
        self._ipa = ipa
        self._def = info
        
    @property
    def con(self):
        return self._con
    @con.setter
    def con(self, con):
        if con != '':
            if con == '\\':
                con = ''
            self._con = con
    
    @property
    def nat(self):
        return self._nat
    @nat.setter
    def nat(self, nat):
        if nat != '':
            if nat == '\\':
                nat = ''
            self._nat = nat
    
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, pos):
        if pos != '':
            if pos == '\\':
                pos = ''
            self._pos = pos
    
    @property
    def ipa(self):
        return self._ipa
    @ipa.setter
    def ipa(self, ipa):
        if ipa != '':
            if ipa == '\\':
                ipa = ''
            self._ipa = ipa
    
    @property
    def info(self):
        return self._def
    @info.setter
    def info(self, info):
        if info != '':
            if info == '\\':
                info = ''
            self._def = info
    
    def reset(self, *, con = '', nat = '', pos = '', ipa = '', info = ''):
        self.con = con
        self.nat = nat
        self.pos = pos
        self.ipa = ipa
        self.info = info
    
    def __str__(self):
        return '\nWord:\t\t\t%s\nMeaning(s):\t\t%s\nPart of Speech:\t%s\nSpelling:\t\t%s\nDefinition:\t\t%s' %(self.con, self.nat, self.pos, self.ipa, self.info)

class Document(object):
    def __init__(self, *, pos = None, dic = None):
        if pos is None:
            pos = {}
        if dic is None:
            dic = {}
        self._pos = pos
        self._dict = dic
    
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        
    @property
    def dic(self):
        return self._dict
    @dic.setter
    def dic(self, _dict):
        self._dict = _dict

def word2dict(w):
    return dict(con = w.con, nat = w.nat, pos = w.pos, ipa = w.ipa, info = w.info)
"""
def dict2word(d):
    return Word(d['con'], d['nat'], d['pos'], d['ipa'], d['info'])
"""
def pos2dict(p):
    return dict(abbr = p.abbr, pos = p.pos, pat = p.pat, info = p.info)
"""
def dict2pos(d):
    return PoS(d['abbr'], d['pos'])
"""
"""
def copy(src):
    w = Word(src.con, src.nat, src.pos, src.ipa, src.info)
    return w
"""
def save(dirL, doc):
    with open(dirL, 'w', encoding = 'utf-8') as f:
        f.write(str(dict(pos = [pos2dict(p) for p in doc.pos.values()], 
                         word = [word2dict(w) for w in doc.dic.values()])))

def load(dirL):
    doc = Document()
    with open(dirL, 'r', encoding = 'utf-8') as f:
        dictL = eval(f.read())
        doc.pos = dict([(d['abbr'], PoS(**d)) for d in dictL['pos']])
        doc.dic = dict([(d['con'], Word(**d)) for d in dictL['word']])
        return doc

def delete(doc, *args):
    if '-p' in args:
        abbr = input('abbr> ')
        if abbr not in doc.pos.keys():
            print('Part of speech "%s" doesn\'t exist!' % abbr)
            return
        del doc.pos[abbr]
    else:
        con = input('con> ')
        if con not in doc.dic.keys():
            print('Word "%s" doesn\'t exist!' % con)
            return
        del doc.dic[con]

def add(doc, *args):
    d = {}
    if '-p' in args:
        d['pos'] = input('pos> ')
        abbr = input('abbr> ')
        d['abbr'] = abbr
        if '-a' in args: # complex mode
            d['pat'] = input('pat> ')
            d['info'] = input('info> ')
        doc.pos[abbr] = PoS(**d)
    else:
        con = input('con> ')
        d['con'] = con
        d['nat'] = input('nat> ')
        if '-a' in args: # complex mode
            pos = input('pos> ')
            while pos != '':
                if pos in doc.pos.keys():
                    if re.search(doc.pos[pos].pat, con) is None:
                        chc = input(f'The word doesn\'t match the enforced pattern for type: {doc.pos[pos].pos}. Do you want to override lexical rules? [y/n]')
                        if chc == 'y':
                            break
                    else:
                        break
                else:
                    print('Invalid part of speech, please input again or press enter to skip the process.')
                pos = input('pos> ')
            d['pos'] = pos
            d['ipa'] = input('ipa> ')
            d['info'] = input('def> ')
        doc.dic[con] = Word(**d)

def adjust(doc, *args):
    d = {}
    if '-p' in args:        
        oabbr = input('abbr> ')
        if oabbr not in doc.pos.keys():
            print('Abbreviation "%s" doesn\'t exist!' & oabbr)
            return
        p = PoS(**pos2dict(doc.pos[oabbr])) # copy a part of speech
        del doc.pos[oabbr]
        d['pos'] = input('new pos> ')
        abbr = input('new abbr> ')
        if abbr == '':
            abbr = oabbr
        d['abbr'] = abbr
        if '-a' in args: # complex mode
            d['pat'] = input('new pat> ')
            d['info'] = input('new info> ')
        p.reset(**d)
        doc.pos[abbr] = p
    else:
        ocon = input('con> ')
        if ocon not in doc.dic.keys():
            print('Word "%s" doesn\'t exist!' % ocon)
            return
        w = Word(**word2dict(doc.dic[ocon])) # copy a word
        del doc.dic[ocon]
        con = input('new con> ')
        if con == '':
            con = ocon
        d['con'] = con
        d['nat'] = input('new nat> ')
        if '-a' in args: # complex mode
            pos = input('new pos> ')
            while pos != '' and pos != '\\':
                if pos in doc.pos.keys():
                    if re.search(doc.pos[pos].pat, con) is None:
                        chc = input(f'The word doesn\'t match the enforced pattern for type: {doc.pos[pos].pos}. Do you want to override lexical rules? [y/n]')
                        if chc == 'y':
                            break
                    else:
                        break
                else:
                    print('Invalid part of speech, please input again or press enter to skip the process.')
                pos = input('new pos> ')
            d['pos'] = pos
            d['ipa'] = input('new ipa> ')
            d['info'] = input('new def> ')
        w.reset(**d)
        doc.dic[con] = w

def echo(doc, *args):
    if '-p' in args:
        abbr = input('abbr> ')
        if abbr not in doc.pos.keys():
            print('Part of speech "%s" doesn\'t exist!' % abbr)
            return
        print(doc.pos[abbr])
    else:
        con = input('con> ')
        if con not in doc.dic.keys():
            print('Word "%s" doesn\'t exist!' % con)
            return
        print(doc.dic[con])

def main():
    doc = Document()
    while True:
        op = input('> ')
        if op == 'exit' or op == ';':
            break
        elif op == 'save':
            file = input('file> ')
            if '.' not in file:
                file += '.ln'
            save(file, doc)
        elif op == 'load':
            file = input('file> ')
            if '.' not in file:
                file += '.ln'
            doc = load(file)
        
        else:
            lis = op.split()
            if lis[0] == 'del':
                delete(doc, *lis)
            
            elif lis[0] == 'pos':
                add(doc, *lis, '-p')
            
            elif lis[0] == 'add':
                add(doc, *lis)
            
            elif lis[0] == 'adj':
                adjust(doc, *lis)
            
            elif lis[0] == 'echo':
                echo(doc, *lis)

if __name__ == '__main__':
    main()