def loenda(sone):
  if sone == "": return []
  res = []
  running = ""
  count = 0
  for i in range(len(sone)):
    if sone[i] == running:
      count+=1
    else:
      if not i==0: 
        res.append(count)
      running=sone[i]
      count = 1
  res.append(count)
  return res
