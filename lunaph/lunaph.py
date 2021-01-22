#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 16:31:53 2021

@author: lfz
"""

import cmd
import shlex
import re
import os
from pyecharts.charts import Tree
from pyecharts import options as opts
import xlrd
import xlwt


class Focloir(dict):
    """
    def __delitem__(self, key):
        value = super().pop(key)
        super().pop(value, None)
    """

    def __setitem__(self, key, value):
        if not value:
            if key not in self.keys():
                super().__setitem__(key, value)
        else:
            if value == '\\':
                value = ''
            elif type(value) == list:
                value.extend(self.__getitem__(key))
                value = list(set(value))
            elif type(value) == dict:
                value.update(self.__getitem__(key))
            super().__setitem__(key, value)

    def reset(self, **kw):
        for k in kw.keys():
            self.__setitem__(k, kw[k])

    def to_dict(self):
        return {k: v for k, v in self.items() if v}


class PoS(Focloir):
    def __init__(self, *, abbr, pos='', pat='.*', info='', **kw):
        super().__init__(abbr=abbr, pos=pos, pat=pat, info=info, **kw)

    def __str__(self):
        return '\nPart of Speech:\t%s\nAbbreviation:\t%s\nInformation:\t%s\nType Pattern:\t%s\n' % (
            self['pos'], self['abbr'], self['info'], self['pat'])


class Word(Focloir):
    def __init__(self, *, con, nat='', pos='', ipa='', info='', ip=None, ep=None, **kw):
        if ip is None:
            ip = []
        if ep is None:
            ep = {}
        super().__init__(con=con, nat=nat, pos=pos, ipa=ipa, info=info, ip=ip, ep=ep, **kw)

    def __str__(self):
        return '\nWord:\t\t%s\nMeaning(s):\t%s\nPart of Speech:\t%s\nSpelling:\t%s\nDefinition:\t%s\n' % (
            self['con'], self['nat'], self['pos'], self['ipa'], self['info'])

    def etym(self):
        return '\nInternal parents: {}\nExternal parents: {}\n'.format(', '.join(self.__getitem__('ip')), ', '.join(self.__getitem__('ep').keys()))


class Lunaph(cmd.Cmd):
    def __init__(self):
        super(Lunaph, self).__init__()
        self.intro = 'Lunaph 0.3.0 Alpha (Jan 22 2021)\nType "help" or "?" for help documents.'
        self.prompt = '/Lexicon$ '
        self.modified = False
        self.cur = 'lex'
        self.doc = dict(lex=dict(title='Lexicon',
                                 content={},
                                 alias={
                                     ';': 'exit',
                                     '+': 'add -n',
                                     '=': 'adj -c -n'
                                 }),
                        pos=dict(title='Parts of Speech',
                                 content={},
                                 alias={
                                     ';': 'exit',
                                     '+': 'add -p',
                                     '=': 'adj -p -a'
                                 }),
                        pro=dict(title='Properties',
                                 content=dict(name=''),
                                 alias={';': 'exit'}))
        with open('help.txt', 'r') as f:
            self.help = eval(f.read())

    def precmd(self, line):
        args = shlex.split(line)
        # The 4 lines below can be replaced as:
        line = ' '.join([
            self.doc[self.cur]['alias'][a]
            if a in self.doc[self.cur]['alias'].keys() else a for a in args
        ])
        return line

    def do_save(self, dirL):
        if dirL == '':
            dirL = input('file> ')
        if '.' not in dirL:
            dirL += '.ln'
        temp_dict = dict(**self.doc)
        temp_dict['pos']['content'] = [
            p.to_dict() for p in self.doc['pos']['content'].values()
        ]
        temp_dict['lex']['content'] = [
            w.to_dict() for w in self.doc['lex']['content'].values()
        ]
        with open(dirL, 'w', encoding='utf-8') as f:
            f.write(str(temp_dict))
            self.modified = False
            del temp_dict

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
            self.doc = dict(**dictL)
            self.doc['pos']['content'] = dict([
                (d['abbr'], PoS(**d)) for d in dictL['pos']['content']
            ])
            self.doc['lex']['content'] = dict([
                (d['con'], Word(**d)) for d in dictL['lex']['content']
            ])
            #           self.alias['lex'].update(dictL['alias']['lex'])
            #           self.alias['pos'].update(dictL['alias']['pos'])
            self.modified = False
            self.prompt = self.doc['pro']['content']['name'] + \
                '/' + self.doc[self.cur]['title'] + '$ '
            del dictL

    def help_load(self):
        print(self.help['load'])

    def do_cat(self, line):
        if line == '':
            if self.cur == 'lex':
                line = input('word> ')
            elif self.cur == 'pos':
                line = input('abbr> ')
            else:
                line = input('name> ')
        if line in self.doc[self.cur]['content'].keys():
            print(self.doc[self.cur]['content'][line])
        else:
            if self.cur == 'lex':
                print('Word "%s" doesn\'t exist!' % line)
            elif self.cur == 'pos':
                print('Abbreviation "%s" doesn\'t exist!' % line)
            else:
                print('File "%s" doesn\'t exist!' % line)

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
                if pos in self.doc['pos']['content'].keys():
                    if re.search(self.doc['pos']['content'][pos]['pat'],
                                 con) is None:
                        print(
                            'The word doesn\'t match the enforced pattern for type: %s. Do you want to override lexical rules? [y/n] '
                            % self.doc['pos']['content'][pos]['pos'])
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
        if '-I' in args or '--ip' in args:
            ip = input('internal parent> ')
            while ip not in self.doc['lex']['content'].keys():
                print(
                    'Invalid word, please input again or press enter to skip the process.')
                ip = input('internal parent> ')
            d['ip'] = [ip]
            #d['ip'].append(input('internal parent> '))
        if '-E' in args or '--ep' in args:
            pcon = input('external parent> ')
            d['ep'] = {pcon: {}}
            d['ep'][pcon]['nat'] = input('meaning> ')
            d['ep'][pcon]['lan'] = input('source language> ')
        self.doc['lex']['content'][con] = Word(**d)
        self.modified = True
        del d

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
        self.doc['pos']['content'][abbr] = PoS(**d)
        self.modified = True
        del d

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
        if con not in self.doc['lex']['content'].keys():
            print('Word "%s" doesn\'t exist!' % con)
            return
        w = Word(**self.doc['lex']['content'][con].to_dict())  # copy a word
        del self.doc['lex']['content'][con]
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
                if pos in self.doc['pos']['content'].keys():
                    if re.search(self.doc['pos']['content'][pos]['pat'],
                                 con) is None:
                        print(
                            'The word doesn\'t match the enforced pattern for type: %s. Do you want to override lexical rules? [y/n] '
                            % self.doc['pos']['content'][pos]['pos'])
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
        if '-I' in args or '--ip' in args:
            ip = input('new internal parent> ')
            while ip not in self.doc['lex']['content'].keys():
                print(
                    'Invalid word, please input again or press enter to skip the process.')
                ip = input('new internal parent> ')
            d['ip'] = [ip]
            #d['ip'].append(input('internal parent> '))
        if '-E' in args or '--ep' in args:
            pcon = input('new external parent> ')
            d['ep'] = {pcon: {}}
            d['ep'][pcon]['nat'] = input('new meaning> ')
            d['ep'][pcon]['lan'] = input('new source language> ')
        w.reset(**d)
        self.doc['lex']['content'][con] = w
        self.modified = True
        del d

    def adj_pos(self, line):
        args = shlex.split(line)
        d = {}
        if len(args) > 0 and args[-1][0] != '-':
            abbr = args[-1]
        else:
            abbr = input('abbreviation> ')
        if abbr not in self.doc['pos']['content'].keys():
            print('Abbreviation "%s" doesn\'t exist!' & abbr)
            return
        # copy a part of speech
        p = PoS(**self.doc['pos']['content'][abbr].to_dict())
        del self.doc['pos']['content'][abbr]
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
        self.doc['pos']['content'][abbr] = p
        self.modified = True
        del d

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
        args = shlex.split(line)
        if '-I' in args or '--ip' in args:
            if len(args) > 1:
                con = args[1]
            else:
                con = input('word> ')
            if len(args) > 2:
                pcon = args[2]
            else:
                pcon = input('internal parent> ')
            if con in self.doc['lex']['content'].keys():
                if pcon in self.doc['lex']['content'][con]['ip']:
                    self.doc['lex']['content'][con]['ip'].remove(pcon)
                    self.modified = True
                else:
                    print(
                        'Word "%s" doesn\'t have the internal parent "%s"!' % (con, pcon))
            else:
                print('Word "%s" doesn\'t exist!' % con)
        elif '-E' in args or '--ep' in args:
            if len(args) > 1:
                con = args[1]
            else:
                con = input('word> ')
            if len(args) > 2:
                pcon = args[2]
            else:
                pcon = input('external parent> ')
            if con in self.doc['lex']['content'].keys():
                if pcon in self.doc['lex']['content'][con]['ep'].keys():
                    del self.doc['lex']['content'][con]['ep'][pcon]
                    self.modified = True
                else:
                    print(
                        'Word "%s" doesn\'t have the external parent "%s"!' % (con, pcon))
            else:
                print('Word "%s" doesn\'t exist!' % con)
        else:
            if line == '':
                if self.cur == 'lex':
                    line = input('word> ')
                elif self.cur == 'pos':
                    line = input('abbreviation> ')
                else:
                    line = input('name> ')
            if line in self.doc[self.cur]['content'].keys():
                del self.doc[self.cur]['content'][line]
                self.modified = True
            else:
                if self.cur == 'lex':
                    print('Word "%s" doesn\'t exist!' % line)
                elif self.cur == 'pos':
                    print('Abbreviation "%s" doesn\'t exist!' % line)
                else:
                    print('File "%s" doesn\'t exist!' % line)

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
        if gl:
            for k in self.doc.keys():
                self.doc[k]['alias'][alias] = txt
        else:
            self.doc[self.cur]['alias'][alias] = txt
        self.modified = True

    def help_alias(self):
        print(self.help['alias'])

    def do_cd(self, line):
        """
        if line == 'lex' or line == 'lexicon':
            self.cur = 'lex'
            self.prompt = 'lexicon$ '
        elif line == 'pos' or line == 'part of speech':
            self.cur = 'pos'
            self.prompt = 'part of speech$ '
        """
        self.cur = line
        self.prompt = self.doc['pro']['content']['name'] + \
            '/' + self.doc[self.cur]['title'] + '$ '

    def help_cd(self):
        print(self.help['cd'])

    def do_ls(self, line):
        args = shlex.split(line)
        if '/' in args:
            print('\n'.join([self.doc[k]['title'] +
                             '\t' + k for k in self.doc.keys()]))
        elif '-a' in args or '--alias' in args:
            print('\n'.join([
                k + '\t' + v for k, v in self.doc[self.cur]['alias'].items()
            ]))
        else:
            print('\t'.join(sorted(self.doc[self.cur]['content'].keys())))

    def help_ls(self):
        print(self.help['ls'])

    def do_mkdir(self, line):
        args = shlex.split(line)
        if len(args) > 0:
            name = args[0]
        else:
            name = input('name> ')
        if len(args) > 1:
            abbr = args[1]
        else:
            abbr = input('abbreviation> ')
        self.doc[abbr] = dict(title=name,
                              content={},
                              alias={
                                  ';': 'exit',
                                  '+': 'touch'
                              })
        self.modified = True

    def help_mkdir(self):
        print(self.help['mkdir'])

    def do_touch(self, line):
        if line == '':
            line = input('name> ')
        self.doc[self.cur]['content'][line] = input('input> ')
        self.modified = True

    def help_touch(self):
        print(self.help['touch'])

    def do_name(self, line):
        if line == '':
            line = input('language name> ')
        self.doc['pro']['content']['name'] = line
        self.prompt = self.doc['pro']['content']['name'] + \
            '/' + self.doc[self.cur]['title'] + '$ '
        self.modified = True

    def help_name(self):
        print(self.help['name'])

    def do_stat(self, line):
        print('Language name: %s' % self.doc['pro']['content']['name'])
        print('Vocabulary quantity: %d' % len(self.doc['lex']['content']))
        print('Parts of speech: %d' % len(self.doc['pos']['content']))

    def help_stat(self):
        print(self.help['stat'])

    def etym(self, w: Word) -> dict:
        data = dict(name='{} "{}"'.format(w['con'], w['nat']), children=[])
        for i in w['ep'].keys():
            data['children'].append(
                dict(name='{} "{}" ({})'.format(i, w['ep'][i]['nat'], w['ep'][i]['lan'])))
        for i in w['ip']:
            data['children'].append(self.etym(self.doc['lex']['content'][i]))
        if data['children'] == []:
            del data['children']
        return data

    def do_etym(self, line):
        if line == '':
            line = input('word> ')
        # print(self.etym(self.doc['lex']['content'][line]))
        print(self.doc['lex']['content'][line].etym())
        t = (
            Tree()
            .add("", [self.etym(self.doc['lex']['content'][line])], orient="RL")
            .set_global_opts(title_opts=opts.TitleOpts(title='Etymology of {}'.format(line)))
            .render('{}.html'.format(line))
        )
        print('Successfully generated "{}.html".'.format(line))

    def help_etym(self):
        print(self.help['etym'])

    def do_import(self, line):
        if self.modified:
            chc = input('Save? [y/n] ')
            if chc == 'y':
                self.do_save('')
        if line == '':
            line = input('file> ')
        if '.' not in line:
            line += '.xls'
        label = int(input('First row is labels? [1/0] '))
        colcon = int(input('column of word> '))
        colnat = input('column of meaning(s)> ')
        colpos = input('column of part of speech> ')
        colipa = input('column of spelling> ')
        coldef = input('column of definition> ')
        index = input('sheet index (default 0)> ')
        if index == '':
            index = 0
        workbook = xlrd.open_workbook(line)
        data = workbook.sheet_by_index(index)
        self.doc['pro']['content']['name'] = workbook.sheet_names()[index]
        for r in range(label, data.nrows):
            d = {}
            con = data.cell_value(r, colcon)
            d['con'] = con
            if colnat != '':
                d['nat'] = data.cell_value(r, int(colnat))
            if colpos != '':
                d['pos'] = data.cell_value(r, int(colpos))
            if colipa != '':
                d['ipa'] = data.cell_value(r, int(colipa))
            if coldef != '':
                d['info'] = data.cell_value(r, int(coldef))
            self.doc['lex']['content'][con] = Word(**d)
        self.modified = False
        self.prompt = self.doc['pro']['content']['name'] + \
            '/' + self.doc[self.cur]['title'] + '$ '
        del d

    def help_import(self):
        print(self.help['import'])

    def do_export(self, line):
        if line == '':
            line = input('file> ')
        if '.' not in line:
            line += '.xls'
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(self.doc['pro']['content']['name'])
        worksheet.write(0, 0, label='Word')
        worksheet.write(0, 1, label='Meanings')
        worksheet.write(0, 2, label='Part of Speech')
        worksheet.write(0, 3, label='Spelling')
        worksheet.write(0, 4, label='Definition')
        i = 1
        for w in sorted(self.doc['lex']['content'].keys()):
            worksheet.write(i, 0, self.doc['lex']['content'][w]['con'])
            worksheet.write(i, 1, self.doc['lex']['content'][w]['nat'])
            worksheet.write(i, 2, self.doc['lex']['content'][w]['pos'])
            worksheet.write(i, 3, self.doc['lex']['content'][w]['ipa'])
            worksheet.write(i, 4, self.doc['lex']['content'][w]['info'])
            i += 1
        workbook.save(line)

    def help_export(self):
        print(self.help['export'])

    def do_tran(self, line):
        if line == '':
            line = input('sentence> ')
        args = shlex.split(line)
        print('\t'.join([self.doc['lex']['content'][i]['nat']
                         if i in self.doc['lex']['content'].keys() else '?' for i in args]))

    def help_tran(self):
        print(self.help['tran'])

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
    os.chdir('lunaph')
    main()
