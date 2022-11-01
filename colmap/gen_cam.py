import random
import csv

def gen_cam():
   #generate 100 sample points
   q_point = []
   for i in range(100, 0, -1):
      q = []
      q.append(i)

      #quaternion is 4d
      #each coefficient range from -1 to 1
      for j in range(4):
         q.append(random.uniform(-1,1))

      #adding translation
      for j in range(3):
         q.append(random.uniform(-6,6))

      q.append(1)
      q.append('img_'+str(i))
      q_point.append(q)
      print(q)
   # write to csv
   with open('gen_point.csv', 'w', encoding='UTF8', newline='') as f:
      writer = csv.writer(f)

      writer.writerows(q_point)


