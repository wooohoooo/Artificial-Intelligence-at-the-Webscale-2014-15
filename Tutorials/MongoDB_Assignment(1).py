import numpy as np
import pymongo



#create dataset
num_feet = np.random.random_integers(100,2500,10000)

num_rooms = np.random.random_integers(2,10,10000)

prices = 400 * num_feet + 25*num_rooms + np.random.normal(0,1000)

#establish connection
client = pymongo.MongoClient()
db = client.test_database #db = client['test-database']

collection = db.test_collection

houses = db.houses
house_attributes = zip(num_feet,num_rooms,prices)

#Store Simulated Dataset

for feet,rooms,price in house_attributes:
	house = {"feet" : feet,
	"rooms" : rooms,
	"price" : price}
	#"tags" : ["mongodb","python","pymongo"],
	#"date": datetime.datetime.utcnow()}
	house_id = houses.insert(house)




#print db.collection_names()

houses.find_one()



#ADD SHORT DESCRIPTION

desc_list = ['cozy','seaside','garden','farm','murder happened here']*2
for i in range(10):
	feet,rooms,price = house_attributes[i]

	descr_house = houses.find_one({"feet" : feet,
	"rooms" : rooms,
	"price" : price})
	ID = descr_house['_id']
	print 'before'
	print  houses.find_one({"_id":ID}) 
#simple use of update
	houses.update({'_id':ID},{"feet" : feet,
	"rooms" : rooms,
	"price" : price,
	"_description":desc_list[i]})
#use push. Mind the difference: 'desc' is an array of values, while _description is only one value
	houses.update({'_id':ID},{'$push':{'desc':desc_list[i]}})
	print '\n after'
	print  houses.find_one({"_id":ID}) 
	
	
#select all houses that have a description
cursor = houses.find({"desc" : {'$exists':True}})

#count all of them
print(cursor.count())
#print(db.command({'dbstats': 1}))


###find all houses with price higher than X and number of rooms y

x = 100000
y = 4

cursor = houses.find({"price":{"$gt":x}},{"rooms":4})

print(cursor.count())
