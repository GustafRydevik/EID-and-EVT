import re

# singleDiseaseParser : string, string --> string
# INPUT : The name of a disease (diseaseName), the record texts listed for the disease (text_raw),
#		  and the name of the file which stores the names of all nations and territories in GIDEON
#		  (country_file_name).
# OUTPUT : The data parsed from each outbreak record, organized into a tab-delimited string format.

def singleDiseaseParser(diseaseName,text_raw, country_file_name):
	print '\n\nNOW PARSING ' + diseaseName + ' OUTBREAKS'
	
	country_file = open(country_file_name, 'r')
	country_file_text = country_file.read()
	country_list_total = country_file_text.upper().split('\n')
	if country_list_total[-1] == '':
		country_list_total.pop(-1)
	country_file.close()
	
	text_raw = '\n\n' + text_raw
	country_list = [] # country_list is a list of all nations which reported outbreaks for the disease
	for i in country_list_total:
		if text_raw.find('\n'+i+'\n') != -1:
			country_list.append(i)

	text_country = text_raw + '\n\nEND'
	output = ''
	output_dictionary = {} # A dictionary of key-value pairs, in which the keys are country names and the values are a list of all records reported by the country
	
	for i in country_list:
		output_dictionary[i] = []
		
	date_position = 0
	text_date = text_raw + '\n\n     9999' # The regular expression functions produce errors if no matches are found, and try loops did not work for many of the parts of the script, so text is often appended to the searched string which would fit the regular expression, but end the while loop.
	searchtxtdate = '(\ \ \ \ \ )(\d\d\d\d)' # The regular expression used to catch the year on outbreaks, in accordance to the pattern specified above
	
#	print country_list
		
	for country in country_list: # Each specific outbreak is confined to a single line and begins with five spaces followed by the year of outbreak. Note that this script only pulls the first year listed--in outbreaks spanning several years, the end year is ignored.
		date_position = text_date.find('\n' + country + '\n') # Initializing the pointer to the beginning of the country
		date_result = re.search(searchtxtdate, text_date[date_position:]) # A regular expression used to find the date, according to the pattern specified by searchtxtdate
		while text_date.find(date_result.group(2), text_date.find('\n', date_position)) < text_date.find('\n\n', date_position): # For all records listed under each country subheading
		 	date_position = text_date.find(date_result.group(2), text_date.find('\n', date_position)) # Resetting the date pointer
	  		output_dictionary[country].append(date_result.group(2)) # Storing the year of outbreak
	  		date_result = re.search(searchtxtdate, text_date[date_position + 15:]) # Resetting the regular expression, searching for the first match AFTER the current line
#			print date_result.group(2)
# 		print output_dictionary[country]
	
	
	indiv_dictionary = {} # A dictionary of key-value pairs, in which the keys are countries and the values are lists of case data from all reported outbreaks
	
	for i in country_list:
		indiv_dictionary[i] = []
	
# 	print output_dictionary
	
	text_indiv = text_raw # Future parsing uses the text_raw, so the text_indiv is a copy which can be manipulated and modified during the case data parsing
	for i in range(0,10): # This removes all commas from numbers (91,342 --> 91342)
		for j in range(0,10):
			if text_indiv.find(str(i) + ',' + str(j)) != -1:
				text_indiv = text_indiv.replace(str(i) + ',' + str(j), str(i) + str(j))
	
	country_location = 0 # This marks the start location in the text_indiv of a country's records
	year_location = 0 # Used to mark the location of the year  of outbreak before a record text
	paren_str = '' # The text of the first parenthetical clause in a record text
	line_str = '' # The text of the outbreak record
	estimated_num = 0 # This stores the number of estimated cases, or acts as a filler if no data are found
	fatalities_num = 0 # Fatal cases
	hospitalized_num = 0 # Hospitalized cases
	confirmed_num = 0 # Confirmed cases

	for country in country_list:
		for j in range(len(output_dictionary[country])):
			indiv_dictionary[country].append('')

