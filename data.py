from sqlite3 import *

db=connect('database.db')
cur=db.cursor()


def check(name,password):
    try:
        cur.execute(f"select * from score where username='{name}'")   
        c=cur.fetchone()
        if c[1]==password:
            return True
        else:
            return False
    except TypeError:
        return False
    
    
    # query="insert into score values(?,?,?)"
    # data=(name,password,hscore)
    # cur.execute(query,data)
    # db.commit()


def update(name,nhscore):
    query=f"UPDATE score SET highscore={nhscore} WHERE username='{name}'"

    cur.execute(query)
    db.commit()

# name=input("enter your username: ")
# nhscore=int(input("enter your new high score: "))
# update(name,nhscore)

# cur.execute("INSERT INTO score(username,password) VALUES('aditya','adi123')")
# cur.execute("select * from score")
# print(cur.fetchall())
# db.commit()
#cur.execute("delete from score where password='aditya123'")
#db.commit()
#Anshu:- [shriyanshu,anshu123]
#Shanu:-[shanu,manu]
#Vaibhav[vaibhav,vaibhav]
#aditya['aditya','adi123']



def new(name,password):
    flag=True
    cur.execute("select * from score")
    for i in cur:
        if name==i[0]:
            flag=False

    if flag==True:  
        query="INSERT INTO score(username,password) VALUES(?,?)"
        data= (name,password)
        cur.execute(query,data)
        db.commit()
    else:
        return -1


def give(name):
    c=f"select highscore from score where username='{name}'"
    cur.execute(c)
    a = cur.fetchone()
    return a[0]

def test():
    c="select * from score"
    cur.execute(c)
    for i in cur.fetchall():
        print(i)



if __name__=='__main__':
    test()