import subprocess

def convertBinaryprotoToNpy():
	convert = './caffe-windows/python/convert.py'
	proto = './caffe/data/mammo_resnet_50/mammogram_mean.binaryproto'
	npy = './caffe/data/mammo_resnet_50/mammogram_mean.npy'
	call(['python', convert, proto, npy])

def trainModel(solver, log, parse):
	subprocess.Popen(['git-bash', 'train.sh', solver, log])
	
def predict(input, output, meanFile, deploy, model)
	classify = './caffe-windows/python/classify.py'
	call(['python', classify, input, output, '--model_def', deploy, '--pretrained_model', model, '--mean_file', meanFile, '--center_only'])