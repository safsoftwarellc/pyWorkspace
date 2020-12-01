import pymongo
import pandas

"""
Step2:  Write a Program to read excel Data to Data Frame(26th Nov)
    Single File Program(PyMongoTDM.py)
    Convert Data Frame to JSON Object
    Convert JSON to Dictionary
"""

df = pandas.read_excel('data/SampleData.xlsx')
df.to_json('data/SampleData.json', orient='records')
# print(df)

dict_excel_data = df.to_dict(orient='records')
for row in dict_excel_data:
    print(row)

# Make Dict as Dataframe
daf = pandas.DataFrame.from_dict(dict_excel_data)
print(daf)

"""
Step3:  Write a Program to Store JSON into MongoDB (30th Nov)
        Create Collection
        Store Data into Collection
        Find Data from Collection
        Convert JSON Collection to Data Frame and Dictionary
"""
myclient = pymongo.MongoClient("mongodb://localhost:27017")
my_tdms_db = myclient["TestDataManagement"]
my_tdms_col = my_tdms_db["exceldata"]

print(myclient.list_database_names())
print(my_tdms_db.list_collection_names())

# for row in dict_excel_data:
#    my_tdms_col.insert_one(row)
all_json_objects = my_tdms_col.find()
for x in all_json_objects:
    print(x["Name"])

# for x in all_json_objects:
#    my_tdms_col.delete_one(x)

"""
Download JSON Data into Excel (DF first)
"""