#	print indiv_dictionary

	for country in country_list: # This loop collects the number of confirmed, estimated, hospitalized, and fatal cases
		year_location = text_indiv.find('\n' + country + '\n') + 1
		
		for j in range(len(output_dictionary[country])):
			paren_str = ''
			line_str = ''
			indiv_output_str = ''
			fatalities_num = 9999 # The case data are initialized at 9999 and only replaced if data is found in the record text
			hospitalized_num = 9999
			confirmed_num = 9999
			estimated_num = 9999
			year_location = text_indiv.find('     ' + str(output_dictionary[country][j]), year_location + 1)
			if re.search('\([\d]+', text_indiv[year_location:text_indiv.find('\n', year_location)]):
				line_str = text_indiv[text_indiv.find(' - ', year_location):text_indiv.find('\n', year_location)]
				paren_str = line_str[line_str.find('('):line_str.find(')')]
				paren_str_full = paren_str # The loop first isolated the parenthetical phrase for a single outbreak which includes the case data.

				fatal_regex1 = re.search('(\d+) (fatal)', paren_str) # The two regular expressions used to identify fatal cases
				fatal_regex2 = re.search('(\d+) (death)', paren_str)
				if fatal_regex1: # Regular expressions have a boolean characteristic in python - true implies a match to the regular expression
					fatalities_num = fatal_regex1.group(1)
#					print country, str(output_dictionary[country][j]), fatalities_num + ' fatalities'
					paren_str = paren_str.replace(fatal_regex1.group(0), '_____') # Replacing the matched case text avoids multiple matches in later, less specific regular expressions
				elif fatal_regex2:
					fatalities_num = fatal_regex2.group(1)
#					print country, str(output_dictionary[country][j]), fatalities_num + ' fatalities'
					paren_str = paren_str.replace(fatal_regex2.group(0), '_____')

				hospitalized_regex1 = re.search('(\d+) (hospital)', paren_str) # The two regular expressions used to identify hospitalized cases
				hospitalized_regex2 = re.search('(\d+) (cases hospital)', paren_str)
				if hospitalized_regex1:
					hospitalized_num = hospitalized_regex1.group(1)
#					print country, str(output_dictionary[country][j]), hospitalized_num + ' hospitalized'
					paren_str = paren_str.replace(hospitalized_regex1.group(0), '_____')
				elif hospitalized_regex2:
					hospitalized_num = hospitalized_regex2.group(1)
#					print country, str(output_dictionary[country][j]), hospitalized_num + ' hospitalized'
					paren_str = paren_str.replace(hospitalized_regex2.group(0), '_____')

				confirmed1 = re.search('(\d+) (confirm)', paren_str) # Regular expressions for confirmed casese
				confirmed2 = re.search('(\d+) (cases confirm)', paren_str)
				confirmed3 = re.search('(\d+) (cases were confirm)', paren_str)
				confirmed4 = re.search('(\d+) (clinical)', paren_str)
				if confirmed1:
					confirmed_num = confirmed1.group(1)
#					print country, str(output_dictionary[country][j]), confirmed_num + ' confirmed'
					paren_str = paren_str.replace(confirmed1.group(0), '_____')
				elif confirmed2:
					confirmed_num = confirmed2.group(1)
#					print country, str(output_dictionary[country][j]), confirmed_num + ' confirmed'
					paren_str = paren_str.replace(confirmed2.group(0), '_____')
				elif confirmed3:
					confirmed_num = confirmed3.group(1)
#					print country, str(output_dictionary[country][j]), confirmed_num + ' confirmed'
					paren_str = paren_str.replace(confirmed3.group(0), '_____')
				elif confirmed4:
					confirmed_num = confirmed4.group(1)
#					print country, str(output_dictionary[country][j]), confirmed_num + ' confirmed'
					paren_str = paren_str.replace(confirmed3.group(0), '_____')

				estimated1 = re.search("(\d+) ('probable')", paren_str) # Regular expressions used for estimated cases
				estimated2 = re.search('(\d+) (suspect)', paren_str)
				estimated3 = re.search('(\d+) (probable)', paren_str)
				estimated4 = re.search('(\d+) (estimate)', paren_str)
				estimated5 = re.search('(\d+) (case)', paren_str)
				if estimated1:
					estimated_num = estimated1.group(1)
					paren_str = paren_str.replace(estimated1.group(0), '_____')
#					print country, str(output_dictionary[country][j]), estimated_num + ' estimated'
				elif estimated2:
					estimated_num = estimated2.group(1)
					paren_str = paren_str.replace(estimated2.group(0), '_____')
