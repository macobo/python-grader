def mood(l):
	elemendid = list(set(l))
	elemendid.sort()
	moodsaid = 0
	for elem in elemendid:
		kogus = l.count(elem)
		if kogus > moodsaid:
			moodsaim = elem
			moodsaid = kogus
	return moodsaim
