import os, glob, uuid

folder = 'milk_cond'
path = os.getcwd() + "\data\images\\" + folder + '\\'

for file in glob.glob(path + '*.jpg'):
    newfilename = path + folder + '_' + str(uuid.uuid1()) + '.jpg'

    print('Old name: ' + file)
    print('New name: ' + newfilename)
    
    os.rename(file, newfilename)

