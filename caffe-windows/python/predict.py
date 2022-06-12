import os
import glob
import cv2
import caffe
import lmdb
import numpy as np
from caffe.proto import caffe_pb2
import sys

caffe.set_mode_cpu() 

#Size of images
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224


'''
Image processing helper function
'''
def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img


'''
Reading mean image, caffe model and its weights 
'''
#Read mean image
mean_blob = caffe_pb2.BlobProto()
with open("test",'r') as f:
    mean_blob.ParseFromString(f.read())
mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
    (mean_blob.channels, mean_blob.height, mean_blob.width))


#Read model architecture and trained model's weights
net = caffe.Net(sys.argv[1], sys.argv[2],caffe.TEST)
#net = caffe.Net('../models/heart_enlargement_model/deploy.prototxt',
#                '../models/heart_enlargement_model/new_model_iter_4000.caffemodel',
#                caffe.TEST)

#Define image transformers
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', mean_array)
transformer.set_transpose('data', (2,0,1))


'''
Making predicitions
'''
test_img_paths = []
##Reading image paths

for img in os.listdir('./test'):
    test_img_paths.append('./test/'+img)
    print(img)

test_ids = []
preds = []

#Making predictions
num = 0
for img_path in test_img_paths:
    print(img_path)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
    
    net.blobs['data'].data[...] = transformer.preprocess('data', img)
    out = net.forward()
    pred_probas = out['prob']
    print(net.forward())

    test_ids = test_ids + [img_path.split('/')[-1][:-4]]
    preds = preds + [pred_probas.argmax()]

    print (img_path, pred_probas)
    print (pred_probas.argmax())
    print ('-------')
    num += 1


'''
Making submission file
'''
with open("./predict.csv","w+") as f:
    f.write("id,label\n")
    for i in range(len(test_ids)):
        f.write(str(test_ids[i])+","+str(preds[i])+"\n")
f.close()
