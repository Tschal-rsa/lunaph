# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 11:30:14 2021

@author: lfz
"""

class PoS(object):
    def __init__(self, abbr, pos):
        self._abbr = abbr
        self._pos = pos
    
    @property
    def abbr(self):
        return self._abbr
    @abbr.setter
    def abbr(self, abbr):
        if abbr != "\\":
            self._abbr = abbr
    
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, pos):
        if pos != "\\":
            self._pos = pos

class Word(object):
    def __init__(self, con, nat, pos = "", ipa = "", info = ""):
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
        if con != "\\":
            self._con = con
    
    @property
    def nat(self):
        return self._nat
    @nat.setter
    def nat(self, nat):
        if nat != "\\":
            self._nat = nat
    
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, pos):
        if pos != "\\":
            self._pos = pos
    
    @property
    def ipa(self):
        return self._ipa
    @ipa.setter
    def ipa(self, ipa):
        if ipa != "\\":
            self._ipa = ipa
    
    @property
    def info(self):
        return self._def
    @info.setter
    def info(self, info):
        if info != "\\":
            self._def = info
    
    def reset(self, con, nat, pos = "\\", ipa = "\\", info = "\\"):
        self.con = con
        self.nat = nat
        self.pos = pos
        self.ipa = ipa
        self.info = info
    
    def __str__(self):
        return "\nWord:\t\t\t%s\nMeaning(s):\t\t%s\nPart of Speech:\t%s\nSpelling:\t\t%s\nDefinition:\t\t%s" %(self.con, self.nat, self.pos, self.ipa, self.info)

class Document(object):
    def __init__(self, _pos = {}, _dict = {}):
        self._pos = _pos
        self._dict = _dict
    
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

def dict2word(d):
    return Word(d['con'], d['nat'], d['pos'], d['ipa'], d['info'])

def pos2dict(p):
    return dict(abbr = p.abbr, pos = p.pos)

def dict2pos(d):
    return PoS(d['abbr'], d['pos'])

def copy(src):
    w = Word(src.con, src.nat, src.pos, src.ipa, src.info)
    return w

def save(dirL, doc):
    with open(dirL, 'w', encoding = 'utf-8') as f:
        f.write(str(dict(pos = [pos2dict(p) for p in doc.pos.values()], 
                         word = [word2dict(w) for w in doc.dic.values()])))

def load(dirL):
    doc = Document()
    with open(dirL, 'r', encoding = 'utf-8') as f:
        dictL = eval(f.read())
        doc.pos = dict([(d['abbr'], dict2pos(d)) for d in dictL['pos']])
        doc.dic = dict([(d['con'], dict2word(d)) for d in dictL['word']])
        return doc

def main():
    doc = Document()
    while True:
        op = input("> ")
        if op == "exit" or op == ";":
            break
        elif op == "del":
            con = input("con> ")
            if con not in doc.dic.keys():
                print("Word \"%s\" doesn't exist!" % con)
                continue
            del doc.dic[con]
        elif op == "save":
            file = input("file> ")
            if "." not in file:
                file += ".ln"
            save(file, doc)
        elif op == "load":
            file = input("file> ")
            if "." not in file:
                file += ".ln"
            doc = load(file)
        
        else:
            lis = op.split()
            if lis[0] == "pos":
                pos = input("pos> ")
                abbr = input("abbr> ")
                doc.pos[abbr] = PoS(abbr, pos)
            
            elif lis[0] == "add":
                con = input("con> ")
                nat = input("nat> ")
                pos, ipa, info = "", "", ""
                if lis[-1] == "-a":
                    pos = input("pos> ")
                    while pos != "" and pos not in doc.pos.keys():
                        print("Invalid part of speech, please input again or press enter to skip the process.")
                        pos = input("pos> ")
                    ipa = input("ipa> ")
                    info = input("def> ")
                doc.dic[con] = Word(con, nat, pos, ipa, info)
            
            elif lis[0] == "adj":
                con = input("con> ")
                if con not in doc.dic.keys():
                    print("Word \"%s\" doesn't exist!" % con)
                    continue
                w = copy(doc.dic[con])
                del doc.dic[con]
                ncon = input("new con> ")
                if ncon == "\\":
                    ncon = con
                nnat = input("new nat> ")
                npos, nipa, ninfo = "\\", "\\", "\\"
                if lis[-1] == "-a":
                    npos = input("new pos> ")
                    while npos != "\\" and npos not in doc.pos.keys():
                        print("Invalid part of speech, please input again or input \\ to skip the process.")
                        npos = input("new pos> ")
                    nipa = input("new ipa> ")
                    ninfo = input("new def> ")
                w.reset(ncon, nnat, npos, nipa, ninfo)
                doc.dic[ncon] = w
            
            elif lis[0] == "echo":
                con = input("con> ")
                if con not in doc.dic.keys():
                    print("Word \"%s\" doesn't exist!" % con)
                    continue
                print(doc.dic[con])

if __name__ == '__main__':
    main()