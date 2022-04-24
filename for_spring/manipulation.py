import sqlite3

con = sqlite3.connect("../db.sqlite3")
cur = con.cursor()

# for i in range(1, 5):
#     query = "INSERT INTO FOR_SPRING_TEST VALUES (?, ?, ?, ?, ?);"
#     cur.execute(query, (i, "title" + str(i), "text" + str(i), "default_image.jpeg", "Anomaly Simulation with tzinfo.csv"))
# con.commit()

query = "SELECT * FROM for_spring_test;"
for row in cur.execute(query):
    print(row)

cur.close()
con.close()
