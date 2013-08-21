def tagurpidi(sone):
    if sone == '': return ''
    return tagurpidi(sone[1:]) + sone[0]