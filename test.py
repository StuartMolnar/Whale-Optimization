prefs_input = [
    [4, 4, 2, 4, 1, 3, 2],
    [1, 1, 3, 4, 2, 1, 1],
    [2, 2, 3, 4, 4, 1, 1],
    [1, 3, 4, 2, 1, 1, 1],
    [1, 3, 4, 2, 1, 1, 1]
]
#              4  3  4  4  2  1  1
assignment = [[1, 4, 4, 2, 2, 2, 4],
#              2  3  3  4  2  3  1
              [3, 4, 3, 1, 2, 1, 4]]

'''
sum= 0 
for shift in assignment:
    for i in range(len(shift)):
        print(prefs_input[shift[i]-1][i])
        sum+= prefs_input[shift[i]-1][i]




import itertools
test_list = [range(1,301, 10), range(1,301, 10)]
output = list(itertools.product(*test_list))

print(output[-100])
print(len(output))


#results = [[percent_feasible, searchagents, iterations, time_elapsed]...]
results = [
    ['20%', 10, 30, 0.04],
    ['100%', 50, 80, 6.7]
]

import datetime
import csv
import os
ct = datetime.datetime.now()
ct = str(ct)[0:-10]
ct = ct[:-6]+'-'+ct[-5:-3]+'-'+ct[-2:]
print(ct)


#section to write 2D array values to new excel document    
newSheetName = ct + '-test1.csv'
cwd = os.getcwd()
newSheetName = os.path.join(cwd, 'datasheets', newSheetName)


with open(newSheetName, 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    results.insert(0, ['Percent Feasible', 'Search Agents', 'Iterations', 'Time Elaped'])
    for row in results:
        writer.writerow(row)
writeFile.close()  

print('Results written to', newSheetName)
'''
'''
results = [
 [1, '0.0%', 1, 1, 0.0020541000000000587],
 [11, '0.0%', 1, 11, 0.0009764999999999358],
 [21, '0.0%', 1, 21, 0.002705099999999905],
 [11, '0.0%', 11, 1, 0.0022841999999998475],
 [121, '0.0%', 11, 11, 0.0008455999999998909],
 [231, '0.0%', 11, 21, 0.0002922999999999121],
 [21, '0.0%', 21, 1, 0.0006737000000005544],
 [231, '20.0%', 21, 11, 0.0005370999999994019],
 [441, '30.0%', 21, 21, 0.00032469999999928945]
]

results = sorted(results)

import time

start = time.time()
x = 0
for i in range(100000000):
  x += 1
end = time.time()
print(start, end, end-start)
'''
from pprint import pprint
#sum_results = [[searchagents*iterations, tries, searchagents, iterations, time elapsed],
                # [searchagents*iterations, tries, searchagents, iterations, time elapsed],
                #  ...
                # ]


results1 = [
            [1000, 5, 10, 100, 3],
            [1000, 3, 100, 10, 2],
            [500, 2, 50, 10, 2],
            [100, 8, 10, 10, 1]
           ]
results2 = [
            [1000, 11, 10, 100, 6],
            [1000, 1, 100, 10, 2],
            [500, 1, 50, 10, 4],
            [100, 12, 10, 10, 2]
           ]

'''
results1 = [
    [1, 1, 1, 1],
    [2, 2, 2, 2]
]

results2 = [
    [3, 3, 3, 3],
    [4, 4, 4, 4]
]
'''
'''
sum_results = [results1, results2]

end_results = []
for inner_length in range(len(sum_results[0])):

    temp = []
    for outer_length in (range(len(sum_results))):
        temp.append(sum_results[outer_length][inner_length])

    print(temp)
    print('---')

    new_temp = temp[0]
    total = 1
    for i in range(1, len(temp)):
        #print('i', i)
        #print(new_temp[1])
        new_temp[1] += temp[i][1]
        new_temp[4] += temp[i][4]
        total += 1

    new_temp[1] = str(round((new_temp[1] / total), 2))
    new_temp[4] = str(round((new_temp[4] / total), 2))
    print('newtemp')
    print(new_temp)
    print('---')

    end_results.append(new_temp)

pprint(end_results)
'''
sum_results = [
    
    [
      #[total runs, tries, searchagents, iterations, time]
      [100, 10, 10, 10, 0.6313107013702393], 
      [200, 5, 20, 10, 0.5595159530639648]
    ],
    [
      [100, 8, 10, 10, 0.45081615447998047], 
      [200, 2, 20, 10, 0.2234022617340088]
    ],
    [
      [100, 10, 10, 10, 0.6068825721740723], 
      [200, 1, 20, 10, 0.11021018028259277]
    ]
  ]

ATTEMPS_ALLOWED = 100
'''

  =>

  [
    #[total runs, success_rate, average tries, searchagents, iterations, average time]
    [100, ignore this part, (tries+tries+tries)/3, 10, 10, (time+time+time)/3]
    [200, ignore this part, (tries+tries+tries)/3, 10, 10, (time+time+time)/3]
  ]

'''
'''
formatted_res = [[0] * (len(sum_results[0][0])+1) for i in range(len(sum_results[0]))]
print(formatted_res)


for j in range(len(sum_results[0])):
    formatted_res[j][1] = sum(1 for matrix in sum_results if matrix[j][1] < ATTEMPS_ALLOWED) / len(sum_results)
    formatted_res[j][2] = sum(matrix[j][1] for matrix in sum_results) / len(sum_results)
    formatted_res[j][5] = sum(matrix[j][4] for matrix in sum_results) / len(sum_results)
    
'''

import csv

filesheet = input('Write the name of filesheet to convert in current directory: ')

with open(filesheet, 'r') as read_file:
  data = csv.reader(read_file, delimiter=',')

  results = []
  for i in range(len(data)):
    if i >= 2:
      results.append(data[i])

  print(results)

