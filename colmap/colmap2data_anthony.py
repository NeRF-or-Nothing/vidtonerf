import sys
import csv

if len(sys.argv) != 3:
    print("Invalid usage. Correct usage: python ImagePositionExtractor \"images.txt\" \"Output.csv\"")
    sys.exit()

infile = open(sys.argv[1], 'r')
lines = infile.readlines()
images = []


for line in lines:
    words = line.split(' ')
    if words[-1].endswith(".JPG\n"):
        image_data = {}
        qw = words[1]
        qx = words[2]
        qy = words[3]
        qz = words[4]
        tx = words[5]
        ty = words[6]
        tz = words[7]
        imageName = words[-1][:-1]
        print(imageName + "- QW:" + qw + ", QX:" + qx + ", QY:" + qy + ", QZ:" + qz + ", TX:" + tx +", TY:" + ty +", TZ:" + tz)

        image_data["Image_Name"] = imageName
        image_data["QW"] = qw
        image_data["QX"] = qx
        image_data["QY"] = qy
        image_data["QZ"] = qz
        image_data["TX"] = tx
        image_data["TY"] = ty
        image_data["TZ"] = tz
        images.append(image_data)

with open(sys.argv[2], mode='w', newline='') as csv_file:
    csv_file.truncate(0)
    fieldnames = ['Image_Name', 'QW', 'QX', 'QY', 'QZ', 'TX', 'TY', 'TZ']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for image in images:
        writer.writerow(image)


