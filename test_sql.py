import sqlite3

conn = sqlite3.connect("tasks.db")
conn.execute("UPDATE tasks SET done = 1")
conn.commit()

print("All tasks:")
for row in conn.execute("SELECT * FROM tasks"):
    print(row)

print("\nCompleted tasks:")
for row in conn.execute("SELECT * FROM tasks WHERE done = 1"):
    print(row)

print("\nTotal tasks:")
print(conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0])

conn.close()