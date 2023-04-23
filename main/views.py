from django.shortcuts import render
from django.http import HttpResponse
import random


#Function Parameters:
#numCourses-> number of given courses to be scheduled
#courses -> number of given constraints (courses, rooms, times, professors, and needed room capacity) to be scheduled
#popSize-> number of chromosomes to be in the population
#times-> All available slots for given courses
#rooms-> All available rooms for given courses
#maxIters-> The maximum iterations to go through the main loop of the genitic algorithm..(the while loop)
#isElite-> A boolean value to allow the mutation process of elitism
#The function genAlg takes these constrains and courses to schedule them

def genAlg(numCourses,courses,popSize,times,rooms,maxIters,isElite):
	#Create an empty list population
	population = []
	fit = []
	#looping from 0 -> number of chromosomes to be in the population
	for i in range(0,popSize):
		#looping from 0 -> number of chromosomes to be in the population
		for j in range(0,numCourses):
			#Add a random time from the list of times to the population list 
			population.append(times[random.randrange(0,len(times))])
			#Add a random room from the list of rooms to the population list 
			population.append(rooms[random.randrange(0,len(rooms))])
			#Add courses to the list (population) from the (courses) list
			population.append(courses[0+5*j])
			#Add the professors to the list (population) from the (courses) list
			population.append(courses[1+5*j])
			#Add the Requested time to the list (population) from the (courses) list
			population.append(courses[2+5*j])
			#Add the Requested rooms to the list (population) from the (courses) list
			population.append(courses[3+5*j])
			#Add the needed room size to the list (population) from the (courses) list
			population.append(courses[4+5*j])

	#the list (fit) = the output of the function (Fitness)
	#with population,popSize,numCourses,rooms, and times as parameters
	fit = fitness(population,popSize,numCourses,rooms,times)

	i = 0

	#while i<(The maximum iterations to go through that loop) 
	# & the highest constraint score/number of given courses to be scheduled <0.9
	while (i < maxIters) and ((float(max(fit))/(numCourses*7)) < 0.9):
		print (i)
		#Creating a new list (newPop)
		newPop = []
		#putting (fit) list in a new variable (toPull)
		toPull = fit[:]
		#sorting toPull from the lowest to the highest constraint fitness score
		toPull.sort()
		toPull = toPull[int(0.9*len(toPull)):len(toPull)]
		#creting a new list topIndexs
		topIndexs = []
		#putting (fit) list in a new variable (tempFit)
		tempFit = fit[:]
		#creting a new list tempPop
		tempPop = []
		for j in range(0,len(toPull)):
			#putting the indexes of the constraints with the highiest fitness scores in the top indexs list
			topIndexs.append(tempFit.index(toPull[j]))
			tempFit[topIndexs[j]] = 0
			#tempPop=tempPop+ population[form (topIndexs[j]*7*numCourse) -> (topIndexs[j]*7*numCourses)+7*numCourses]
			tempPop += population[topIndexs[j]*7*numCourses:(topIndexs[j]*7*numCourses)+7*numCourses]

		for j in range(0,popSize):
			#Check if is Elite is True
			if isElite:
			#Create a new variable howToReproduce which contains a random value
				howToReproduce = random.random()
			#Create a new variable r which contains a random number from the range of(0 -> lenghth of top indexes)
				r = random.randrange(0,len(topIndexs))
				#Create a variable winner which contains
				#tempPop list[r*number of constraints->(r*number of constraints)+number of constraints]
				winner = tempPop[(r*numCourses*7):((r*numCourses*7)+(numCourses*7))]
				
				child = 0
				
				if howToReproduce < 0.15:
					#child == the output of the mutation function
					#with winner,numCourses,times, and rooms as parameters
					child = mutate(winner,numCourses,times,rooms)
				else:
					#assign howToReproduce to a random value from the range of (0 -> 3)
					howToReproduce = random.randrange(0,3)
					#check if howToReproduce == 0
					if howToReproduce == 0:
						#child == the output of the swapRooms function
						#with winner,numCourses, and rooms as parameters
						child = swapRooms(winner,numCourses,rooms)
					#check if howToReproduce == 1
					elif howToReproduce == 1:
						#child == the output of the swapTimes function
						#with winner,numCourses, and times as parameters
						child = swapTimes(winner,numCourses,times)
					else:
						#child == the output of the changeCourseTime function
						#with winner,numCourses, and times as parameters
						child = changeCourseTime(winner,numCourses,times)

				#check if the output of the fitness function with the child as the list of the new population
						# > the output of the fitness function with the winner as the list of the new population
				if fitness(child,1,numCourses,rooms,times)[0] > fitness(winner,1,numCourses,rooms,times)[0]:
					#newPop = newPop + child
					newPop += child
				else:
					#newPop = newPop + winner
					newPop += winner
			else:
				#create 2 variables pick1, pick2 which equal a random number
				#from the range of (0 -> number of chromosomes to be in the population)
				pick1 = random.randrange(0,popSize)
				pick2 = random.randrange(0,popSize)

				winner = 0
				#check if the list fit with index of pick1>the list fit with index of pick2
				if fit[pick1] > fit[pick2]:
					winner = pick1
				else:
					winner = pick2

				#winner=list of population[from winner*number of constraints -> (winner*number of constraints)+number of constraints]
				winner = population[(winner*numCourses*7):((winner*numCourses*7)+(numCourses*7))]
				#howToReproduce = a random value
				howToReproduce = random.random()
				child = 0
				#check if the random value of howToReproduce<0.15
				if howToReproduce < 0.15:
					#child == the output of the mutation function
					#with winner,numCourses,times, and rooms as parameters
					child = mutate(winner,numCourses,times,rooms)
				else:
					#assign howToReproduce to a random value from the range of (0 -> 3)
					howToReproduce = random.randrange(0,3)
					#check if howToReproduce == 0
					if howToReproduce == 0:
						#child == the output of the swapRooms function
						#with winner,numCourses, and rooms as parameters
						child = swapRooms(winner,numCourses,rooms)
					#check if howToReproduce == 1
					elif howToReproduce == 1:
						#child == the output of the swapTimes function
						#with winner,numCourses, and times as parameters
						child = swapTimes(winner,numCourses,times)
					else:
						#child == the output of the changeCourseTime function
						#with winner,numCourses, and times as parameters
						child = changeCourseTime(winner,numCourses,times)
				#check if the output of the fitness function with the child as the list of the new population
					# > the output of the fitness function with the winner as the list of the new population
				if fitness(child,1,numCourses,rooms,times)[0] > fitness(winner,1,numCourses,rooms,times)[0]:
					#newPop=newPop + child
					newPop += child
				else:
					#newPop=newPop + winner
					newPop += winner
		#population list equal the newPop list
		population = newPop[:]
		#fit = the output of the fitness function 
		#with population,popSize,numCourses,rooms and times as parameters
		fit = fitness(population,popSize,numCourses,rooms,times)
		i += 1
	#create a new variable maxIndex which equals index of the constraint with highest
	#fitness score in the fit list 
	maxIndex = fit.index(max(fit))
	#Return the scehduale with the constraints with highest fitness scores
	return population[7*maxIndex:7*maxIndex+7*numCourses]

