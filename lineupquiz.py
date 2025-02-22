
import sqlite3
conn = sqlite3.connect('quiz2.sqlite')
cur = conn.cursor()


cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS lb (user TEXT, score INTEGER)')
isloggedin = False
while True:
    fq = input('Select action. Type "create" to create an account or "login" to log into your account Type "quit" to exit: ') #asks whether to log in or create account
    if fq == "create":
        username = input ("Enter your username here: ")
        pwd = input ("Enter your password here: ")
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        altak = cur.fetchall()
        if len(altak) > 0 and altak[0][0] == username:
            print ('Username already taken. Please try again with another username')
            continue
        else:
            cur.execute ('INSERT INTO users (username, password) VALUES (?, ?)', (username, pwd,))
            user = username
            isloggedin = True
            score = 0
            cur.execute ('INSERT INTO lb (user, score) VALUES (?, ?)', (user, score))
            print ('You have succesfully created your account')
            conn.commit()
            break
    elif fq == "login":
        username = input ("Enter your username here: ")
        pwd = input ("Enter your password here: ")
        cur.execute ('SELECT * FROM users WHERE username = ?', (username,))
        altak = cur.fetchall()
        if len (altak) > 0 and altak[0][0] == username and altak[0][1] == pwd:
            user = username
            cur.execute ("SELECT score FROM lb WHERE user = ?", (user,))
            score = cur.fetchall()[0][0]
            isloggedin = True
            print ('You have succesfully logged in')
            break
        else:
            print ("Login credentials incorrect. Please try again.")
            continue
    elif fq == "quit": quit()
    else: print ("Command not recognised. Please try again.")

print ("Please wait, loading teams...")



import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import random

try:
    html = urllib.request.urlopen("https://gpracingstats.com/constructors/").read()
except:
    print ("You need an internet connection to take this quiz. Please connect to the internet and try again.")
    quit()
soup = BeautifulSoup(html, 'html.parser')
divs = soup ('div')
cons = list()
for div in divs:    
    fd = div.get ('class', None)
    if fd is not None and fd[0] == 'scroll':
        inshtml = str(div)
        soup = BeautifulSoup(inshtml, 'html.parser')
        links = soup ('a')
        for link in links:
            fl = link.get ('href', None)
            if fl is not None and fl.startswith ('https://gpracingstats.com/constructors/') is True:
                cons.append (link.string)

def lowered (list_):
    voc = []
    for x in list_:
        voc.append(x.lower())
    return voc
allans = []
while isloggedin is True:
    mtr = input ('Type in command. For a question, type "play". To view leaderboard, type "score". To quit, type "quit": ')   
    if mtr == "play":
        ct = random.choice (cons)
        url = 'https://gpracingstats.com/constructors/' + urllib.parse.quote(ct.lower().replace(' ', '-'))
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup('table')
        dryr = dict ()
        lup = list()
        for table in tables:
            ff = table.get ('class', None)
            if ff is not None and ff == ['summary', 'sortable', 'constructor-seasons', 'hl-col-3', 'align-r-4', 'data-items-4']:
                inshtml = str(table)
                soup = BeautifulSoup(inshtml, 'html.parser')
                tds = soup ('td')
                for td in tds:
                    ins2html = str (td)
                    soup = BeautifulSoup (ins2html, 'html.parser')
                    time = soup ('time')
                    if time != []:
                        year = time[0].string                    
                    clas = td.get ('class', None)
                    if clas is not None and clas == ['nowrap', 'driver-col']:
                        drivers = soup ('a')
                        for driver in drivers:
                            lup.append (driver.string)
                            dryr[year] = lup    
                        lup = []                
        answered = False
        chosen = random.choice(list(dryr.items()))
        while answered is False:
            voc = []
            print ("Team: " + ct)
            print ("Year: " + chosen[0])
            count = 0
            voc = lowered (chosen[1])
            while count < len (chosen[1]):
                v = input("Enter driver: ")
                allans.append (v.title())
                if v is not None or v != '':
                    count += 1
                else:
                    continue
                if v.lower() in voc:
                    score = score + 5 
                    print ("✔️")
                else: print ("❌")
            print ("Your answers: ")
            for y in allans:
                if y in chosen[1]:
                    print (y + " ✔️")
                else: print (y + " ❌")
            print ()
            triggered = False
            for v in chosen [1]:
                if v in allans:
                    continue
                else:
                    if triggered is False:
                        print ("The drivers you missed: ")  
                        triggered = True
                    print (v)                
            print ("\n") 
            answered = True
            allans = []
            cur.execute ("UPDATE lb SET score = ? WHERE user = ?", (score, user,))
            conn.commit()
    elif mtr == "quit":
        print ("Thank you for playing.")
        quit()
    elif mtr == "score":
        cur.execute ("SELECT * FROM lb ORDER BY score DESC")
        leadbrd = cur.fetchall()
        count = 1
        for item in leadbrd:
            if item[0] == user:
                ust = item[0] + " (You)"
            else:
                ust = item [0]
            if count == 1:
                print ("🥇 " + ust + ": " + str(item[1]))
            elif count == 2:
                print ("🥈 " + ust + ": " + str(item[1]))
            elif count == 3:
                print ("🥉 " + ust + ": " + str(item[1]))
            else:
                print (ust + ": " + str(item[1]))       
            count = count + 1
        print ("\n")   
    else:
        print ("Command not recognised. Please try again.")
