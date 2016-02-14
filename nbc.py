""" 
	Author 			: Shirish Kadam 
	Date 			: 13th Feb 2016
	Algorigthm 		: Naive Bayes Classifier (Supervised Machine Learning)
	Implementation 	: A basic Spam filtering
	Training Data 	: learn_data.txt
"""

###################################
from math import log10
##################################

no_of_records = 6
no_of_attributes = 6											# Excluding the outcome
record_data = [[0 for x in range(7)] for x in range(6)]			#	Initialize the 2D matrix 6 by 7
i = 0

#	Create a 2D Matrix of the training data

fp = open("learn_data.txt","r")
for record in fp:
	if record.startswith("//")==False:			#	Skip the column head
		record = record.split()
###		print record
		
		for j in xrange(len(record)):
			###print i,j,record[j]
			record_data[i][j]=record[j]
		i += 1


###print record_data

#	The prior probability of each class

""" The total number of records of each class to the number of records in the dataset """

records_each_class = [0 for x in range(2)]
prob_of_each_class = [0 for x in range(2)]

for i in range(6):
	if record_data[i][6]=="T":
		records_each_class[0] += 1
	elif record_data[i][6]=="E":
		records_each_class[1] += 1

print records_each_class

""" The prior probability of each class """

for i in range(2):
	prob_of_each_class[i] = float(records_each_class[i])/float(no_of_records)

print prob_of_each_class

""" The total value of attributes for each class """

attr_of_each_class = [0 for x in range(2)]
val = 0

for i in range(6):
	for j in range(7):

		if j!=6:											#	To avoid the outcome/class from getting added
			val += int(record_data[i][j])

		if record_data[i][6]=="T":
			attr_of_each_class[0] += val
		elif record_data[i][6]=="E":
			attr_of_each_class[1] += val

		val = 0

print attr_of_each_class

""" Total number of times an attribute appears in a particular class """

single_attr_within_a_class = [[0 for x in range(6)] for x in range(2)] 						# A 2D Matrix of 2 by 7

for i in range(6):
	for j in range(7):
	
		if record_data[i][6]=="T" and j<6:
			single_attr_within_a_class[0][j] += int(record_data[i][j])
		elif record_data[i][6]=="E" and j<6:
			single_attr_within_a_class[1][j] += int(record_data[i][j])

print single_attr_within_a_class

""" The probability of an attribute appearing in a class """

prob_of_attr_within_class = [[0 for x in range(6)] for x in range(2)]

for i in range(2):
	for j in range(6):
		prob_of_attr_within_class[i][j] = float(single_attr_within_a_class[i][j] + 1)/float(attr_of_each_class[i] + no_of_attributes)
print prob_of_attr_within_class

""" A single zero in the data can wipe out the entire information in the data. This is 'Zero Frequency' problem.
	To avoid this apply Laplace Estimation. Hence, (Assumption!) a uniform distribution over all attributes. """

########################################################################################################################

prob_of_class = [0 for x in range(2)]

"""for i in range(2):
	for j in range(6):
		prob_of_class[i] = prob_of_each_class[i] * prob_of_attr_within_class[i][j]"""



""" Underflow prevention """

###input_data = [2,1,2,0,0,1]
print "Enter the record to predict"
input_data = []

for i in range(6):
	input_data.append(float(raw_input()))										# input data set

for i in range(2):
	###print "\n"
	for j in range(6):
		prob_of_class[i] += (input_data[j] * log10(prob_of_attr_within_class[i][j]))				# Here log 10 to the base is used....
		###print input_data[j]," * log(",prob_of_attr_within_class[i][j],")"

	prob_of_class[i] = log10(prob_of_each_class[i]) + prob_of_class[i]
	###print "log(",prob_of_each_class[i],") + " ,prob_of_attr_within_class[i][j]

print "Ans: ",prob_of_class
print "Max: ",max(prob_of_class)

if(prob_of_class[0]>prob_of_class[1]):
	print "Prediction: T"
else:
	print "Prediction: E"