#Function swapRooms-> Takes a single chromosome(Schedule), a number of courses in that schedule, and the available rooms for these courses
	#Function parameters are:
	#schedule-> A single chromosome
	#numCourses-> The number of constraints in the schedule
	#rooms-> The available rooms for these given courses
#The function should return a new chromosome (schedule) by swapping the rooms in that schedule

def swapRooms(schedule,numCourses,rooms):
  #Defining a new chromosome called sched containing the given one
  sched = schedule[:]
  #Defining a variable room1 that contains rooms a random available room from the range of (0, the lenghtgh of the list of available rooms)
  room1 = rooms[random.randrange(0,len(rooms))]
  #Defining a variable room2 that contains rooms a random available room from the range of (0, the lenghtgh of the list of available rooms)
  room2 = rooms[random.randrange(0,len(rooms))]
  #looping through sched with step size of 7(number of constraints in the schedule)
  #swapping room1 elements with room2
  for i in range(0,len(sched),7):
    if sched[i+1] == room1:
      sched[i+1] = room2
    elif sched[i+1] == room2:
      sched[i+1] = room1
#Return the new scheduale (sched)
  return sched

#Function swapTimess-> Takes a single chromosome(Schedule), a number of courses in that schedule, and the available times for these courses
	#Function parameters are:
	#schedule-> A single chromosome
	#numCourses-> The number of constraints in the schedule
	#times-> The available times for these given courses
