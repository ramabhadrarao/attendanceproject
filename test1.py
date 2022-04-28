import pymongo
conn=pymongo.MongoClient("mongodb://localhost:9999")
mydb=conn['studentattendance']
courses=mydb['courses']
batches=mydb['batches']
semesters=mydb['semesters']
course_list=[{
    "course_name":"MCA",
    "course_code":"1F",
    "course_duration":2,
    "course_level":"PG"
},
{
    "course_name":"MBA",
    "course_code":"1E",
    "course_duration":2,
    "course_level":"PG"
}

]

status=courses.insert_many(course_list)
print(status.inserted_ids)