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
        self.intro = 'Lunaph 0.2.0 Alpha (Jan 18 2021)\nType "help" or "?" for help documents.'
        self.prompt = 'lexicon$ '
        self.modified = False
        self.cur = 'lex'
        self.lex = {}
        self.pos = {}
        self.alias = dict(lex = {';': 'exit', 
                                 '+': 'add -n', 
                                 '=': 'adj -c -n'}, 
                          pos = {';': 'exit', 
                                 '+': 'add -p', 
                                 '=': 'adj -p -a'})
    
    def precmd(self, line):
        args = shlex.split(line)
        if self.cur == 'lex':
            line = ' '.join([self.alias['lex'][a] if a in self.alias['lex'].keys() else a for a in args])
        elif self.cur == 'pos':
            line = ' '.join([self.alias['pos'][a] if a in self.alias['pos'].keys() else a for a in args])
        return line
    
    def do_save(self, dirL):
        if dirL == '':
            dirL = input('file> ')
        if '.' not in dirL:
            dirL += '.ln'
        with open(dirL, 'w', encoding = 'utf-8') as f:
            f.write(str(dict(pos = [p.to_dict() for p in self.pos.values()], 
                             word = [w.to_dict() for w in self.lex.values()], 
                             alias = self.alias)))
            self.modified = False
    
    def help_save(self):
        print('You can save your records by inputting an absolute/relative path (with a file name) \
after the prompt "file> ". If you don\'t include an extension, it will be the default ".ln".')
    
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
            self.lex = dict([(d['con'], Word(**d)) for d in dictL['word']])
            self.alias['lex'].update(dictL['alias']['lex'])
            self.alias['pos'].update(dictL['alias']['pos'])
    
    def help_load(self):
        print('You can load your records by inputting an absolute/relative path (with a file name) \
after the prompt "file> ". If you don\'t include an extension, it will be the default ".ln".')
    
    def cat_word(self, con):
        if con == '':
            con = input('word> ')
        if con in self.lex.keys():
            print(self.lex[con])
        else:
            print('Word "%s" doesn\'t exist!' % con)
    
    def cat_pos(self, abbr):
        if abbr == '':
            abbr = input('abbr> ')
        if abbr in self.pos.keys():
            print(self.pos[abbr])
        else:
            print('Abbreviation "%s" doesn\'t exist!' % abbr)
    
    def do_cat(self, line):
        if self.cur == 'lex':
            self.cat_word(line)
        elif self.cur == 'pos':
            self.cat_pos(line)
    
    def help_cat(self):
        print('In lexicon: By inputting an existing word, you can see the full information of the word.')
        print('In part of speech: By inputting the abbreviation of an existing part of speech, you can see the full information of it.')
    
    def add_word(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            con = args[-1]
        else:
            con = input('word> ')
        d['con'] = con
        if '-n' in args or '--nat' in args:
            d['nat'] = input('meaning> ')
        if '-p' in args or '--pos' in args:
            pos = input('part of speech> ')
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
                pos = input('part of speech> ')
            d['pos'] = pos
        if '-i' in args or '--ipa' in args:
            d['ipa'] = input('spelling> ')
        if '-d' in args or '--def' in args:
            d['info'] = input('definition> ')
        self.lex[con] = Word(**d)
        self.modified = True
    
    def add_pos(self, line):
        args = shlex.split(line)
        d = {}
        if '-p' in args or '--pos' in args:
            d['pos'] = input('part of speech> ')
        if len(args) > 0 and args[-1][0] != '-':
            abbr = args[-1]
        else:
            abbr = input('abbreviation> ')
        d['abbr'] = abbr
        if '-t' in args or '--pat' in args:
            d['pat'] = input('type pattern> ')
        if '-i' in args or '--info' in args:
            d['info'] = input('information> ')
        self.pos[abbr] = PoS(**d)
        self.modified = True
    
    def do_add(self, line):
        args = shlex.split(line)
        if self.cur == 'lex':
            if line == '' or args[0][0] != '-':
                line = '-n -p -i -d ' + line
            self.add_word(line)
        elif self.cur == 'pos':
            if line == '' or args[0][0] != '-':
                line = '-p -t -i ' + line
            self.add_pos(line)
    
    def help_add(self):
        print('In lexicon:')
        print('Alias "+" is the simple mode to add new words. You may input the word (e.g. "lunaph") \
after the prompt "word> " (or input "+ lunaph" at the beginning) and input the meaning(s) after the prompt \
"meaning> ". If you input "add" at the beginning (without any flag) and you can set the (abbreviation of the) \
part of speech, spelling and detailed definition after inputting the word and its meaning. If you want to \
skip one of the processes, just press enter at the corresponding prompt. If your word doesn\'t match the \
enforced pattern of your part of speech, you can override the lexical rules by inputting "y".')
        print('You can also customize the input contents by these flags:')
        print('"-n" or "--nat" for natlang synonyms (meanings)')
        print('"-p" or "--pos" for part of speech')
        print('"-i" or "--ipa" for spelling')
        print('"-d" or "--def" for definition')
        print('Therefore, "+" is equivalent to "add -n", and "add" is actually "add -n -p -i -d".\n')
        print('In part of speech:')
        print('By inputting "+" (or "+ <abbr>"), you can set some parts of speech. You may input a full name \
(e.g. "noun") after the prompt "part of speech> " and input a abbreviation (e.g. "n") after the prompt \
"abbreviation> ". If you input "add" at the beginning (or "add <abbr>") and you can set the type pattern \
and more information after inputting the part of speech and its abbreviation. If you want to skip one of the \
processes, just press enter at the corresponding prompt.')
        print('The type pattern of a part of speech is a regular expression that the words must match. \
For instance, the word "viro" matches the regular expression "o$" or ".*o$" et cetera.')
        print('You can also customize the input contents by these flags:')
        print('"-p" or "--pos" for the full name of the part of speech')
        print('"-t" or "--pat" for the type pattern of the part of speech')
        print('"-i" or "--info" for the information of the part of speech')
        print('Therefore, "+" is equivalent to "add -p", and "add" is actually "add -p -t -i".')
    
    def adj_word(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            con = args[-1]
        else:
            con = input('word> ')
        if con not in self.lex.keys():
            print('Word "%s" doesn\'t exist!' % con)
            return
        w = Word(**self.lex[con].to_dict()) # copy a word
        del self.lex[con]
        if '-c' in args or '--con' in args:
            ncon = input('new word> ')
            if ncon != '':
                con = ncon
        d['con'] = con
        if '-n' in args or '--nat' in args:
            d['nat'] = input('new meaning> ')
        if '-p' in args or '--pos' in args:
            pos = input('new part of speech> ')
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
                pos = input('new part of speech> ')
            d['pos'] = pos
        if '-i' in args or '--ipa' in args:
            d['ipa'] = input('new spelling> ')
        if '-d' in args or '--def' in args:
            d['info'] = input('new definition> ')
        w.reset(**d)
        self.lex[con] = w
        self.modified = True
    
    def adj_pos(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            abbr = args[-1]
        else:
            abbr = input('abbreviation> ')
        if abbr not in self.pos.keys():
            print('Abbreviation "%s" doesn\'t exist!' & abbr)
            return
        p = PoS(**self.pos[abbr].to_dict()) # copy a part of speech
        del self.pos[abbr]
        if '-p' in args or '--pos' in args:
            d['pos'] = input('new part of speech> ')
        if '-a' in args or '--abbr' in args:
            nabbr = input('new abbreviation> ')
            if nabbr != '':
                abbr = nabbr
        d['abbr'] = abbr
        if '-t' in args or '--pat' in args:
            d['pat'] = input('new type pattern> ')
        if '-i' in args or '--info' in args:
            d['info'] = input('new information> ')
        p.reset(**d)
        self.pos[abbr] = p
        self.modified = True
    
    def do_adj(self, line):
        args = shlex.split(line)
        if self.cur == 'lex':
            if line == '' or args[0][0] != '-':
                line = '-c -n -p -i -d ' + line
            self.adj_word(line)
        elif self.cur == 'pos':
            if line == '' or args[0][0] != '-':
                line = '-p -a -t -i ' + line
            self.adj_pos(line)
    
    def help_adj(self):
        print('In lexicon:')
        print('Alias "=" is the simple mode to adjust the existing words. After inputting the word you want \
to adjust, you can set the new word and new meanings. If you input "adj" at the beginning (or "adj <word>") \
and you can set the new part of speech, spelling and definition after setting the word and its meaning. If you \
want to skip one of the processes, please press enter after the corresponding prompt. Note that inputting "\\" \
will delete the corresponding record.')
        print('You can also customize the input contents by these flags:')
        print('"-c" or "--con" for modifying the conword')
        print('"-n" or "--nat" for modifying natlang synonyms (meanings)')
        print('"-p" or "--pos" for modifying the part of speech')
        print('"-i" or "--ipa" for modifying the spelling')
        print('"-d" or "--def" for modifying the definition')
        print('Therefore, "=" is equivalent to "adj -c -n", and "adj" is actually "add -c -n -p -i -d".\n')
        print('In part of speech:')
        print('Alias "=" is the simple mode to adjust the existing parts of speech. After inputting the \
abbreviation of the part of speech you want to adjust, you can set the new name and the new abbreviation. \
If you input "adj" at the beginning (or "adj <abbr>") and you can set the new type pattern and extra \
information after setting the name and its abbreviation. If you want to skip one of the processes, please \
press enter after the corresponding prompt. Note that inputting "\\" will delete the corresponding record.')
        print('You can also customize the input contents by these flags:')
        print('"-a" or "--abbr" for modifying the abbreviation')
        print('"-p" or "--pos" for modifying the full name of the part of speech')
        print('"-t" or "--pat" for modifying the type pattern of the part of speech')
        print('"-i" or "--info" for modifying the information of the part of speech')
        print('Therefore, "=" is equivalent to "adj -a -p", and "adj" is actually "adj -a -p -t -i".')
    
    def del_word(self, con):
        if con == '':
            con = input('word> ')
        if con in self.lex.keys():
            del self.lex[con]
            self.modified = True
        else:
            print('Word "%s" doesn\'t exist!' % con)
        
    def del_pos(self, abbr):
        if abbr == '':
            abbr = input('abbreviation> ')
        if abbr in self.pos.keys():
            del self.pos[abbr]
            self.modified = True
        else:
            print('Abbreviation "%s" doesn\'t exist!' % abbr)
    
    def do_del(self, line):
        if self.cur == 'lex':
            self.del_word(line)
        elif self.cur == 'pos':
            self.del_pos(line)
    
    def help_del(self):
        print('In lexicon: You can delete an existing word by inputting the word.')
        print('In part of speech: You can delete an existing part of speech by inputting the abbreviation.')
    
    def do_alias(self, line):
        args = shlex.split(line)
        gl = True if '-g' in args or '--global' in args else False
        if len(args) > 1:
            alias = args[-2]
            txt = args[-1]
        else:
            alias = input('alias> ')
            txt = input('replace text> ')
        if gl or self.cur == 'lex':
            self.alias['lex'][alias] = txt
        if gl or self.cur == 'pos':
            self.alias['pos'][alias] = txt
        self.modified = True
    
    def help_alias(self):
        print('By inputting the alias and the text you want to replace, you can simplify the commands you \
use regularly. For instance, by setting "alias ct cat" in "part of speech", you can type "ct <abbr>" instead \
of "cat <abbr>" to see the full information of the part of speech. Note that your aliases only work in the \
directory where you set it. Thus, the alias above won\'t work when you are in "lexicon". To set global \
aliases, you can add the flag "-g" or "--global".')
    
    def do_cd(self, line):
        if line == 'lex' or line == 'lexicon':
            self.cur = 'lex'
            self.prompt = 'lexicon$ '
        elif line == 'pos' or line == 'part of speech':
            self.cur = 'pos'
            self.prompt = 'part of speech$ '
    
    def help_cd(self):
        print('You can switch the directory by "cd lex" and "cd pos".')
    
    def do_ls(self, line):
        args = shlex.split(line)
        if self.cur == 'lex':
            if '-a' in args or '--alias' in args:
                print('\n'.join([k + '\t' + v for k, v in self.alias['lex'].items()]))
            else:
                print('\t'.join(sorted(self.lex.keys())))
        elif self.cur == 'pos':
            if '-a' in args or '--alias' in args:
                print('\n'.join([k + '\t' + v for k, v in self.alias['pos'].items()]))
            else:
                print('\t'.join(sorted(self.pos.keys())))
    
    def help_ls(self):
        print('In lexicon: "ls" will list all the words in your lexicon.')
        print('In part of speech: "ls" will list all the parts of speech.')
        print('After adding "-a" or "--alias", "ls" will list all the aliases \
(both global aliases and aliases available in your current directory.')
    
    def do_exit(self, line):
        if self.modified:
            chc = input('Save? [y/n]')
            if chc == 'y':
                self.do_save('')
        return True
    
    def help_exit(self):
        print('You can exit Lunaph by "exit" or ";".')
    
    def emptyline(self):
        pass
    
    def default(self, line):
        print('Unknown command: %s' % line)

def main():
    try:
        Lunaph().cmdloop()
    except KeyboardInterrupt:
        pass
    
if __name__ == '__main__':
    main()