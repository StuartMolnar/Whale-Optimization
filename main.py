import optimizers.WOA as woa
import optimizers.GA as ga


from pprint import pprint
import math
import itertools
import time
import datetime
import csv
import os
import numpy as np

'''
Let's assume nurse prefs are expressed as "aversions", scale of 1-4, where 4 is maximum aversion.
Let's assume for now that we have 5 nurses and 7 days, and we need to schedule 2 nurses per day.
So that's 14 time-slots.  Each nurse must work 2 or 3 shifts total over the 7 days.
Let's assume that there are no hard constraints EXCEPT: no nurse may work adjacent days (no worries about wraparound (for now))
'''

'''
New constraints
Let's assume nurse prefs are expressed as "aversions", scale of 1-4, where 4 is maximum aversion.
Let's assume we have 5 nurses and 7 days.
We need to schedule 1 nurse per day.
Each nurse cannot work more than 2 shifts over 7 days.
Every nurse must work at least 1 shift.
No nurse may work adjacent shifts.
'''
#nurse preferences for working on a given day. nurses do not have individual shift preferences, only day preferences
prefs_input = [
    [4, 4, 2, 4, 1, 3, 2],
    [1, 1, 3, 4, 2, 1, 1],
    [2, 2, 3, 4, 4, 1, 1],
    [1, 3, 4, 2, 1, 1, 1],
    [1, 3, 4, 2, 1, 1, 1]
]




#------------------test section---------------------------
'''
we have two core adjustable values that affect the accuracy of our algorithm
the first is search agents, and the second is iterations
search agents affect how accurate each pass is
iterations affect how many passes we have
the time it takes for our function to complete is going to be a factor of iterations*searchagents
we want to find the set up of iterations and searchagents that finds us a feasible answer in the least amount of time

we also want to run the same tests to find this value of iterations and search agents on the genetic algorithm
and we want to see how the results differ between whale optimization and genetic algorithm
'''
#changes woa output to something we can work with
def refrangulate(arr, stride):
  ans = []
  for index, element in enumerate(arr):
    if index % stride == 0:
      ans.append([])
    ans[-1].append(element)
  return ans


#returns the total aversion of a given assignment by matching it against given preferences
def calculationTotalAversion(prefs, assignment):
  HARD_HATE = len(prefs) * len(prefs[0]) * 20       # 20 is a lot more than 4 (4 is max hate)
  ans = 0

 
  # hard constraint: same nurse not on both shifts
  for day in range(len(assignment[0])):
    if assignment[0][day] == assignment[1][day]:
      ans += HARD_HATE * 10
  
  
  # hard constraint: no adjacent workdays
  for shift in assignment:
    for day in range(1, len(shift)):
      if shift[day-1] == shift[day]:
        ans += HARD_HATE
  
      
  # hard constraint: at most 3 workdays
  # hard constraint: at least 2 workdays
  days_worked = [0] * len(prefs)
  for shift in assignment:
    for day in range(len(shift)):
      days_worked[shift[day]-1] += 1 

  for nurse in days_worked:
    if nurse < 2 or nurse > 3:
      ans += HARD_HATE

  # soft constraints: map current shift to preferences
  nurse_ans = 0
  for shift in assignment:
      for i in range(len(shift)):
          nurse_ans += prefs_input[shift[i]-1][i]
  ans += nurse_ans
   

  return ans


  '''
  # old constraints
  # hard constraint: no nurses works 2 days in a row (ignoring wraparound)

  for day in range(1, len(assignment)):   #7 days in a week
    if assignment[day-1] == assignment[day]:
      ans += HARD_HATE
  

  #hard constraint:
  #  no nurse works more than 2 days
  #  every nurse works at least 1 day
  for nurse in range(len(prefs)):
    days_worked = 0
    for day in assignment:
      if day == nurse+1:
        days_worked+=1
    if days_worked < 1 or days_worked > 2:
      ans += HARD_HATE
  
  nurse_ans = 0
  for day in range(len(assignment)):
    nurse_ans += prefs[assignment[day]-1][day]

  ans += nurse_ans
  
  print('assignment in aversion ')
  for shift in assignment:
    print(shift)
  return 0

  '''




