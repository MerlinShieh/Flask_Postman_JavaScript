SimpleCheckJson.py
	使用方式 
		json_1 = {'code':200}
		json_2 = {'code':400,'name':'Bob'}
	简单判断json_1的key是否是json_2的key的子集
		python SimpleCheckJson.py json_1 json_2
		output True


StrictCheckJson.py
	使用方式
		json_1 = {'code':200}
		json_2 = {'code':400}
		json_3 = {'code':200,'name':'Bob'}

	严格检查json_1是不是json_2的子集，key和value都要满足
		python StrictCheckJson.py json_1 json_2
		output False
		python StrictCheckJson.py json_1 json_3
		outpt True