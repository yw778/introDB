import random
import time

a1=(2011,7,1,0,0,0,0,0,0)
a2=(2017,8,6,23,59,59,0,0,0)

def league():
	file = open('league.csv', 'w')
	out = []
	for i in xrange(1, 4):
		prize = random.randint(0, 1000) * 10000
		out.append(str(i) + "," + str(prize) + "\n")

	file.writelines(out)
	file.flush()
	file.close()

def item():
	file = open('item.csv', 'w')
	out = []
	for i in xrange(1, 11):
		price = random.randint(0, 150)*50
		out.append(str(i) + "," + str(price) + "\n")

	file.writelines(out)
	file.flush()
	file.close()

def hero():
	file = open('hero.csv', 'w')
	out = []
	for i in xrange(1, 21):
		ability = ["XP Gain", "Damage", "Mana", "Attack Speed", "Health"]
		out.append(str(i) + "," + ability[random.randint(0, 4)] + "\n")

	file.writelines(out)
	file.flush()
	file.close()

def proteam():
	file = open('pro_team.csv', 'w')
	out = []
	for i in xrange(1, 6):
		out.append(str(i) + "\n")

	file.writelines(out)
	file.flush()
	file.close()

def matchhost():
	file = open('match_host.csv', 'w')
	out = []
	j = 0
	start=time.mktime(a1)
	end=time.mktime(a2)
	for i in xrange(1, 31):
		if i%10 == 1:
			j += 1
		t=random.randint(start,end)
		date_touple=time.localtime(t)
		date=time.strftime("%Y-%m-%d",date_touple)
		tm = time.strftime("%H:%M:%S", date_touple)
		out.append(str(i)+","+str(j)+","+date+","+tm+"\n")

	file.writelines(out)
	file.flush()
	file.close()

def teamcompose():
	file = open('team_compose.csv', 'w')
	out = []
	for i in xrange(1, 31):
		win = 0+1*random.randint(0,1)
		fb = 0+1*random.randint(0,1)
		for j in xrange(0, 2):
			out.append(str(i)+","+str(j)+","+str((j+fb)%2)+","+str((j+win)%2)+","+str(random.randint(0,11))+"\n")

	file.writelines(out)
	file.flush()
	file.close()

def playin():
	file = open('play_in.csv', 'w')
	out = []
	for i in xrange(1, 31):
		pt = []
		pt.append(random.randint(1, 5))
		pt.append(random.randint(1, 5))
		while pt[1] == pt[0]:
			pt[1] = random.randint(1, 5)
		for j in xrange(0, 2):
			out.append(str(i)+","+str(j)+","+str(pt[j])+"\n")

	file.writelines(out)
	file.flush()
	file.close()

def playerconsistof():
	file = open('player_consist_of.csv', 'w')
	out = []
	j = 0
	pos = [1, 2, 3, 4, 5]
	for i in xrange(1, 26):
		if i%5 == 1:
			j += 1
			random.shuffle(pos)
		out.append(str(i)+","+str(pos[i%5])+","+str(j)+"\n")

	file.writelines(out)
	file.flush()
	file.close()

def pick():
	file = open('pick.csv', 'w')
	read = open('play_in.csv', 'r')
	out = []
	hids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	mid = 0
	pt = 0
	for line in read:
		l = line.split(",")
		pt += 1
		if mid != l[0]:
			mid = l[0]
			random.shuffle(hids)
			pt = 0
		for i in xrange(5):
			pid = int(l[2])*5-i
			hid = hids[pt*5 + i]
			out.append(str(pid)+","+str(hid)+","+str(mid)+"\n")

	file.writelines(out)
	file.flush()
	file.close()

def own():
	file = open('own.csv', 'w')
	read = open('pick.csv', 'r')
	out = []
	iids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	start=time.mktime(a1)
	end=time.mktime(a2)
	for line in read:
		l = line.split(",")
		mid = int(l[2])
		hid = int(l[1])
		random.shuffle(iids)
		for i in xrange(3):
			iid = iids[i]
			t=random.randint(start,end)
			date_touple=time.localtime(t)
			tm = time.strftime("%M:%S", date_touple)
			out.append(str(iid)+","+str(hid)+","+tm+","+str(mid)+"\n")

	file.writelines(out)
	file.flush()
	file.close()

def belongto():
	file = open('belong_to.csv', 'w')
	read = open('pick.csv', 'r')
	out = []
	radiant = 0
	cnt = 0
	for line in read:
		cnt += 1
		l = line.split(",")
		mid = int(l[2])
		hid = int(l[1])
		lasthit = random.randint(0, 1500)
		death = random.randint(0,30)
		kill = random.randint(0, 30)
		level = random.randint(1, 25)
		denies = random.randint(0, 200)
		gpm = random.randint(150, 1200)
		assist = random.randint(0, 50)
		xpm = random.randint(150, 1200)
		out.append(str(mid)+","+str(radiant)+","+str(hid)+","+str(lasthit)+","+str(death)+","+str(kill)+","+str(level)+","+str(denies)+","+str(gpm)+","+str(assist)+","+str(xpm)+"\n")

		if cnt%5 == 0:
			radiant = 1-radiant

	file.writelines(out)
	file.flush()
	file.close()

def participate():
	file = open('participate.csv', 'w')
	out = []
	for i in xrange(1, 4):
		for j in xrange(1, 6):
			out.append(str(i)+","+str(j)+"\n")

	file.writelines(out)
	file.flush()
	file.close()




belongto()