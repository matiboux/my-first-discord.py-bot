def parsecommand(query):
	argv = []
	args = ""
	while(query):
		l = len(query)
		
		# Find an unescaped ' '
		i = query.find(' ')
		if i > 0:
			while query[i - 1] == '\\':
				i = query.find(' ', i + 1)
		
		if i < 0: break  # No more next arguments
		
		# If argument starts with a '"'
		if query[0] == '"':
			query = query[1:]
			
			# Find the next unescaped "
			j = query.find('"', 1)
			if j > 0:
				while query[j - 1] == '\\':
					j = query.find('"', j + 1)
			
			# If a space happened before
			if j >= 0 and i < j:
				# Find the next unescaped ' '
				i = query.find(' ', j + 1)
				if i > 0:
					while query[i - 1] == '\\':
						i = query.find(' ', i + 1)
			
			argv.append(query[:j])
		else:
			argv.append(query[:i])
		
		query = query[i + 1:]
		if not args: args = query
	
	argv.append(query)
	return len(argv), argv, args