#The function should return a new chromosome (schedule) by swapping the times in that schedule

def swapTimes(schedule,numCourses,times):
	#Defining a new chromosome called sched conraining the given one
  sched = schedule[:]
  #Defining a variable times1 that contains times a random available time from the range of (0, the lenghtgh of the list of available times)
  time1 = times[random.randrange(0,len(times))]
    #Defining a variable times2 that contains times a random available time from the range of (0, the lenghtgh of the list of available times)
  time2 = times[random.randrange(0,len(times))]
    #looping through sched with step size of 7(number of constraints in the schedule) and swapping time1 elements with time2
  for i in range(0,len(sched),7):
    if sched[i] == time1:
      sched[i] = time2
    elif sched[i] == time2:
      sched[i] = time1
      #return a new chromosome (schedule) by swapping the times in that schedule
  return sched

# Function changeCourseTime-> Takes a single chromosome(Schedule), a number of courses in that schedule, and the available times for these courses
	#Function parameters are:
	#schedule-> A single chromosome
	#numCourses-> The number of constraints in the schedule
	#times-> The available times for these given courses#
# Returns a new schedule by randomly changing the time of a single course

def changeCourseTime(schedule,numCourses,times):
	#Defining a new chromosome called sched conraining the given one
  sched = schedule[:]
  #Defining a variable time that contains times a random available time from the range of (0, the lenghtgh of the list of available times)
  time = times[random.randrange(0,len(times))]
  #Defining a variable course that contains a random number from the range of (0, the number of given constraints)
  course= random.randrange(0,numCourses)
	#Assigning the random time to a random constraint
  sched[course*7] = time
  #return the new scheduale
  return sched

#Function mutate-> Takes a single chromosome(Schedule), a number of courses in that schedule, the available times for these courses, and the available rooms
	#Function parameters are:
	#schedule-> A single chromosome
	#numCourses-> The number of constraints in the schedule
	#times-> The available times for these given courses
	#rooms-> The available rooms for these given courses
#Returns a new schedule by randomly changing both time and room for a single course

def mutate(schedule,numCourses,times,rooms):
#Defining a new chromosome called sched conraining the given one
  sched = schedule[:]
  #Defining a variable time that contains times a random available time from the range of (0, the lenghtgh of the list of available times)
  time = times[random.randrange(0,len(times))]
  #Defining a variable time that contains times a random available time from the range of (0, the lenghtgh of the list of available times)
  room = rooms[random.randrange(0,len(rooms))]
  #Defining a variable course that contains a random number from the range of (0, the number of given constraints)
  course= random.randrange(0,numCourses)
#Assigning the random time to a random constraint
  sched[course*7] = time
  #Assigning the random room to a random constraint after the time
  sched[course*7+1] = room
#return the new scheduale
  return sched

#Function fitness-> Takes a number of schedules, The number of courses in each schedule, the available rooms for these courses, and the available times
	#Function parameters are:
	#pop-> a list of new population
	#popSize-> A number of given schedules
	#numCourses-> The number of constraints in the schedule
	#rooms-> The available rooms for these given courses
	#times-> The available times for these given courses
#Returns a list containing each fitness score

