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

    with open("test.txt","r") as o:
        data = o.readlines()
    
    #join as continuous string
    cont = "".join(data)
    
    clean = cleanString(cont)
    statistics = pd.DataFrame()
    
    ignore = ["and","the","be","by","to","of","on","an","in","at","it","as","is","a"]
    
    print("ignoring words: ")
    print(ignore)
    print()
    
    firstunique = -1
    n = 0
    
    storage = {}
    
    while firstunique != 0:
        
        n += 1
        
        col = "{} word".format(n)        
        if n != 1:
            col = col + "s"
        
        print("analysis for " + col + ":")
        
        unique, counts = countPhrase(clean,n,ignore)
        
        temp = pd.DataFrame({"phrase":unique,"count":counts}).sort_values("count", ascending = False)
    
        firstunique = list(temp["count"]).index(1)
        print("there are {} non-uniques".format(firstunique))
        
        multi = np.array(temp)[:firstunique,:]
        
        storage[str(n)] = multi