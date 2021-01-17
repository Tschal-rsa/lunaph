# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 16:31:53 2021

@author: lfz
"""

import cmd, shlex, re

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
        self.intro = 'Lunaph 0.1.0 Alpha (Jan 18 2021)\nType "help" or "?" for more information.'
        self.prompt = '> '
        self.modified = False
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
            self.modified = False
    
    def help_save(self):
        print('You can save your records by inputting an absolute/relative path (with a file name) after the prompt "file> ". If you don\'t include an extension, it will be the default ".ln".')
    
    def do_load(self, dirL):
        if self.modified:
            chc = input('Save? [y/n]')
            if chc == 'y':
                self.do_save('')
        if dirL == '':
            dirL = input('file> ')
        if '.' not in dirL:
            dirL += '.ln'
        with open(dirL, 'r', encoding = 'utf-8') as f:
            dictL = eval(f.read())
            self.pos = dict([(d['abbr'], PoS(**d)) for d in dictL['pos']])
            self.dic = dict([(d['con'], Word(**d)) for d in dictL['word']])
            self.alias.update(dictL['alias'])
    
    def help_load(self):
        print('You can load your records by inputting an absolute/relative path (with a file name) after the prompt "file> ". If you don\'t include an extension, it will be the default ".ln".')
    
    def do_echo(self, con):
        if con == '':
            con = input('con> ')
        if con in self.dic.keys():
            print(self.dic[con])
        else:
            print('Word "%s" doesn\'t exist!' % con)
    
    def help_echo(self):
        print('By inputting an existing word, you can see the full information of the word.')
    
    def do_echop(self, abbr):
        if abbr == '':
            abbr = input('abbr> ')
        if abbr in self.pos.keys():
            print(self.pos[abbr])
        else:
            print('Abbreviation "%s" doesn\'t exist!' % abbr)
            
    def help_echop(self):
        print('By inputting the abbreviation of an existing part of speech, you can see the full information of it.')
    
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
        self.modified = True
        
    def help_add(self):
        print('Alias "d" is the simple mode to add new words. You may input the word (e.g. "lunaph") after the prompt "con> " (or input "d lunaph" at the beginning) and input the meaning(s) after the prompt "nat> ". There is also a complex mode to add new words. Input "+" at the beginning and you can set the part of speech ("pos> "), spelling ("ipa> ") and detailed definition ("def> ") after inputting the word and its meaning. If you want to skip one of the processes, just press enter at the corresponding prompt. If your word doesn\'t match the enforced pattern of your part of speech, you can override the lexical rules by inputting "y".')
        print('You can also customize the input contents by these flags:')
        print('"-n" or "--nat" for natlang synonyms (meanings)')
        print('"-p" or "--pos" for part of speech')
        print('"-i" or "--ipa" for spelling')
        print('"-d" or "--def" for definition')
        print('Therefore, "d" is equivalent to "add -n", and "+" is equivalent to "add -n -p -i -d".')
    
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
        self.modified = True
    
    def help_addp(self):
        print('By inputting "dp" (or "dp <abbr>"), you can set some parts of speech. You may input a full name (e.g. "noun") after the prompt "pos> " and input a abbreviation (e.g. "n") after the prompt "abbr> ". There is also a complex mode to add new parts of speech. Input "+p" at the beginning (or "+p <abbr>") and you can set the type pattern ("pat> ") and more information ("info> ") after inputting the part of speech and its abbreviation. If you want to skip one of the processes, just press enter at the corresponding prompt.')
        print('The type pattern of a part of speech is a regular expression that the words must match. For instance, the word "viro" matches the regular expression "o$" or ".*o$" et cetera.')
        print('You can also customize the input contents by these flags:')
        print('"-p" or "--pos" for the full name of the part of speech')
        print('"-t" or "--pat" for the type pattern of the part of speech')
        print('"-i" or "--info" for the information of the part of speech')
        print('Therefore, "dp" is equivalent to "addp -p", and "+p" is equivalent to "addp -p -t -i".')
    
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
        self.modified = True
    
    def help_adj(self):
        print('Alias "j" is the simple mode to adjust the existing words. After inputting the word you want to adjust, you can set the new word and new meanings. There is also a complex mode to adjust words. Input "=" at the beginning (or "= <word>") and you can set the new part of speech, spelling and definition after setting the word and its meaning. If you want to skip one of the processes, please press enter after the corresponding prompt. Note that inputting "\\" will delete the corresponding record.')
        print('You can also customize the input contents by these flags:')
        print('"-c" or "--con" for modifying the conword')
        print('"-n" or "--nat" for modifying natlang synonyms (meanings)')
        print('"-p" or "--pos" for modifying the part of speech')
        print('"-i" or "--ipa" for modifying the spelling')
        print('"-d" or "--def" for modifying the definition')
        print('Therefore, "j" is equivalent to "adj -c -n", and "=" is equivalent to "add -c -n -p -i -d".')
    
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
        self.modified = True
    
    def help_adjp(self):
        print('Alias "jp" is the simple mode to adjust the existing parts of speech. After inputting the abbreviation of the part of speech you want to adjust, you can set the new name and the new abbreviation. There is also a complex mode to adjust words. Input "=p" at the beginning (or "=p <abbr>") and you can set the new type pattern and extra information after setting the name and its abbreviation. If you want to skip one of the processes, please press enter after the corresponding prompt. Note that inputting "\\" will delete the corresponding record.')
        print('You can also customize the input contents by these flags:')
        print('"-a" or "--abbr" for modifying the abbreviation')
        print('"-p" or "--pos" for modifying the full name of the part of speech')
        print('"-t" or "--pat" for modifying the type pattern of the part of speech')
        print('"-i" or "--info" for modifying the information of the part of speech')
        print('Therefore, "jp" is equivalent to "adjp -a -p", and "=p" is equivalent to "addp -a -p -t -i".')
    
    def do_del(self, con):
        if con == '':
            con = input('con> ')
        if con in self.dic.keys():
            del self.dic[con]
            self.modified = True
        else:
            print('Word "%s" doesn\'t exist!' % con)
    
    def help_del(self):
        print('You can delete an existing word by inputting the word.')
        
    def do_delp(self, abbr):
        if abbr == '':
            abbr = input('abbr> ')
        if abbr in self.pos.keys():
            del self.pos[abbr]
            self.modified = True
        else:
            print('Abbreviation "%s" doesn\'t exist!' % abbr)
    
    def help_delp(self):
        print('You can delete an existing part of speech by inputting the abbreviation.')
    
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
        self.modified = True
    
    def help_alias(self):
        print('By inputting the alias and the text you want to replace, you can simplify the commands you use regularly.')
    
    def do_exit(self, line):
        if self.modified:
            chc = input('Save? [y/n]')
            if chc == 'y':
                self.do_save('')
        return True
    
    def help_exit(self):
        print('You can exit Lunaph by "exit" or ";".')
    
    def default(self, line):
        print('Unknown command: %s' % line)

def main():
    try:
        Lunaph().cmdloop()
    except KeyboardInterrupt:
        pass
    
if __name__ == '__main__':
    main()