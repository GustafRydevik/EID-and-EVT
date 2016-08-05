import sample_single_disease_parser
import re
import sys

# sample_all_disease_parser.py
# INPUT : Following the 'sample_all_disease_parser.py', input the names of the following three
# 		following three files, separated by spaces and in the following order:
# 			1. Name of the outbreak records file (must be a .txt file)
# 			2. Desired name of the output file (must be a .txt file)
# 			3. Name of the country names list (must be a .txt file)
# OUTPUT : Writes the parsed data to a tab delimited file, the name of which is specified in the
# 			arguments.


if len(sys.argv) != 4:
	print ('Please input the the names of the following files, in the following order:\n'+
			'\t1. Name of the outbreak records file\n' +
			'\t2. Desired name of the output file\n' +
			'\t3. Name of the country names list\n')

else:
	outbreaks_file_name = sys.argv[1]
	output_file_name = sys.argv[2]
	country_list_file_name = sys.argv[3]
	
	outbreaksFile = open(outbreaks_file_name, 'r')
	outbreaksText = outbreaksFile.read()

	diseaseList = [] # A list of k-v pairs, in which a unique disease name paired with all of its outbreak text

	outbreaksText += '\n\nNULLDISEASE-----\n\n'
	diseaseName = ''
	nextDisease = re.search('([A-Z/ /\-/\&/\,/\./0-9/\(/\)/\']+)-----\n\n', outbreaksText).group(1)
	textBeginning = 0
	textEnding = 0
	isolatedDiseaseText = ''

	while True:
		textBeginning = textEnding
		diseaseName = nextDisease
		if diseaseName == 'NULLDISEASE':
			break
		nextDisease = re.search('([A-Z/ /\-/\&/\,/\./0-9/\(/\)/\']+)-----\n\n',outbreaksText[textBeginning + 70:]).group(1) #finds the next disease name in the text file
		textEnding = outbreaksText.find('\n' + nextDisease + '-----')
		textBeginning = outbreaksText[textBeginning:].find('-----\n\n') + (textBeginning + 7)
		isolatedDiseaseText = outbreaksText[textBeginning : textEnding]
		diseaseList.append((diseaseName,isolatedDiseaseText))

	outputFile = open(output_file_name,'w')
	# Printing
	outputFile.write('Disease\tCountry\tYear\tCountry Flag\tAnimal Flag\tPublication Year Flag\tRecord Text\tTotal Cases\n')

	for i in diseaseList:
		outputFile.write(sample_single_disease_parser.singleDiseaseParser(i[0],i[1],country_list_file_name))

	outputFile.close()
	outbreaksFile.close()
