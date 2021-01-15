# Lunaph
A small language recorder.

## How to use

After executing the .py file, you will see the prompt "> ", where you can input the operations below.

### pos

By inputting "pos", you can set some parts of speech. You may input a full name (e.g. "noun") after the prompt "pos> " and input a abbreviation (e.g. "n") after the prompt "abbr> ".

### add

This is the simple mode to add new words. You may input the word (e.g. "lunaph") after the prompt "con> " and input the meaning(s) after the prompt "nat> ". There is also a complex mode to add new words. Input "add -a" at the beginning and you can set the part of speech ("pos> "), spelling ("ipa> ") and detailed definition ("def> ") after inputting the word and its meaning. If you want to skip one of the processes, just press enter at the corresponding prompt.

### adj

This is the simple mode to adjust the existing words. After inputting the word you want to adjust, you can set the new word and new meanings. There is also a complex mode to adjust words. Input "adj -a" at the beginning and you can set the new part of speech, spelling and definition after setting the word and its meaning. If you want to skip one of the processes, please input "\\" after the corresponding prompt. Note that pressing enter will delete the corresponding record.

### echo

By inputting an existing word, you can see the full information of the word.

### del

You can delete an existing word by inputting the word.

### save & load

You can save or load your records by inputting an absolute/relative path (with a file name) after the prompt "file> ", if you don't include an extension, it will be the default ".ln".

### exit & ;

You can input "exit" or simply a semicolon ";" to exit the program.

## Update log

- 2021-1-15 0.0.1 Alpha

  I should admit that the code is simple but messy.

## About the name "Lunaph"

The word "lunaph" comes from Ai Rael (which is one of my constructed languages). It derives from "lw'nafh", which means "dream" in Cthuvian. The meaning of this word hasn't changed much throughout the history. I set this particular name for this project because it is one of my unrealistic dreams.