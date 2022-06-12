import numpy as np
from subprocess import call

meanFile = 'mammogram_balanced_mean.npy'
deploy = 'resnet_50_deploy.prototxt'
caffeModel = 'resnet_50_balanced_solver_iter_8950.caffemodel'
pred_result = 'result.npy'

testFile = open('test.txt', 'r')

datatest = testFile.readlines()

i = 0
correct = 0
incorrect = 0

for d in datatest[0:]:
	arr = d.split(' ')
	if len(arr) > 1:
		image = arr[0]
		actual = arr[1].replace('\n', '')
		image = 'test/' + image
		call(['python', classify, image, pred_result, '--model_def', deploy, '--pretrained_model', caffeModel, '--mean_file', meanFile, '--center_only'])
		prediction = np.load('result.npy')
		if str(actual) == str(prediction[0].argmax()):
			correct = correct + 1
			print('Predicting image: ' + image + ' | actual: ' + actual + ' | prediction: ' + str(prediction[0].argmax()) + ' | correct | correct so far: ' + str(correct))
		else:
			incorrect = incorrect + 1
			print('Predicting image: ' + image + ' | actual: ' + actual + ' | prediction: ' + str(prediction[0].argmax()) + ' | incorrect | incorrect so far: ' + str(incorrect))
		
print('Num of correct: ' + str(correct) + ' / 703 | num of inccorect: ' + str(incorrect))