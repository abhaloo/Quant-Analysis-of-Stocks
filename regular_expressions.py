#The following is a file for reference on regular expressions,;
#referenced from pythonprogramming.net
#
#
#Regular expressions are used to traverse through text based data to find things.
#Their purpose is to express a pattern of data that is to be located
#
#In Python 3, the module to use regular expressions is re.
#
#
#Regular expressions are useful for sifting through an arbitrary body of text in search of something specific.
#Imagine a programmer is looking for prices in a body of text. You're basically looking for a dollar sign($), followed 
#at least 1 number, maybe a decimal point and then maybe more numbers.
#In order to incoroporate all the possibilities in a search we must use regualr expressions. 
#
#
#-------------------------------------------------------------
#Identifiers:
#
#\d = any number
#\D = anything but a number
#\s = space
#\S = anything but a space
#\w = any letter
#\W = anything but a letter
#. = any character, except for a new line
#\b = space around whole words
#\. = period. must use backslash, because . normally means any #character.
#
#----------------------------------------------------------------
#Modifiers:
#
#{1,3} = for digits, u expect 1-3 counts of digits, or "places"
#+ = match 1 or more
#? = match 0 or 1 repetitions.
#* = match 0 or MORE repetitions
#$ = matches at the end of string
#^ = matches start of a string
#| = matches either/or. Example x|y = will match either x or y
#[] = range, or "variance"
#{x} = expect to see this amount of the preceding code.
#{x,y} = expect to see this x-y amounts of the precedng code
#
#--------------------------------------------------------------------
#
#White Space Charts:
#
#\n = new line
#\s = space
#\t = tab
#\e = escape
#\f = form feed
#\r = carriage return
#Characters to REMEMBER TO ESCAPE IF USED!
#
#----------------------------------------------------------------------
#
#. + * ? [ ] $ ^ ( ) { } | \
#Brackets:

#[] = quant[ia]tative = will find either quantitative, or quantatative.
#[a-z] = return any lowercase letter a-z
#[1-5a-qA-Z] = return all numbers 1-5, lowercase letters a-q and uppercase A-Z
#----------------------------------------------------------------------

#example code
import re 

exampleString = '''
James is 15 years old, and Daniel is 27 years old. 
Edgar is 65, and his grandfather is 103. Meanwhile, Jess is only 4'''


#start regular expressions with r'
#we want to search for digits of lengths 1-3
ages = re.findall(r'\d{1,3}',exampleString)

#search for any captial letter, followed by any number of lower case letters
names = re.findall(r'[A-Z][a-z]*',exampleString)


print(ages)
print(names)