from pyspark import SparkContext
sc = SparkContext("local", "MaxTempByCity")

data = sc.textFile("test.csv").map(lambda line: line.split(","))
print(data.collect())
data = data.filter(lambda x: x[1] != "null")
data = data.map(lambda x: (x[0], float(x[2])))
print(data.collect())
max_temps = data.reduceByKey(lambda x, y: max(x, y))
print(data.collect())

for city, max_temp in max_temps.collect():
    print(f"{city}: {max_temp}")
sc.stop()