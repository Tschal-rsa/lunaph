# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 16:31:53 2021

@author: lfz
"""

import cmd, sys, shlex, re

class PoS(object):
    def __init__(self, *, abbr, pos = '', pat = '.*', info = ''):
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
    
    def to_dict(self):
        return dict(abbr = self.abbr, pos = self.pos, pat = self.pat, info = self.info)
    
    def __str__(self):
        return '\nPart of Speech:\t%s\nAbbreviation:\t%s\nInformation:\t%s\nType Pattern:\t%s' %(self.pos, self.abbr, self.info, self.pat)

class Word(object):
    def __init__(self, *, con, nat = '', pos = '', ipa = '', info = ''):
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
    
    def to_dict(self):
         return dict(con = self.con, nat = self.nat, pos = self.pos, ipa = self.ipa, info = self.info)
    
    def __str__(self):
        return '\nWord:\t\t\t%s\nMeaning(s):\t\t%s\nPart of Speech:\t%s\nSpelling:\t\t%s\nDefinition:\t\t%s' %(self.con, self.nat, self.pos, self.ipa, self.info)

class Lunaph(cmd.Cmd):
    def __init__(self):
        super(Lunaph, self).__init__()
        self.intro = 'Lunaph 0.1.0 Alpha'
        self.prompt = '> '
        self.pos = {}
        self.dic = {}
        self.alias = {';': 'exit', 
                      'd': 'add -n', 
                      '+': 'add -n -p -i -d', 
                      'dp': 'addp -p', 
                      '+p': 'addp -p -t -i', 
                      'j': 'adj -c -n', 
                      '=': 'adj -c -n -p -i -d', 
                      'jp': 'adjp -p -a', 
                      '=p': 'adjp -p -a -t -i'}
    
    def precmd(self, line):
        args = shlex.split(line)
        return ' '.join([self.alias[a] if a in self.alias.keys() else a for a in args])
    
    def do_save(self, dirL):
        if dirL == '':
            dirL = input('file> ')
        if '.' not in dirL:
            dirL += '.ln'
        with open(dirL, 'w', encoding = 'utf-8') as f:
            f.write(str(dict(pos = [p.to_dict() for p in self.pos.values()], 
                             word = [w.to_dict() for w in self.dic.values()], 
                             alias = self.alias)))
    
    def do_load(self, dirL):
        if dirL == '':
            dirL = input('file> ')
        if '.' not in dirL:
            dirL += '.ln'
        with open(dirL, 'r', encoding = 'utf-8') as f:
            dictL = eval(f.read())
            self.pos = dict([(d['abbr'], PoS(**d)) for d in dictL['pos']])
            self.dic = dict([(d['con'], Word(**d)) for d in dictL['word']])
            self.alias.update(dictL['alias'])
    
    def do_echo(self, con):
        if con == '':
            con = input('con> ')
        if con in self.dic.keys():
            print(self.dic[con])
        else:
            print('Word "%s" doesn\'t exist!' % con)
    
    def do_echop(self, abbr):
        if abbr == '':
            abbr = input('abbr> ')
        if abbr in self.pos.keys():
            print(self.pos[abbr])
        else:
            print('Abbreviation "%s" doesn\'t exist!' % abbr)
    
    def do_add(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            con = args[-1]
        else:
            con = input('con> ')
        d['con'] = con
        if '-n' in args or '--nat' in args:
            d['nat'] = input('nat> ')
        if '-p' in args or '--pos' in args:
            pos = input('pos> ')
            while pos != '':
                if pos in self.pos.keys():
                    if re.search(self.pos[pos].pat, con) is None:
                        chc = input(f'The word doesn\'t match the enforced pattern for type: {self.pos[pos].pos}. Do you want to override lexical rules? [y/n]')
                        if chc == 'y':
                            break
                    else:
                        break
                else:
                    print('Invalid part of speech, please input again or press enter to skip the process.')
                pos = input('pos> ')
            d['pos'] = pos
        if '-i' in args or '--ipa' in args:
            d['ipa'] = input('ipa> ')
        if '-d' in args or '--def' in args:
            d['info'] = input('def> ')
        self.dic[con] = Word(**d)
    
    def do_addp(self, line):
        args = shlex.split(line)
        d = {}
        if '-p' in args or '--pos' in args:
            d['pos'] = input('pos> ')
        if len(args) > 0 and args[-1][0] != '-':
            abbr = args[-1]
        else:
            abbr = input('abbr> ')
        d['abbr'] = abbr
        if '-t' in args or '--pat' in args:
            d['pat'] = input('pat> ')
        if '-i' in args or '--info' in args:
            d['info'] = input('info> ')
        self.pos[abbr] = PoS(**d)
    
    def do_adj(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            con = args[-1]
        else:
            con = input('con> ')
        if con not in self.dic.keys():
            print('Word "%s" doesn\'t exist!' % con)
            return
        w = Word(**self.dic[con].to_dict()) # copy a word
        del self.dic[con]
        if '-c' in args or '--con' in args:
            ncon = input('new con> ')
            if ncon != '':
                con = ncon
        d['con'] = con
        if '-n' in args or '--nat' in args:
            d['nat'] = input('new nat> ')
        if '-p' in args or '--pos' in args:
            pos = input('new pos> ')
            while pos != '' and pos != '\\':
                if pos in self.pos.keys():
                    if re.search(self.pos[pos].pat, con) is None:
                        chc = input(f'The word doesn\'t match the enforced pattern for type: {self.pos[pos].pos}. Do you want to override lexical rules? [y/n]')
                        if chc == 'y':
                            break
                    else:
                        break
                else:
                    print('Invalid part of speech, please input again or press enter to skip the process.')
                pos = input('new pos> ')
            d['pos'] = pos
        if '-i' in args or '--ipa' in args:
            d['ipa'] = input('new ipa> ')
        if '-d' in args or '--def' in args:
            d['info'] = input('new def> ')
        w.reset(**d)
        self.dic[con] = w
    
    def do_adjp(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            abbr = args[-1]
        else:
            abbr = input('abbr> ')
        if abbr not in self.pos.keys():
            print('Abbreviation "%s" doesn\'t exist!' & abbr)
            return
        p = PoS(**self.pos[abbr].to_dict()) # copy a part of speech
        del self.pos[abbr]
        if '-p' in args or '--pos' in args:
            d['pos'] = input('new pos> ')
        if '-a' in args or '--abbr' in args:
            nabbr = input('new abbr> ')
            if nabbr != '':
                abbr = nabbr
        d['abbr'] = abbr
        if '-t' in args or '--pat' in args:
            d['pat'] = input('new pat> ')
        if '-i' in args or '--info' in args:
            d['info'] = input('new info> ')
        p.reset(**d)
        self.pos[abbr] = p
    
    def do_del(self, con):
        if con == '':
            con = input('con> ')
        if con in self.dic.keys():
            del self.dic[con]
        else:
            print('Word "%s" doesn\'t exist!' % con)
        
    def do_delp(self, abbr):
        if abbr == '':
            abbr = input('abbr> ')
        if abbr in self.pos.keys():
            del self.pos[abbr]
        else:
            print('Abbreviation "%s" doesn\'t exist!' % abbr)
    
    def do_alias(self, line):
        args = shlex.split(line)
        if len(args) > 0:
            alias = args[0]
        else:
            alias = input('alias> ')
        if len(args) > 1:
            txt = args[1]
        else:
            txt = input('replace text')
        self.alias[alias] = txt
    
    def do_exit(self, line):
        sys.exit()
    
    def default(self, line):
        print('Unknown command: %s' % line)

def main():
    try:
        Lunaph().cmdloop()
    except KeyboardInterrupt:
        sys.exit()
    
if __name__ == '__main__':
    main()