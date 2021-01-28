# wordStats
Python script to take a block of text and return counts of phrases used

scans increasing phrase lengths until all unique phrases are found. A scan length of 1 will count repeated words in a document, for example.

ignore.txt is pre-populated and contains a list of words to exclude from this scan, and should contain any overly common connective words such as "and", "but", "be", etc.