def doNurseOptimization(prefs, SearchAgents, Max_iter, optimizer_name='WOA'):

  # creates a benchmark function (called objf)
  def objf(x):  # this is a closure, wheeeeee
    # rounds every element, and then restructures into a rectangle
    
    #print('vector:', x)
    assignment = refrangulate([math.floor(thing) for thing in x], len(prefs[0]))
    #print('assignment \n', assignment)
    # print(assignment)
    #print('assignment \n', assignment)
    return calculationTotalAversion(prefs, assignment)

  # sets up arguments for optimizer (dim, SearchAgents_no, Max_iter)
  NUM_SHIFTS = 2

  num_days = len(prefs[0])
  dim = NUM_SHIFTS * num_days
  #SearchAgents_no = 30    # edit me
  #Max_iter = 30           # edit me

  # runs optimizer (to get answer)
  raw_woa_ans = woa.WOA(objf, 1, 5, dim, SearchAgents, Max_iter)
  raw_woa_ans_vect = raw_woa_ans.bestIndividual

  raw_woa_ans_vect = [math.floor(elt) for elt in raw_woa_ans_vect]
  woa_ans = refrangulate(raw_woa_ans_vect, len(prefs[0]))

  # says some stuff?  outputs?   whatever?
  return [woa_ans, raw_woa_ans.best]
'''
results = doNurseOptimization(prefs_input, 1000, 5)

for shift in results[0]:
  print(shift)

print(results[1])
'''
def runTest1(prefs, searchagents, max_iter, test_iter):
  #run each set of values multiple times
  #calculate % accuracy (how many solutions are less than 700 aversion)

  scores = []
  num_feasible = 0
  for i in range(test_iter):
    score = doNurseOptimization(prefs, searchagents, max_iter)[1]
    if score < 700:
      num_feasible += 1
    scores.append(score)

  percent_feasible = num_feasible / len(scores)

  return [scores, percent_feasible]

#print(runTest1(prefs_input, 30, 30, 10))

def runTest2(prefs, searchagents, max_iter):
  #run until feasible solution is found, count how many tries it took
  feasible_solution = None
  iterations = 0
  ATTEMPS_ALLOWED = 5

  while not feasible_solution:
    solution = doNurseOptimization(prefs, searchagents, max_iter)[1]
    if solution < 700:
      feasible_solution = solution
    iterations += 1
    if iterations > ATTEMPS_ALLOWED:
      iterations = str(ATTEMPS_ALLOWED) + '+, no solution found'
      break

  return [solution, iterations]
  




def runTest3(prefs, searchagents, max_iter):
  pass

