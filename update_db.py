from mysql.connector import connect
import random
import report
import configparser

config = configparser.ConfigParser()
config.read("C:/Users/Sonit Maddineni/Documents/config.ini")
mydb = connect(
  host = "localhost" ,
  user = config.get('mysql', 'user'),
  password = config.get('mysql', 'password'),
  database = "nchs"
  )
cur = mydb.cursor(buffered=True)
#clears the table
cur.execute("DELETE FROM nchs.data")
mydb.commit()

#stores the points of all students at the end of the quarter
cur.execute('UPDATE nchs.track SET winners = Points')
mydb.commit()

#list of all the prizes for students overall
school_reward = ["Free ticket to a football match", "Pay dues for three of your clubs", "No homework for two days", "50 activity points", "Flex you last hour"]
food_reward = ["Fast lunch pass", "6 donut pack", "Gift card for your favorite restaurant", "Starbucks coffee", "orange crush drink"]
spirit_item = ["School hoodie", "NCHS backpack", "Ironmen water bottle", "NCHS cap", "NCHS T-Shirt"]

#creating a list of prizes for that quarter based off of their points
sqls = ["SELECT winners FROM nchs.track WHERE winners = (SELECT MAX(winners) FROM nchs.track)", "SELECT winners FROM nchs.track WHERE Grade = 9 AND winners = (SELECT MAX(winners) FROM nchs.track WHERE Grade = 9)", "SELECT winners FROM nchs.track WHERE Grade = 10 AND winners = (SELECT MAX(winners) FROM nchs.track WHERE Grade = 10)", "SELECT winners FROM nchs.track WHERE Grade = 11 AND winners = (SELECT MAX(winners) FROM nchs.track WHERE Grade = 11)", "SELECT winners FROM nchs.track WHERE Grade = 12 AND winners = (SELECT MAX(winners) FROM nchs.track WHERE Grade = 12)"]
prizes = []
for ind in range(5):
  cur.execute(sqls[ind])
  point = []
  for i in cur:
    point.append(i)
  print(point)
  try:
    if point[0][0] > 300:
      x = random.choice(school_reward)
      prizes.append(x)
      school_reward.pop(x)
    elif point[0][0] >200:
      x = random.choice(food_reward)
      prizes.append(x)
      food_reward.pop(x)
    else:
      x = random.choice(spirit_item)
      prizes.append(x)
      spirit_item.remove(x)
  except Exception as e:
    pass

#generating random winner from each grade level
cur.execute("SELECT  Name FROM nchs.track t1 WHERE Grade = 9")
grade9 = random.choice([item for item in cur])
cur.execute("SELECT  Name FROM nchs.track t1 WHERE Grade = 10")
grade10 = random.choice([item for item in cur])
cur.execute("SELECT  Name FROM nchs.track t1 WHERE Grade = 11")
grade11 = random.choice([item for item in cur])
cur.execute("SELECT  Name FROM nchs.track t1 WHERE Grade = 12")
grade12 = random.choice([item for item in cur])

#storing these in the database table
cur.execute("INSERT INTO nchs.data (Name) VALUES ('a{}'), ('b{}'), ('c{}'), ('d{}'), ('e{}'), ('f{}'), ('g{}'), ('h{}'), ('i{}')".format(grade9[0], grade10[0], grade11[0], grade12[0], prizes[0], prizes[1], prizes[2], prizes[3], prizes[4]))
mydb.commit()

#generating a report
report.export('Report')

#resetting the points for the next quarter.
cur.execute("UPDATE nchs.track SET Points = 0")
mydb.commit()