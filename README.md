# Lunaph
A small language recorder.

## How to use

After executing the .py file, you will see the prompt "> ", where you can input the operations below.

### pos | “add -p"

By inputting "pos" or "add -p", you can set some parts of speech. You may input a full name (e.g. "noun") after the prompt "pos> " and input a abbreviation (e.g. "n") after the prompt "abbr> ". There is also a complex mode to add new parts of speech. Input "pos -a" or "add -p -a" or "add -a -p" at the beginning and you can set the type pattern ("pat> ") and more information ("info> ") after inputting the part of speech and its abbreviation. If you want to skip one of the processes, just press enter at the corresponding prompt.

The type pattern of a part of speech is a regular expression that the words must match. For instance, the word "viro" matches the regular expression "o$" or ".*o$" et cetera.

### add

This is the simple mode to add new words. You may input the word (e.g. "lunaph") after the prompt "con> " and input the meaning(s) after the prompt "nat> ". There is also a complex mode to add new words. Input "add -a" at the beginning and you can set the part of speech ("pos> "), spelling ("ipa> ") and detailed definition ("def> ") after inputting the word and its meaning. If you want to skip one of the processes, just press enter at the corresponding prompt.

If your word doesn't match the enforced pattern of your part of speech, you can override the lexical rules by inputting "y".

### adj

This is the simple mode to adjust the existing words. After inputting the word you want to adjust, you can set the new word and new meanings. There is also a complex mode to adjust words. Input "adj -a" at the beginning and you can set the new part of speech, spelling and definition after setting the word and its meaning. If you want to skip one of the processes, please press enter after the corresponding prompt. Note that inputting "\\" will delete the corresponding record.

#### adj -p

This is the simple mode to adjust the existing parts of speech. After inputting the abbreviation of the part of speech you want to adjust, you can set the new name and the new abbreviation. There is also a complex mode to adjust words. Input "adj -p -a" or "adj -a -p" at the beginning and you can set the new type pattern and extra information after setting the name and its abbreviation. If you want to skip one of the processes, please press enter after the corresponding prompt. Note that inputting "\\" will delete the corresponding record.

### echo

By inputting an existing word, you can see the full information of the word.

#### echo -p

By inputting an existing part of speech, you can see the full information of it.

### del

You can delete an existing word by inputting the word.

#### del -p

You can delete an existing part of speech by inputting the abbreviation.

### save & load

You can save or load your records by inputting an absolute/relative path (with a file name) after the prompt "file> ", if you don't include an extension, it will be the default ".ln".

### exit | ;

You can input "exit" or simply a semicolon ";" to exit the program.

## Update log

- 2021-1-16 0.0.2 Alpha

  1. Added "type pattern" and "information" to "part of speech", as well as other features.
  2. Optimized code style.
  
- 2021-1-15 0.0.1 Alpha

  I should admit that the code is simple but messy.

## About the name "Lunaph"

The word "lunaph" comes from Ai Rael (which is one of my constructed languages). It derives from "lw'nafh", which means "dream" in Cthuvian. The meaning of this word hasn't changed much throughout the history. I set this particular name for this project because it is one of my unrealistic dreams.