def convertToCsv(results, test, second_column):
  ct = datetime.datetime.now()
  ct = str(ct)[0:-10]
  ct = ct[:-6]+'-'+ct[-5:-3]+'-'+ct[-2:]

  #section to write results to new excel document    
  newSheetName = ct + '-' + test + '.csv'
  cwd = os.getcwd()
  newSheetName = os.path.join(cwd, 'datasheets', newSheetName)
  pprint(results)
  results = sorted(results)

  with open(newSheetName, 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    results.insert(0, ['Total Runs', second_column, 'Search Agents', 'Iterations', 'Time Elapsed'])
    results.insert(0, ['WOA Test 1'])


    for row in results:
        writer.writerow(row)
  writeFile.close()  

  print('Results written to', newSheetName)

def runTests(pref, runOne, runTwo, runThree):
  
  #this takes too much runtime, just hardcode desirable values instead
  #every combination of searchagents and iterations from x-y skipping by z
  COMBINATIONS = [range(1,101, 10), range(1,101, 10)]  
  AGENT_ITER_LIST_TEMP = list(itertools.product(*COMBINATIONS))
  AGENT_ITER_LIST = []
  #maybe iterate over list and remove outlier values at arbitrary number (10k+total iterations maybe)
  for i in range(len(AGENT_ITER_LIST_TEMP)):
    if AGENT_ITER_LIST_TEMP[i][0] * AGENT_ITER_LIST_TEMP[i][1] <= 100:
      AGENT_ITER_LIST.append(AGENT_ITER_LIST_TEMP[i])

  length = len(AGENT_ITER_LIST)
  print(AGENT_ITER_LIST)
  #every combination takes factorial runtime, just hardcode desirable values instead
 
  #------------test 1----------------
  #results = [[searchagents*iterations, percent_feasible, searchagents, iterations, time_elapsed]...]
  if runOne:
    results = []
    TEST_ITERATIONS = 10
    for i in range(length):
      current_combination = AGENT_ITER_LIST[i]
      print('running test 1 with', str(current_combination), 'at iteration', str(i), 'of', str(length))
      start = time.time()
      test_result = runTest1(prefs_input, current_combination[0], current_combination[1], TEST_ITERATIONS)
      end = time.time()
      results.append([current_combination[0] * current_combination[1], str(test_result[1]*100) + '%', current_combination[0], current_combination[1], abs(end - start)])

    #sort results by total iterations
    
    #pprint(results)
    #print(results[np.argsort(results[:,0])])
    convertToCsv(results, 'test1', 'Viable Solutions')

  #------------test 2----------------

  #results = [total runs, tries, search agents, iterations, time elapsed]
  if runTwo:
    results = []
    for i in range(length):
      current_combination = AGENT_ITER_LIST[i]
      print('running test 2 with', str(current_combination), 'at iteration', str(i), 'of', str(length))
      start = time.time()
      test_result = runTest2(prefs_input, current_combination[0], current_combination[1])
      end = time.time()
      results.append([current_combination[0] * current_combination[1], test_result[1], current_combination[0], current_combination[1], abs(end - start)])

    convertToCsv(results, 'test2', '# of Attempts')

  #------------test 3----------------

# TODO 
# come up with third test
# implement tests with genetic algorithm
# DONE figure out why time is not calculated properly


runTests(prefs_input, False, True, False)



 '''
  AGENT_ITER_LIST = [
    #------------
    [5, 10],
    [5, 50],
    [5, 100],
    [5, 500],
    [5, 1000],
    [5, 3000],
    #
    [10, 5],
    [50, 5],
    [100, 5],
    [500, 5],
    [1000, 5],
    [3000, 5],
    #------------
    [15, 10],
    [15, 50],
    [15, 100],
    [15, 500],
    #
    [10, 15],
    [50, 15],
    [100, 15],
    [500, 15],
    #------------
    [50, 10],
    [50, 50],
    [50, 100],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
  ]
  '''

'''
#------------genetic algorithm section-----------------



def calculationTotalAversionGA(prefs, assignment):
  HARD_HATE = len(prefs) * len(prefs[0]) * 20       # 20 is a lot more than 4 (4 is max hate)
  ans = 0

  # hard constraint: 2 nurses on duty today
  for day in range(len(prefs[0])):      # 7 days in week
    num_on_duty = sum([assignment[nurse][day] for nurse in range(len(prefs))])
    if num_on_duty != 2:
      ans += HARD_HATE * 10

  for nurse in range(len(prefs)):
    nurse_ans = 0
    
    # hard constraint: at most 3 workdays
    # hard constraint: at least 2 workdays
    num_workdays = sum(assignment[nurse])
    if num_workdays > 3 or num_workdays < 2:
      nurse_ans += HARD_HATE

    for day in range(len(prefs[0])):      # 7 days in week
      # hard constraint: no adjacent workdays
      if day != 0 and assignment[nurse][day] > 0.5 and assignment[nurse][day-1] > 0.5:
        nurse_ans += HARD_HATE


      # soft constraint: read my prefs you jerk, I asked for Tuesdays, I hate Mondays
      nurse_ans += assignment[nurse][day] * prefs[nurse][day]
    ans += nurse_ans
  return ans


def doNurseOptimizationGA(prefs, optimizer_name='WOA'):

  # creates a benchmark function (called objf)
  def objf(x):  # this is a closure, wheeeeee
    # rounds every element, and then restructures into a rectangle
    
    #print('x \n', x)
    assignment = refrangulate([round(thing) for thing in x], len(prefs[0]))
    #print('assignment \n', assignment)
    # print(assignment)
    return calculationTotalAversionGA(prefs, assignment)

  # sets up arguments for optimizer (dim, SearchAgents_no, Max_iter)
  num_nurses = len(prefs)
  num_days = len(prefs[0])
  dim = num_nurses * num_days
  SearchAgents_no = 30     # FIXME
  Max_iter = 50      # FIXME

  # runs optimizer (to get answer)
  raw_woa_ans = ga.GA(objf, 0, 1, dim, SearchAgents_no, Max_iter)
  raw_woa_ans_vect = raw_woa_ans.bestIndividual

  #print('raw_woa_ans_vect \n', raw_woa_ans_vect)
  raw_woa_ans_vect = [round(elt) for elt in raw_woa_ans_vect]
  woa_ans = refrangulate(raw_woa_ans_vect, len(prefs[0]))

  # says some stuff?  outputs?   whatever?
  return woa_ans

pprint(doNurseOptimizationGA(prefs_input))




#---------------------------------------------------------------------------------------------------------------------
#boolean vs continuous problems
#integer problems vs real value problems

#possible that our problem can't be solved using WOA or a similar algorithm

#try to change what we want our output to be, to better match how WOA works
#woa likes to use float values rather than the boolean 0 and 1 we have assigned it

#some hard constraints are hardcoded to work for boolean values 0 and 1, if we change what our output looks like we need to change how the constraints are checked
'''