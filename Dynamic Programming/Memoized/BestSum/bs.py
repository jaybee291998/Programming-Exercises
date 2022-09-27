def bestSum(n, arr, memo = {}):
	if n == 0:	return []
	if n < 0:	return None
	if n in memo :	return memo[n]

	besRes = None
	for num in arr:
		res = bestSum(n - num, arr, memo)
		if res != None:
			res = res.copy()
			res.append(num)
			if besRes == None or len(res) < len(besRes):
				besRes = res
	memo[n] = besRes
	return besRes
memo = {}
for i in  range(10, 100):
	print("bestSum[" + str(i) + "]=" + str(bestSum(i, [1,2,5,25], memo)))