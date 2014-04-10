def korduvate_summa(arvud):
  temp = []
  for i in range(len(arvud)):
    if arvud[i] in arvud[0:i]:
      temp.append(arvud[i])
  return sum(temp) + sum(set(temp))
