# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:34:22 2020

@author: Louis Beal
"""

import string
import numpy as np
import pandas as pd

    
def cleanString(inpStr):
    
    """takes input string, converts to all lowercase and outputs
    sequential list of words"""
    
    #convert to lowercase
    inpStr = inpStr.lower()
    
    #replace special characters with space
    replace = ["/","-"]
    
    #list of accepted characters
    #ascii lower case, plus additional
    accept = list(string.ascii_lowercase) + [str(n) for n in range(10)] + [" "]
    
    
    cleanList = []
    for letter in list(inpStr):
        
        if letter in accept:
            cleanList.append(letter)
            
        elif letter in replace:
            cleanList.append(" ")
            
    #join letters
    clean = "".join(cleanList)
    
    #split by word and remove spaces    
    wordList = clean.split(" ")
    wordList = [w for w in wordList if w != ""]
    
    return(wordList)


def countPhrase(inpLst,filtLen=1,ignore = None):
    """apply matching filter along input list, counting repeats"""
    
    if ignore is not None:
        inpLst = [w for w in inpLst if w not in ignore]
        
    if filtLen > 1:
        #apply filter
        
        filtered = []
        for i in range(len(inpLst) - filtLen + 1):
            filtered.append(" ".join(inpLst[i:i+filtLen]))
        
    else:
        filtered = inpLst
        
    #print(filtered)
    
    unique, counts = np.unique(filtered, return_counts=True)
    
    return(unique, counts)


if __name__ == "__main__":

    #load document to test
    with open("sample.txt","r") as o:
        data = o.readlines()
    
    #load exceptions (prevents spam of commonly used words)
    with open("ignore.txt") as i:
        ignore = i.readlines()        
        ignore = [x.strip() for x in ignore]
        #also ignore single letters
        ignore += list(string.ascii_lowercase)
    # print("ignoring words: ")
    # print(ignore)
    # print()
    
    #join as continuous string and run a cleanup
    cont = "".join(data)
    
    clean = cleanString(cont)
    
    
    nonuniq = -1 #counter for non-unique words
    n = 0    
    storage = {}

    #run for increasing phrase lengths until a set of wholly unique phrases is found    
    while nonuniq != 0:        
        
        n += 1        
        currentLen = "{} word".format(n) 
        print("analysis for " + currentLen + " strings:")
        
        #generate list of unique word patterns and their respective counts
        unique, counts = countPhrase(clean,n,ignore)
        
        #use pandas to sort phrases into a descending order of usage
        temp = pd.DataFrame({"phrase":unique,"count":counts})        
        temp = temp.sort_values("count", ascending = False)
    
        #the index of the first count of 1 (unique phrase)
        #counts the number of non-unique phrases used before it
        #within the descending list
        nonuniq = list(temp["count"]).index(1)
        print("\tfound {} non-uniques".format(nonuniq))
        
        if nonuniq != 0:
            #store these reused phrases for anaylsis
            multi = np.array(temp)[:nonuniq,:]        
            storage[currentLen] = multi
            
            
            
            
    with open("result.txt","w+") as o:
        
        o.write("-"*49)
        o.write("\nWordStats breakdown of word usage in scanned file\n")
        o.write("-"*49 + "\n")
                
        
        #format for a more readable vertical setup
        widths = []
        
        vsplit = "\n++"
        header = "\n||"
        
        #set up columns
        nRows = len(storage[list(storage.keys())[0]])
        rows = ["\n|| "]*nRows
        
        for key in storage.keys():
            data = storage[key]
            words = data[:,0]
            
            maxwidth = max([len(x) for x in words])
            
            header += key.ljust(maxwidth) + "        ||"
            vsplit += "-"*maxwidth + "--------++"
            
            for i in range(len(rows)):
                
                
                if i < len(data):
                    
                    word = data[i,0].ljust(maxwidth)
                    count = str(data[i,1]).ljust(3)
                    
                    text = word + " | " + count + " || "
                
                else:
                    
                    text = " "*maxwidth + " |     || "
                    
                rows[i] += text
                    
                    
        o.write(vsplit)
        o.write(header)
        o.write(vsplit)        
        for row in rows:
            o.write(row)            
        o.write(vsplit)
        