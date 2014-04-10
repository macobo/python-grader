def laienda(s, lis):
	vastus = ""
	for indeks in range(len(s)):
		vastus += lis[indeks] * s[indeks]
	return vastus
