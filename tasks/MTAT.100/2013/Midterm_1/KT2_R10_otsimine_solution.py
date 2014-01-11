f = open("sonad.txt", encoding="utf-8")
lines = list(map(lambda x: x.strip(), f.readlines()))
f.close()
notfound = True

while(notfound):
  sis = input("Sisesta sõna algus: ")
  results = []

  for word in lines:
    if word[0:len(sis)] == sis:
      results.append(word)

  if len(results) == 0:
    print("Sellist sõna ei leidu.")
  elif len(results) == 1:
    print(results[0])
    notfound = False
  else:
    print("Leidub mitu sellise algusega sõna:")
    for word in results:
      print(word)
