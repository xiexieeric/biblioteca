from pyspark import SparkContext
from itertools import combinations

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file
data = data.distinct()


# 1 - Read data in as pairs of (user_id, item_id clicked on by the user)
# (user_id, item_id)

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

# 2 - Group data into (user_id, list of item ids they clicked on)
# (user_id, [item ids they clicked on])

grouped_data = pairs.groupByKey()

# 3 - Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
# (user_id, (item1, item2)) (user_id, (item1, item3)) ...

transformed_pairs = grouped_data.flatMap(lambda group: [(group[0], tuple(sorted(combination))) for combination in combinations(group[1], 2)])
reversed_transformed_pairs = transformed_pairs.map(lambda id_pair: (id_pair[1], id_pair[0]))


# 4 - Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
# ((item1, item2), [user1, user2, user3]

co_clicked = reversed_transformed_pairs.groupByKey()


# 5 - Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
# ((item1, item2), 4)

count_clicks = co_clicked.map(lambda co_click: (co_click[0], len(co_click[1])))


# 6 - Filter out any results where less than 3 users co-clicked the same pair of items
# [(('1', '4'), 3), (('1', '3'), 3), (('3', '4'), 5)]

filtered_results = count_clicks.filter(lambda pair: pair[1] > 2)
print(filtered_results.collect())

sc.stop()