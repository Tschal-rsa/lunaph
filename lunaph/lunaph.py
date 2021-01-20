#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 16:31:53 2021

@author: lfz
"""

import cmd
import shlex
import re


class Focloir(dict):
    def __delitem__(self, key):
        value = super().pop(key)
        super().pop(value, None)

    def __setitem__(self, key, value):
        if value == '':
            if key not in self.keys():
                super().__setitem__(key, value)
        else:
            if value == '\\':
                value = ''
            super().__setitem__(key, value)

    def reset(self, **kw):
        for k in kw.keys():
            self.__setitem__(k, kw[k])

    def to_dict(self):
        return dict(self.items())


class PoS(Focloir):
    def __init__(self, *, abbr, pos='', pat='.*', info='', **kw):
        super().__init__(abbr=abbr, pos=pos, pat=pat, info=info, **kw)

    def __str__(self):
        return '\nPart of Speech:\t%s\nAbbreviation:\t%s\nInformation:\t%s\nType Pattern:\t%s\n' % (
            self['pos'], self['abbr'], self['info'], self['pat'])


class Word(Focloir):
    def __init__(self, *, con, nat='', pos='', ipa='', info='', **kw):
        super().__init__(con=con, nat=nat, pos=pos, ipa=ipa, info=info, **kw)

    def __str__(self):
        return '\nWord:\t\t%s\nMeaning(s):\t%s\nPart of Speech:\t%s\nSpelling:\t%s\nDefinition:\t%s\n' % (
            self['con'], self['nat'], self['pos'], self['ipa'], self['info'])


class Lunaph(cmd.Cmd):
    def __init__(self):
        super(Lunaph, self).__init__()
        self.intro = 'Lunaph 0.2.1 Alpha (Jan 20 2021)\nType "help" or "?" for help documents.'
        self.prompt = 'lexicon$ '
        self.modified = False
        self.cur = 'lex'
        self.doc = dict(lex={}, pos={})
        self.alias = dict(lex={
            ';': 'exit',
            '+': 'add -n',
            '=': 'adj -c -n'
        },
                          pos={
                              ';': 'exit',
                              '+': 'add -p',
                              '=': 'adj -p -a'
                          })
        with open('help.txt', 'r') as f:
            self.help = eval(f.read())

    def precmd(self, line):
        args = shlex.split(line)
        # The 4 lines below can be replaced as:
        line = ' '.join([
            self.alias[self.cur][a] if a in self.alias[self.cur].keys() else a
            for a in args
        ])
        return line

    def do_save(self, dirL):
        if dirL == '':
            dirL = input('file> ')
        if '.' not in dirL:
            dirL += '.ln'
        with open(dirL, 'w', encoding='utf-8') as f:
            f.write(
                str(
                    dict(pos=[p.to_dict() for p in self.doc['pos'].values()],
                         word=[w.to_dict() for w in self.doc['lex'].values()],
                         alias=self.alias)))
            self.modified = False

    def help_save(self):
        print(self.help['save'])

    def do_load(self, dirL):
        if self.modified:
            chc = input('Save? [y/n] ')
            if chc == 'y':
                self.do_save('')
        if dirL == '':
            dirL = input('file> ')
        if '.' not in dirL:
            dirL += '.ln'
        with open(dirL, 'r', encoding='utf-8') as f:
            dictL = eval(f.read())
            self.doc['pos'] = dict([(d['abbr'], PoS(**d))
                                    for d in dictL['pos']])
            self.doc['lex'] = dict([(d['con'], Word(**d))
                                    for d in dictL['word']])
            self.alias['lex'].update(dictL['alias']['lex'])
            self.alias['pos'].update(dictL['alias']['pos'])
            self.modified = False

    def help_load(self):
        print(self.help['load'])

    def do_cat(self, line):
        if line == '':
            if self.cur == 'lex':
                line = input('word> ')
            elif self.cur == 'pos':
                line = input('abbr> ')
        if line in self.doc[self.cur].keys():
            print(self.doc[self.cur][line])
        else:
            if self.cur == 'lex':
                print('Word "%s" doesn\'t exist!' % line)
            elif self.cur == 'pos':
                print('Abbreviation "%s" doesn\'t exist!' % line)

    def help_cat(self):
        print(self.help['cat'])

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
                if pos in self.doc['pos'].keys():
                    if re.search(self.doc['pos'][pos]['pat'], con) is None:
                        print(
                            'The word doesn\'t match the enforced pattern for type: %s. Do you want to override lexical rules? [y/n] '
                            % self.doc['pos'][pos]['pos'])
                        chc = input()
                        if chc == 'y':
                            break
                    else:
                        break
                else:
                    print(
                        'Invalid part of speech, please input again or press enter to skip the process.'
                    )
                pos = input('part of speech> ')
            d['pos'] = pos
        if '-i' in args or '--ipa' in args:
            d['ipa'] = input('spelling> ')
        if '-d' in args or '--def' in args:
            d['info'] = input('definition> ')
        self.doc['lex'][con] = Word(**d)
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
        self.doc['pos'][abbr] = PoS(**d)
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
        print(self.help['add'])

    def adj_word(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            con = args[-1]
        else:
            con = input('word> ')
        if con not in self.doc['lex'].keys():
            print('Word "%s" doesn\'t exist!' % con)
            return
        w = Word(**self.doc['lex'][con].to_dict())  # copy a word
        del self.doc['lex'][con]
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
                if pos in self.doc['pos'].keys():
                    if re.search(self.doc['pos'][pos]['pat'], con) is None:
                        print(
                            'The word doesn\'t match the enforced pattern for type: %s. Do you want to override lexical rules? [y/n] '
                            % self.doc['pos'][pos]['pos'])
                        chc = input()
                        if chc == 'y':
                            break
                    else:
                        break
                else:
                    print(
                        'Invalid part of speech, please input again or press enter to skip the process.'
                    )
                pos = input('new part of speech> ')
            d['pos'] = pos
        if '-i' in args or '--ipa' in args:
            d['ipa'] = input('new spelling> ')
        if '-d' in args or '--def' in args:
            d['info'] = input('new definition> ')
        w.reset(**d)
        self.doc['lex'][con] = w
        self.modified = True

    def adj_pos(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            abbr = args[-1]
        else:
            abbr = input('abbreviation> ')
        if abbr not in self.doc['pos'].keys():
            print('Abbreviation "%s" doesn\'t exist!' & abbr)
            return
        p = PoS(**self.doc['pos'][abbr].to_dict())  # copy a part of speech
        del self.doc['pos'][abbr]
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
        self.doc['pos'][abbr] = p
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
        print(self.help['adj'])

    def do_del(self, line):
        if line == '':
            if self.cur == 'lex':
                line = input('word> ')
            elif self.cur == 'pos':
                line = input('abbreviation> ')
        if line in self.doc[self.cur].keys():
            del self.doc[self.cur][line]
            self.modified = True
        else:
            if self.cur == 'lex':
                print('Word "%s" doesn\'t exist!' % line)
            elif self.cur == 'pos':
                print('Abbreviation "%s" doesn\'t exist!' % line)

    def help_del(self):
        print(self.help['del'])

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
        print(self.help['alias'])

    def do_cd(self, line):
        if line == 'lex' or line == 'lexicon':
            self.cur = 'lex'
            self.prompt = 'lexicon$ '
        elif line == 'pos' or line == 'part of speech':
            self.cur = 'pos'
            self.prompt = 'part of speech$ '

    def help_cd(self):
        print(self.help['cd'])

    def do_ls(self, line):
        args = shlex.split(line)
        if '/' in args:
            print('\t'.join(sorted(self.doc.keys())))
        elif '-a' in args or '--alias' in args:
            print('\n'.join(
                [k + '\t' + v for k, v in self.alias[self.cur].items()]))
        else:
            print('\t'.join(sorted(self.doc[self.cur].keys())))

    def help_ls(self):
        print(self.help['ls'])

    def do_exit(self, line):
        if self.modified:
            chc = input('Save? [y/n] ')
            if chc == 'y':
                self.do_save('')
        return True

    def help_exit(self):
        print(self.help['exit'])

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
