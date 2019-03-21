'''
    This file is for clearing the un needed stuff from the file "spine.csv" and make it easier to work with
    I will make a file that contains a mapping of episode -> topic hierarchy
'''

'''
    Current important stuff are indexed as followed:
    Hierarchy:
    Level 1 - index 2
    Level 2 - index 3
    Level 3 - index 4
    Level 4 - index 5
    Level 5 - index 6
    
    Episodes:
    indices 9 - 28
'''

class Hierarchy:
    def __init__(self, level1, level2, level3, level4, level5):
        self.level1 = level1
        self.level2 = level2
        self.level3 = level3
        self.level4 = level4
        self.level5 = level5

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.level1 == other.level1 and self.level2 == other.level2 and self.level3 == other.level3 and self.level4 == other.level4 and self.level5 == other.level5
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def BuildHierarchy(row):
    h = Hierarchy(row[2], row[3], row[4], row[5], row[6])
    return h


def checkComma(str):
    return '|' in str


import csv

filename = "D:\\data for kobi\\eLearning\\new episode level\\Spine.csv"
outFilename = "D:\\data for kobi\\eLearning\\new episode level\\NewSpine.csv"
duplicateEpisodesFilename = "D:\\data for kobi\\eLearning\\new episode level\\DuplicateEpisodes.csv"

epMap = {}  # define an empty dictionary to map from episode to hierarchy
duplicates = {}

with open(filename, 'rb') as csvfile:
    creader = csv.reader(csvfile, delimiter=',')
    lineNum = 1
    a = next(creader)  # get rid of first header line

    for row in creader:
        h = BuildHierarchy(row)

        for i in range(9, 29, 1):
            if row[i]:
                if row[i] in duplicates:
                    # append another duplicate:
                    duplicates[row[i]].append(h)
                    continue
                if row[i] in epMap:
                    # a newly found duplicate:
                    duplicates[row[i]] = [epMap[row[i]], h]
                    # if epMap[row[i]] != h:
                    #     print 'duplicate episode: "' + row[i] + '", was found in line: ' + str(lineNum)
                else:
                    epMap[row[i]] = h

        lineNum = lineNum + 1

    with open(outFilename, 'wb') as outFile:
        cwriter = csv.writer(outFile, delimiter='|')

        cwriter.writerow(['episode', 'level1', 'level2', 'level3', 'level4', 'level5'])
        for episode in epMap:
            h = epMap[episode]
            cwriter.writerow([episode, h.level1, h.level2, h.level3, h.level4, h.level5])

    with open(duplicateEpisodesFilename, 'wb') as duplicatesFile:
        duplicatesWriter = csv.writer(duplicatesFile, delimiter='|')

        duplicatesWriter.writerow(['serial number of duplicate', 'episode', 'level1', 'level2', 'level3', 'level4', 'level5'])
        for episode in duplicates:
            num = 1
            for h in duplicates[episode]:
                duplicatesWriter.writerow([str(num), episode, h.level1, h.level2, h.level3, h.level4, h.level5])
                num = num + 1
