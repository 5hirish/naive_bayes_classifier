""" 
Author          : Shirish Kadam
Date            : 13th Feb 2016
Algorithm       : Naive Bayes Classifier (Supervised Machine Learning)
Implementation  : A basic Spam filtering
Training Data   : learn_data.txt and training_data.cvs
"""

###################################
from math import log10


##################################

def num_of_records(fp):
    num_records = 0
    for record in fp:
        if not record.startswith("//"):  # Skip the column head
            num_records += 1
    return num_records


def num_of_attributes(fp):
    num_attr = 0
    for record in fp:
        if record.startswith("//"):
            record = record.split()
            for j in xrange(len(record)):
                num_attr += 1
    return num_attr


def num_of_class(num_attr, record_data):
    outcome = []
    unique_outcome = []
    for i in range(num_attr):
        outcome.append(record_data[i][num_attr])
    
    [unique_outcome.append(item) for item in outcome if item not in unique_outcome]

    num_class = len(unique_outcome)
    return (num_class, unique_outcome)
    

fp = open("training_data.cvs", "r")

num_records = num_of_records(fp)
fp.seek(0)                                  # File pointer to the beginning
num_attr_outcome = num_of_attributes(fp)    # Including the outcome
num_attr = num_attr_outcome - 1             # Excluding the outcome
#fp.seek(0) 
#num_class = num_of_class(fp, num_records)

print "Training Dataset Info:\n"
print "Total Attributes:", num_attr, "Total Records:", num_records

record_data = [[0 for x in range(num_attr_outcome)] for x in range(num_records)]  # Initialize the 2D matrix 6 by 7
i = 0

attributes = []
# Create a 2D Matrix of the training data
fp.seek(0)
for record in fp:
    if not record.startswith("//"):  # Skip the column head
        record = record.split()
        # ### print record

        for j in xrange(len(record)):
            # print i,j,record[j]
            record_data[i][j] = record[j]
        i += 1
    else:
        record = record.split()
        for j in xrange(len(record)):
            attributes.append(record[j])


fp.close()

outcome = []
num_class, outcome_data = num_of_class(num_attr, record_data)
print "Total Classes:", num_class
print outcome_data

# ### print record_data

# The prior probability of each class

""" The total number of records of each class to the number of records in the dataset """

records_each_class = [0 for x in range(num_class)]
prob_of_each_class = [0 for x in range(num_class)]

for i in range(num_attr):
    if record_data[i][num_attr] == "T":
        records_each_class[0] += 1
    elif record_data[i][num_attr] == "E":
        records_each_class[1] += 1

print records_each_class

""" The prior probability of each class """

for i in range(num_class):
    prob_of_each_class[i] = float(records_each_class[i]) / float(num_attr)

print prob_of_each_class

""" The total value of attributes for each class """

attr_of_each_class = [0 for x in range(num_class)]
val = 0

for i in range(num_records):
    for j in range(num_attr_outcome):

        if j != num_attr:  # To avoid the outcome/class from getting added
            val += int(record_data[i][j])

        if record_data[i][num_attr] == "T":
            attr_of_each_class[0] += val
        elif record_data[i][num_attr] == "E":
            attr_of_each_class[1] += val

        val = 0

print attr_of_each_class

""" Total number of times an attribute appears in a particular class """

single_attr_within_a_class = [[0 for x in range(num_attr)] for x in range(num_class)]  # A 2D Matrix of 2 by 7

for i in range(num_records):
    for j in range(num_attr_outcome):

        if record_data[i][num_attr] == "T" and j < num_attr:
            single_attr_within_a_class[0][j] += int(record_data[i][j])
        elif record_data[i][num_attr] == "E" and j < num_attr:
            single_attr_within_a_class[1][j] += int(record_data[i][j])

print single_attr_within_a_class

""" The probability of an attribute appearing in a class """

prob_of_attr_within_class = [[0 for x in range(num_attr)] for x in range(num_class)]

for i in range(num_class):
    for j in range(num_attr):
        prob_of_attr_within_class[i][j] = float(single_attr_within_a_class[i][j] + 1) / float(
            attr_of_each_class[i] + num_attr)
print prob_of_attr_within_class

""" A single zero in the data can wipe out the entire information in the data. This is 'Zero Frequency' problem.
To avoid this apply Laplace Estimation. Hence, (Assumption!) a uniform distribution over all attributes. """

########################################################################################################################

prob_of_class = [0 for x in range(num_class)]

""" Underflow prevention """

# ### input_data = [2,1,2,0,0,1] for testing
print "Enter the record to predict"
input_data = []

for i in range(num_attr):
    input = raw_input(attributes[i]+": ")
    input_data.append(float(input))

solution = {}

for i in range(num_class):
    # print "\n"
    for j in range(num_attr):
        prob_of_class[i] += (input_data[j] * log10(prob_of_attr_within_class[i][j]))  # Here log 10 to the base is used
    # ### print input_data[j]," * log(",prob_of_attr_within_class[i][j],")"

    prob_of_class[i] += log10(prob_of_each_class[i])
    solution[prob_of_class[i]] = outcome_data[i]
# ### print "log(",prob_of_each_class[i],") + " ,prob_of_attr_within_class[i][j]

print "Ans: ", prob_of_class

solution_probability = max(prob_of_class)

print "Max: ", solution_probability

print "Prediction : ", solution[solution_probability]
