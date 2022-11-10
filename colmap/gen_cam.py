import random
import csv

def gen_cam():
   #generate 100 sample points
   images = []
   file = open('images.csv', 'w')
   writer = csv.writer(file)
   for i in range(100, 0, -1):
      image_data = {}
      image_data["Image_Name"] = i

      #quaternion is 4d
      #each coefficient range from -1 to 1
     
      image_data["QW"] = random.uniform(-1,1)
      image_data["QX"] = random.uniform(-1,1)
      image_data["QY"] = random.uniform(-1,1)
      image_data["QZ"] = random.uniform(-1,1)
     
      #adding translation
      image_data["TX"] = random.uniform(-6,6)
      image_data["TY"] = random.uniform(-6,6) 
      image_data["TZ"] = random.uniform(-6,6)

      images.append(image_data)
   
   with open("images.csv", mode = 'w', newline='') as csv_file:
      csv_file.truncate(0)
      fieldnames = ['Image_Name', 'QW', 'QX', 'QY', 'QZ', 'TX', 'TY', 'TZ']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

      writer.writeheader()
      for image in images:
         writer.writerow(image)  

def gen_3d():
   file = open("points3D.txt", "a")
   points = []
   for i in range(100):
      x = random.uniform(-30,30)
      y = random.uniform(-30,20)
      z = random.uniform(0,40)
      s = str(i) + " "  + str(x) + " "  + str(y) + " " + str(z)
      file.writelines(s)
     


 
