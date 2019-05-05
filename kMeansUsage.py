import csv


def getAllGroupsData(filename):
    print 'Starting to read all data'
    with open(filename, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter='|')
        a = creader.next()  # get rid of the first row (instructions...)
        data = []
        rowCount = 1
        for row in creader:
            currData = []
            for i in range(len(row)):
                if i == 0:
                    continue
                currData.append(row[i])
            data.append(currData)
            if rowCount % 100000 == 0:
                print 'current row = ' + str(rowCount)
            rowCount = rowCount + 1

        print 'Finished reading all data'
        return data


def writeKMeansAnalyzeToCSV(y_kmeans, filename):
    print 'writing k means analyze data to csv'
    with open(filename, 'wb') as kmeansFile:
        cswriter = csv.writer(kmeansFile, delimiter='|')
        cswriter.writerow(['kmeansGroup', ' '])
        for i in y_kmeans:
            cswriter.writerow([i, ' '])


def kMeansAnalyze(k, inputFilename, outputFilename):
    print 'importing k-means analyze tools'
    from sklearn.cluster import KMeans
    print 'Starting to analyze ' + str(k) + ' means of the data calculated'

    X = getAllGroupsData(inputFilename)
    print 'Starting to cluster'
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    writeKMeansAnalyzeToCSV(y_kmeans, outputFilename)


print 'Starting k-means analyze'

inputFilename = "D:\\data for kobi\\eLearning\\new episode level\\third cluster\\studentsVector.csv"
ks = [2, 3, 4, 5]
for k in ks:
    outputFilename = "D:\\data for kobi\\eLearning\\new episode level\\third cluster\\kMeansOutput " + str(k) + " means.csv"

    kMeansAnalyze(k, inputFilename, outputFilename)

print 'Done k-means analyze'
