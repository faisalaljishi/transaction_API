from random import randrange
from proof_of_concept import User

def test1():
    u = User()
    u.earn("DANNON", 300)
    u.earn("UNILEVER", 200)
    u.spend(200)
    u.earn("MILLER COORS", 10000)
    u.earn("DANNON", 1000)
    u.spend(5000)
    printer(u)

def test2():
    u = User()
    u.earn("DANNON", 10000)
    u.earn("UNILEVER", 200)
    u.spend(200)
    u.earn("MILLER COORS", 100)
    u.earn("DANNON", 100)
    u.spend(5000)
    printer(u)

def test3():
    u = User()
    u.earn("DANNON", 100)
    u.earn("UNILEVER", 200)
    u.spend(200)
    u.earn("MILLER COORS", 100)
    u.earn("DANNON", 100)
    u.earn("DANNON", 100)
    u.earn("MILLER COORS", 400)
    u.earn("UNILEVER", 800)
    u.spend(1200)
    printer(u)

def test4():
    u = User()
    u.earn("DANNON", 600)
    u.earn("UNILEVER", 600)
    u.spend(1200)
    u.earn("MILLER COORS", 800)
    u.earn("DANNON", 500)
    u.earn("MILLER COORS", 400)
    u.earn("UNILEVER", 800)
    u.spend(2500)
    printer(u)

def test5():
    u = User()
    for _ in range(25):
        u.earn("DANNON", 100)
    u.spend(2500)
    printer(u)


def testR():
    u = User()
    u.earn("DANNON", randrange(1,20)*100)
    u.earn("UNILEVER", randrange(1,20)*100)
    u.spend(200)
    u.earn("MILLER COORS", randrange(1,20)*100)
    u.earn("DANNON", randrange(1,20)*100)
    u.earn("MILLER COORS", randrange(1,20)*100)
    u.earn("UNILEVER", randrange(1,20)*100)
    u.earn("DANNON", randrange(1, 20) * 100)
    u.earn("MILLER COORS", randrange(1, 20) * 100)
    u.spend(1200)
    printer(u)

def printer(u):
    print(u.payers)
    print(u.fundQueue)
    print(u.transactionHistory)


# test1()
# test2()
test3()
# test4()
# test5()
# testR()