#					print country, str(output_dictionary[country][j]), estimated_num + ' estimated'
				elif estimated3:
					estimated_num = estimated3.group(1)
					paren_str = paren_str.replace(estimated3.group(0), '_____')
#					print country, str(output_dictionary[country][j]), estimated_num + ' estimated'
				elif estimated4:
					estimated_num = estimated4.group(1)
					paren_str = paren_str.replace(estimated4.group(0), '_____')
#					print country, str(output_dictionary[country][j]), estimated_num + ' estimated'
				elif estimated5:
					estimated_num = estimated5.group(1)
					paren_str = paren_str.replace(estimated5.group(0), '_____')
#					print country, str(output_dictionary[country][j]), estimated_num + ' estimated'

				indiv_output_str = str(estimated_num)

			else:
				indiv_output_str = '9999\t' # If no parenthetical clause if found in the record text, the case data is filled with 9999s
			indiv_dictionary[country][j] = indiv_output_str

	
				
			
	year_position_bool = 0 # Used to store the position of the outbreak year, marking the start of an outbreak record
	country_position_bool = 0 # The position of the current nation or territory's name, marking the start of all records
	year_text_bool = ''
	flag_bool = 0 # Boolean turned to 1 for multinational flag
	flag_animal_bool = 0 # Boolean turned to 1 for animal flag
	flag_pubyear_bool = 0 # Boolean turned to 1 for publication year flag
	for i in country_list: # These boolean functions flag entries for post-processing. Specific strings can be found in many misclassified outbreaks--the regular expressions search for these strings and, if a certain entry is flagged, the full text of the outbreak entry will be included in the output.
		country_position_bool = text_raw.find('\n'+i+'\n') - 1
		year_position_bool = country_position_bool
		for j in range(len(output_dictionary[i])):
			flag_bool = 0
			flag_animal_bool = 0
			flag_pubyear = 0
			year_text_bool = output_dictionary[i][j][:4]
			year_position_bool = text_raw.find(year_text_bool, text_raw.find('\n', year_position_bool))
			for k in range(len(country_list_total)): # Flags if a country name is found in the record text
				if (text_raw.upper()).find(country_list_total[k],  year_position_bool, text_raw.find('\n', year_position_bool)) != -1:
					flag_bool = 1
#					print 'Nation or territory found: ' + country_list_total[k]
					break
			if (text_raw.find('military', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or # The strings used for multinational flags
				 text_raw.find('tourist', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('travel', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('introduc', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('return', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('neighbor', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('arriv', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('cruise', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('visit', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('missionar', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('flight', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('import', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('export', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('Navy', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('navy', year_position_bool, text_raw.find('\n', year_position_bool)) != -1):
					flag_bool = 1
			if (text_raw.find('animal', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('mammal', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find(' dog', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('wolf ', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('wolve ', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('deer ', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('goat', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('monkey', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('macaque', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find(' lion', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find(' zoo ', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find(' pig', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('bird', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find('fish', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find('antelope', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('sheep', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find('cattle', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find('livestock', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find('poultry', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find('zebra', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find(' cow', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find('horse', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or 
				 text_raw.find(' ox', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('equine', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('ovine', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('canine', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find('murine', year_position_bool, text_raw.find('\n', year_position_bool)) != -1 or
				 text_raw.find(' farm', year_position_bool, text_raw.find('\n', year_position_bool)) != -1):
				flag_animal_bool = 1
			if text_raw.find('(publication year)', year_position_bool, text_raw.find("\n", year_position_bool)) != -1:
				flag_pubyear = 1
			output_dictionary[i][j] += '\t' + str(flag_bool) + '\t' + str(flag_animal_bool) + '\t' + str(flag_pubyear) + '\t'
			if flag_bool == 1 or flag_animal_bool == 1:
				output_dictionary[i][j] += text_raw[text_raw.find(' - ', year_position_bool)+3:text_raw.find('\n', year_position_bool)]
			
	
	
	for i in country_list:
		for j in range(len(output_dictionary[i])):
			output_dictionary[i][j] = output_dictionary[i][j] + '\t' + indiv_dictionary[i][j]
	
	outputString = ""
	for i in country_list:
		for j in range(len(output_dictionary[i])):
			outputString += diseaseName + '\t' + i + '\t' + str(output_dictionary[i][j]) + '\n'
	return outputString

