import csv
import re


class Episode:
    def __init__(self, episode_slug, correct_answers_percentage):
        self.episode_slug = episode_slug
        self.correct_answers_percentage = correct_answers_percentage


class Student:
    def __init__(self, accountID):
        self.accountID = accountID
        self.episodes = {}  # The episodes that this student has *finished*
        self.topics = {}

    def addEpisode(self, episode):
        if episode.episode_slug not in self.episodes:
            self.episodes[episode.episode_slug] = episode

    def calculateTopics(self):
        self.topics = {}  # initialize empty

        for episode_slug in self.episodes:
            if episode_slug not in epMap:
                continue
            current_topics = epMap[episode_slug]
            for topic in current_topics:
                if topic is None:
                    continue
                episode = self.episodes[episode_slug]
                if topic in self.topics:
                    self.topics[topic][0] = self.topics[topic][0] + episode.correct_answers_percentage
                    self.topics[topic][1] = self.topics[1] + float(1)
                else:
                    self.topics[topic] = [episode.correct_answers_percentage, float(1)]  # percentage_on_topic, num_of_episodes_on_topic

        for topic in self.topics:
            self.topics[topic][0] = self.topics[topic][0] / self.topics[topic][1]  # avg of topic score

        # complete missing topics:
        for topic in topicsList:
            if topic not in self.topics:
                self.topics[topic] = [0, 0]  # didn't practice this topic

    def getTopicScore(self, topic):
        return self.topics[topic][0]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.accountID == other.accountID
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def clearText(str):
    return str.replace('\'', '')


def myReader(fileName):
    with open(fileName, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter='|')

        for row in creader:
            is_finished = int(row[19])
            if is_finished == 0:  # if not finished ignore this attempt
                continue

            account_id = row[0]

            episode_slug = re.sub(r'_.*', '', row[9])

            correct_answers_percentage = float(row[21])
            episode = Episode(episode_slug, correct_answers_percentage)

            if account_id in students:
                students[account_id].addEpisode(episode)
            else:
                currentStudent = Student(account_id)
                currentStudent.addEpisode(episode)
                students[account_id] = currentStudent



def getRelevantTopic(row):
    if row[4]:
        return row[4]
    if row[3]:
        return row[3]
    if row[2]:
        return row[2]
    if row[1]:
        return row[1]
    return None


def buildEpisodeMap(spineFilename):
    with open(spineFilename, 'rb') as spine:
        creader = csv.reader(spine, delimiter='|')
        a = next(creader)  # get rid of first header line

        for row in creader:
            episode_slug = row[0]
            topic = getRelevantTopic(row)
            if topic is not None:
                if episode_slug in epMap:
                    if topic not in epMap[episode_slug]:
                        epMap[episode_slug].append(topic)
                else:
                    epMap[episode_slug] = [topic]
                if topic not in topicsList:
                    topicsList.append(topic)


students = {}
epMap = {}
topicsList = []

print 'Starting program'
print 'Starting to go over all of the data files'
# go over all of the data files:
for num in range(6):
    myReader("D:\\data for kobi\\eLearning\\new episode level\\episode_run_000" + str(num) + "_part_00")

print 'Finished to go over all of the data files'
print 'Starting to calculate episode map (maps from episode to topic)'
# calculate episode map (maps from episode to topic):
buildEpisodeMap("D:\\data for kobi\\eLearning\\new episode level\\NewSpine.csv")

print 'Finished to calculate episode map (maps from episode to topic)'
print 'Starting to calculate topics for every student and write him in a file)'
# calculate topics for every student and write him in a file:
studentsFilename = "D:\\data for kobi\\eLearning\\new episode level\\studentsVector.csv"
with open(studentsFilename, 'wb') as studentsFile:
    cwriter = csv.writer(studentsFile, delimiter='|')

    names = ['account_id']
    for topic in topicsList:
        names.append(topic)

    cwriter.writerow(names)

    for account_id in students:
        students[account_id].calculateTopics()

        score = [account_id]
        for topic in topicsList:
            score.append(students[account_id].getTopicScore(topic))

        cwriter.writerow(score)

print 'Finished to calculate topics for every student and write him in a file)'
print 'Finished program'