def fitness(pop,popSize,numCourses,rooms,times):
	#Create a new empty list (fit)
	fit = []
	#loop through the number of the given courses
	for i in range(0,popSize):
		#Create a variable (afit) which equals a 0
		afit = 0
		#Create a variable curChrom and put all constraints in it
		curChrom = i*numCourses*7
		#looping through the range of (0 -> number of constraints with step size of 7 )
		for j in range(0,numCourses*7,7):
			#Creating a variable sameTimeSameRoom which has a score of 2
			sameTimeSameRoom = 2
			#Creating a variable sameTimeSameProf which has a score of 2
			sameTimeSameProf = 2
			#Creating a variable requestedRoom which has a score of 0
			requestedRoom = 0
			#Creating a variable requestedTime which has a score of 0
			requestedTime = 0
			#Creating a variable roomSizeNeed which has a score of 1
			roomSizeNeed = 1
			#Create a variable temp time which contains the 1st constraint in the new population->Time
			tempTime = pop[curChrom+j]
			#Create a variable temp time which contains the 2nd constraint in the new population->Room
			tempRoom = pop[curChrom+j+1]
			#Create a variable temp time which contains the 4th constraint in the new population->Professor
			tempProf = pop[curChrom+j+3]

			#loop through the new population constraints
			#Check if the rquested time is 5th constraint in the new population
			#increase the score of the requestedTime from 0 -> 1
			for k in range(0,len(pop[curChrom+j+4])):
				if(pop[curChrom+j+4][k] == tempTime):
					requestedTime = 1
					break
			
			#loop through the new population constraints
			#Check if the rquested room is 6th constraint in the new population
			#increase the score of the requestedRoom from 0 -> 1
			for k in range(0,len(pop[curChrom+j+5])):
				if(pop[curChrom+j+5][k] == tempRoom):
					requestedRoom = 1
					break

			#looping from the last constraint on the 1st slot (8th element)-> the number of total constraints
			#with a step size of 7
			for k in range(j+7,numCourses*7,7):

			#Check if tempTime is the 1st constraint and tempRoom is the 2nd constraint in the new population
				if (tempTime == pop[curChrom+k]) and (tempRoom == pop[curChrom+k+1]):
					#sameTimeSameRoom equals 0
					sameTimeSameRoom = 0
			#Check if tempTime is the 1st constraint and tempProf is the 4th constraint in the new population
				if (tempTime == pop[curChrom+k]) and (tempProf == pop[curChrom+k+3]):
					#sameTimeSameProf equals 0
					sameTimeSameProf = 0
			#afit= afit + sameTimeSameRoom + sameTimeSameProf + requestedRoom + requestedTime + roomSizeNeed
			#get the final score of each constraint
			afit += sameTimeSameRoom + sameTimeSameProf + requestedRoom + requestedTime + roomSizeNeed
		#add each fitness score to the list (fit)
		fit.append(afit)
	#Return the list fit
	return fit

# Testing the code

#list of given courses
courses = ['CS304','CS217','CS201','CS205']
#list of given professros
profs = ['El-Attar','Hadidy','Nashwa','Zeinab','A.Hassan','Mohab','Amira','Dina']
#list of given available slots
times = ['1st Slot','2nd Slot','5th slot','6th slot','3rd slot','4th Slot','7th Slot','8th Slot']
#list of given rooms
rooms = ['G18','129','209','F17','S18']

initial = []
#i in range (0, lenghths of all given lists combined)
for i in range(0,25):
	#ranrange(0, lenghth of each list)
	initial.append(courses[random.randrange(0,4)])
	initial.append(profs[random.randrange(0,8)])
	temp = []
	#putting times in temp then adding temp to the initial
	temp.append(times[random.randrange(0,8)])
	temp.append(times[random.randrange(0,8)])
	initial.append(temp)
	#putting rooms in temp2 then adding temp2 to the initial
	temp2 = []
	temp2.append(rooms[random.randrange(0,5)])
	temp2.append(rooms[random.randrange(0,5)])
	initial.append(temp2)
	initial.append(20)




def homepage(request):
	courses = genAlg(25,initial,100,times,rooms,1000,True)
	return render(request = request, template_name = "main/home.html", context = {"courses":courses})