import os, json
import numpy as np
import jinja2
import random
import pdfkit

from subprocess import call
from flask import Flask, render_template, request, send_from_directory, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func
from werkzeug import secure_filename
from datetime import datetime


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads/')
CROPPED_IMAGE_FOLDER = os.path.join(APP_ROOT, 'croppedImages/')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mammograms.sqlite3'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CROPPED_IMAGE_FOLDER'] = CROPPED_IMAGE_FOLDER
app.config['SESSION_ID'] = str(datetime.now())
app.jinja_env.filters['zip'] = zip

meanFile = './caffe-windows/python/mammogram_mean.npy'
deploy = './caffe-windows/python/resnet-deploy.prototxt'
caffeModel = './caffe-windows/python/resnet_50_solver_iter_7160.caffemodel'
classify = './caffe-windows/python/classify.py'
cropped_images = app.config['CROPPED_IMAGE_FOLDER']
pred_result = './result.npy'

db = SQLAlchemy(app)

class mammograms(db.Model):
	id = db.Column('file_id', db.Integer, primary_key = True)
	sessionId = db.Column(db.String(50))
	fileName = db.Column(db.String(50))
	fileLocation = db.Column(db.String(100))
	title = db.Column(db.String(50))
	patientName = db.Column(db.String(50))
	breast = db.Column(db.String(10))
	breastView = db.Column(db.String(10))
	notes = db.Column(db.String(100))
	croppedFile = db.Column(db.String(100))

	def __init__(self, sessionId, fileName, fileLocation, title, patientName, breast, breastView, notes, croppedFile):
		self.sessionId = sessionId
		self.fileName = fileName
		self.fileLocation = fileLocation
		self.title = title
		self.patientName = patientName
		self.breast = breast
		self.breastView = breastView
		self.notes = notes
		self.croppedFile = croppedFile

class quizItems(db.Model):
	id = db.Column('question_id', db.Integer, primary_key = True)
	question = db.Column(db.String(100))
	questionImage = db.Column(db.String(50))
	answer = db.Column(db.String(30))
	otherChoice1 = db.Column(db.String(30))
	otherChoice2 = db.Column(db.String(30))
	otherChoice3 = db.Column(db.String(30))
	
	def __init__(self, question, questionImage, answer, otherChoice1, otherChoice2, otherChoice3):
		self.question = question
		self.questionImage = questionImage
		self.answer = answer
		self.otherChoice1 = otherChoice1
		self.otherChoice2 = otherChoice2
		self.otherChoice3 = otherChoice3

@app.route('/')
def home():
	navbarActive = 'home'
	return render_template('home.html', navbar=navbarActive)
		
@app.route('/predict', methods=['GET', 'POST'])
def predict():
	listMammograms = mammograms.query.all()
	for mammogram in listMammograms:
		imageToDelete = mammogram.fileName
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], imageToDelete))
		croppedImageToDelete = mammogram.croppedFile
		if croppedImageToDelete != '':
			os.remove(os.path.join(app.config['CROPPED_IMAGE_FOLDER'], croppedImageToDelete))
		db.session.delete(mammogram)
		db.session.commit()
	
	quiz = quizItems.query.all()
	if len(quiz) < 10:
		deleteQuiz = quizItems.query.all()
		for x in deleteQuiz:
			db.session.delete(x)
			db.session.commit()
			
		question1 = 'Fill in the blank/s of the following statement: ________ is a low-dose x-ray exam. The x-ray images produced by this exam are called ________.'
		questionImage1 = ''
		answer1 = 'Mammography, mammograms'
		otherChoice1a = 'Breast magnetic resonance imaging, MRI scans'
		otherChoice2a = 'Breast ultrasound, breast ultrasound image'
		otherChoice3a = 'Breast x-ray, breast x-ray image'
		quizItem = quizItems(question1, questionImage1, answer1, otherChoice1a, otherChoice2a, otherChoice3a)
		db.session.add(quizItem)
		db.session.commit()
		
		question2 = 'The given image is one of the two standard projections in a screening mammography. What do you call the given projection?'
		questionImage2 = 'craniocaudal.jpg'
		answer2 = 'Craniocaudal view'
		otherChoice1b = 'Mediolateral oblique view'
		otherChoice2b = 'Side projection view'
		otherChoice3b = 'Multi-side view'
		quizItem = quizItems(question2, questionImage2, answer2, otherChoice1b, otherChoice2b, otherChoice3b)
		db.session.add(quizItem)
		db.session.commit()
		
		question3 = 'What is the type of breast cancer described by cancer cells that line the milk ducts of the breast and is contained only in the milk ducts?'
		questionImage3 = ''
		answer3 = 'Ductal carcinoma in situ'
		otherChoice1c = 'Invasive ductal carcinoma'
		otherChoice2c = 'Lobular carcinoma in situ'
		otherChoice3c = 'Invasive lobular carcinoma'
		quizItem = quizItems(question3, questionImage3, answer3, otherChoice1c, otherChoice2c, otherChoice3c)
		db.session.add(quizItem)
		db.session.commit()
		
		question4 = 'The following types of masses typically define benign tumors except for one:'
		questionImage4 = ''
		answer4 = 'Spiculated masses'
		otherChoice1d = 'Round masses'
		otherChoice2d = 'Oval masses'
		otherChoice3d = 'Lobulated masses'
		quizItem = quizItems(question4, questionImage4, answer4, otherChoice1d, otherChoice2d, otherChoice3d)
		db.session.add(quizItem)
		db.session.commit()
		
		question5 = 'The given image is a type of mass that indicates malignancy. Which of the following types of mass is indicated here?'
		questionImage5 = 'spiculated.jpg'
		answer5 = 'Spiculated masses'
		otherChoice1e = 'Irregular masses'
		otherChoice2e = 'Obscured masses'
		otherChoice3e = 'Lobulated masses'
		quizItem = quizItems(question5, questionImage5, answer5, otherChoice1e, otherChoice2e, otherChoice3e)
		db.session.add(quizItem)
		db.session.commit()
		
		question6 = 'The following are common symptoms of breast cancer except for one:'
		questionImage6 = ''
		answer6 = 'Nipple numbness'
		otherChoice1f = 'Nipple discharge'
		otherChoice2f = 'Redness of the nipple'
		otherChoice3f = 'Nipple pain'
		quizItem = quizItems(question6, questionImage6, answer6, otherChoice1f, otherChoice2f, otherChoice3f)
		db.session.add(quizItem)
		db.session.commit()
		
		question7 = 'Fill in the blank/s of the following: _________ is the use of drugs to destroy cancer cells usually by inhibiting the ability of the cancer cells to grow and spread.'
		questionImage7 = ''
		answer7 = 'Chemotherapy'
		otherChoice1g = 'Radiation therapy'
		otherChoice2g = 'Hormonal therapy'
		otherChoice3g = 'Targeted therapy'
		quizItem = quizItems(question7, questionImage7, answer7, otherChoice1g, otherChoice2g, otherChoice3g)
		db.session.add(quizItem)
		db.session.commit()
		
		question8 = 'The image shows a mammogram with a large round region of interest indicated by the line. Is this a benign or malignant calcification?'
		questionImage8 = 'benigncalcification.jpg'
		answer8 = 'Benign calcification'
		otherChoice1h = 'Malignant calcification'
		otherChoice2h = ''
		otherChoice3h = ''
		quizItem = quizItems(question8, questionImage8, answer8, otherChoice1h, otherChoice2h, otherChoice3h)
		db.session.add(quizItem)
		db.session.commit()
		
		question9 = 'The image shows a region of interest of a mammogram indicated by an arrow. What type of mass is shown here?'
		questionImage9 = 'roundmass.jpg'
		answer9 = 'Round mass'
		otherChoice1i = 'Irregular mass'
		otherChoice2i = 'Spiculated mass'
		otherChoice3i = 'Lobulated mass'
		quizItem = quizItems(question9, questionImage9, answer9, otherChoice1i, otherChoice2i, otherChoice3i)
		db.session.add(quizItem)
		db.session.commit()
		
		question10 = 'Fill in the blank/s of the following: _________ targets the resources (proteins, specific genes, tissue environment) that fuel the survival and growth of cancer.'
		questionImage10 = ''
		answer10 = 'Targeted therapy'
		otherChoice1j = 'Chemotherapy'
		otherChoice2j = 'Radiation therapy'
		otherChoice3j = 'Hormonal therapy'
		quizItem = quizItems(question10, questionImage10, answer10, otherChoice1j, otherChoice2j, otherChoice3j)
		db.session.add(quizItem)
		db.session.commit()
		
	if request.method == 'POST':
		errorMessage = ''
	
		if 'file' not in request.files:
			errorMessage = 'No file uploaded.'
			return Response(json.dumps(errorMessage), status=500, mimetype='application/json')
		
		imageGalleryRender = ''
		
		for file in request.files.getlist("file"):
			if file.filename == '':
				errorMessage = 'No filename uploaded.'
				return Response(json.dumps(errorMessage), status=500, mimetype='application/json')
			
			if file and isFileAllowed(file.filename):
				sessionId = app.config['SESSION_ID']
				filename = secure_filename(file.filename)
				fileLocation = 'predict/' + filename
				title = filename
				patientName = 'Unregistered'
				breast = 'Unregistered'
				breastView = 'Unregistered'
				notes = 'No description yet.'
				croppedFile = ''
				file.save("".join([app.config['UPLOAD_FOLDER'], filename]))
				mammogram = mammograms(sessionId, filename, fileLocation, title, patientName, breast, breastView, notes, croppedFile)
				db.session.add(mammogram)
				db.session.commit()
				
				id = mammograms.query.filter_by(fileName=filename).first().id
				
				imageGalleryRender += 	'<div style="width: 200px;" class="col-lg-4 col-md-5 col-xs-6 mx-lg-0 mx-md-5 mx-sm-6 mb-lg-4 mb-md-3 mb-sm-2 container thumbnail-container" thumbnail-id="' + str(id) + '" thumbnail-src="predict/' + filename + '"> \n' \
										'		<div class="card" style="width: 18rem;"> \n ' \
										'			<div class="card-body"> \n' \
										'				<span class="modal-icon delete-icon d-inline float-right" data-toggle="tooltip" data-placement="top" title="Delete"> \n' \
										'					<i class="fas fa-trash-alt fa-lg"></i> \n' \
										'				</span> \n' \
										'				<span class="modal-icon mr-1 edit-icon d-inline float-right" data-target="#modal" data-toggle="modal" data-toggle="tooltip" data-placement="top" title="Edit"> \n' \
										'					<i class="far fa-edit fa-lg"></i> \n' \
										'				</span> \n' \
										'				<h5 id="card_' + str(id) + '_title" class="card-title">' + filename + '</h5> \n' \
										'				<p id="card_' + str(id) + '_patientName" class="card-text">Patient name: ' + patientName + '</p> \n' \
										'				<p id="card_' + str(id) + '_breast" class="card-text">Breast: ' + breast + '</p> \n' \
										'				<p id="card_' + str(id) + '_breastView" class="card-text">Mammogram view: ' + breastView + '</p> \n' \
										'				<p id="card_' + str(id) + '_notes" class="card-text">Description: ' + notes + '</p> \n' \
										'			</div> \n' \
										'			<a href="" class="d-block thumbnail" style="z-index: 3;" data-target="#modal" data-toggle="modal"> \n' \
										'				<div class="thumbnail-img-container" data-imageSource="predict/id=' + str(id) + '"> \n' \
										'  					<img class="card-img-bottom img-responsive" src="predict/' + filename + '" alt="Card image cap" /> \n' \
										'					<div class="overlay"> \n' \
										'				  		<img src="/static/images/edit-icon.png" /> \n' \
										'					</div> \n' \
										'				</div> \n' \
										'			</a> \n' \
										'		</div> \n' \
										'</div> \n'
			else:
				errorMessage = 'Only .png, .jpg, and .jpeg files are accepted.'
				return Response(json.dumps(errorMessage), status=500, mimetype='application/json')
		
		return Response(json.dumps(imageGalleryRender),  mimetype='application/json')
		
	navbarActive = 'predict'
	return render_template('predict.html', navbar=navbarActive)
	
@app.route('/predict/id=<id>')
def sendImageById(id):
	filename = mammograms.query.filter_by(id=id).first().fileName
	return sendImage(filename)

@app.route('/predict/<filename>')
def sendImage(filename):
	return send_from_directory('uploads', filename)

@app.route('/delete', methods=['POST'])
def deleteMammogram():
	idMammogram = request.form['id']
	mammogram = mammograms.query.filter_by(id=idMammogram).first()
	imageToDelete = mammogram.fileName
	os.remove(os.path.join(app.config['UPLOAD_FOLDER'], imageToDelete))
	croppedImageToDelete = mammogram.croppedFile 
	if croppedImageToDelete != '':
		os.remove(os.path.join(app.config['CROPPED_IMAGE_FOLDER'], croppedImageToDelete))
	db.session.delete(mammogram)
	db.session.commit()
	return Response(json.dumps('success'),  mimetype='application/json')

@app.route('/deleteAll', methods=['POST'])
def deleteAll():
	listMammograms = mammograms.query.all()
	for mammogram in listMammograms:
		imageToDelete = mammogram.fileName
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], imageToDelete))
		croppedImageToDelete = mammogram.croppedFile 
		if croppedImageToDelete != '':
			os.remove(os.path.join(app.config['CROPPED_IMAGE_FOLDER'], croppedImageToDelete))
		db.session.delete(mammogram)
		db.session.commit()
	return Response(json.dumps('success'),  mimetype='application/json')
	
@app.route('/saveMammogram', methods=['POST'])
def saveMammogram():
	idMammogram = request.form['id']
	mammogram = mammograms.query.filter_by(id=idMammogram).first()
	mammogram.title = request.form['title']
	if mammogram.title == '':
		mammogram.title = 'Unlabeled'
	mammogram.patientName = request.form['patientName']
	if mammogram.patientName == '':
		mammogram.patientName = 'Unspecified'
	mammogram.breast = request.form['breast']
	mammogram.breastView = request.form['breastView']
	mammogram.notes = request.form['notes']
	db.session.commit()
	mammogram = mammograms.query.filter_by(id=idMammogram).first()
	return Response(json.dumps('Updated successfully'),  mimetype='application/json')

@app.route('/saveCroppedFile', methods=['POST'])
def saveCroppedFile():
	file = request.files['croppedFile']
	idMammogram = request.form['id']
	mammogram = mammograms.query.filter_by(id=idMammogram).first()
	fileName = mammogram.fileName.split('.')[0] + '_' + file.name + '_' + str(idMammogram) + '.png'
	file.save("".join([app.config['CROPPED_IMAGE_FOLDER'], fileName]))
	mammogram = mammograms.query.filter_by(id=idMammogram).first()
	mammogram.croppedFile = fileName
	db.session.commit()
	return Response(json.dumps('Updated successfully'),  mimetype='application/json')
	
@app.route('/predictResults')
def predictResults():
	listMammograms = mammograms.query.all()
	navbarActive = 'predict'
	
	call(['python', classify, cropped_images, pred_result, '--model_def', deploy, '--pretrained_model', caffeModel, '--mean_file', meanFile, '--center_only'])

	res = []
	data = np.load('result.npy')
	for d in data:
		predMade = np.argmax(d)
		if predMade == 0:
			res.append('Benign mass')
		elif predMade == 1:
			res.append('Malignant mass')
		elif predMade == 2:
			res.append('Benign calcification')
		else:
			res.append('Malignant calcification')
	
	return render_template('predictResults.html', mammograms=listMammograms, navbar=navbarActive, result = res)
	
@app.route('/predictResults/<filename>')
def sendCroppedFile(filename):
	croppedImageToDelete = filename
	return send_from_directory('croppedImages', filename)

@app.route('/pdfPredictResults')
def pdfPredictResults():
	listMammograms = mammograms.query.all()
	res = []
	data = np.load('result.npy')
	for d in data:
		predMade = np.argmax(d)
		if predMade == 0:
			res.append('Benign mass')
		elif predMade == 1:
			res.append('Malignant mass')
		elif predMade == 2:
			res.append('Benign calcification')
		else:
			res.append('Malignant calcification')
	path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
	config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
	rendered = render_template('pdfPredictResults.html', mammograms=listMammograms, result=res, filepath=app.config['CROPPED_IMAGE_FOLDER'])
	css = ['./static/css/bootstrap.min.css', './static/css/pdfResults.css']
	pdf = pdfkit.from_string(rendered, False, configuration=config, css=css)
	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Diposition'] = 'inline; filename=output.pdf'
	return response
	
@app.route('/quiz', methods=['GET'])
def quiz():
	quiz = quizItems.query.order_by(func.random()).limit(10).all()
	quizData = []
	navbarActive = 'quiz'
	i = 0
	for quizItem in quiz:
		otherChoices = []
		quizId = quizItem.id
		otherChoices.append(quizItem.answer)
		otherChoices.append(quizItem.otherChoice1)
		otherChoices.append(quizItem.otherChoice2)
		otherChoices.append(quizItem.otherChoice3)
		if quizItem.otherChoice2 != '':
			random.shuffle(otherChoices)
		quizDataItem = {'id': quizId, 'question': quizItem.question, 'questionImage': quizItem.questionImage, 'correctAnswer': quizItem.answer, 'otherChoices': otherChoices}
		quizData.append(quizDataItem)
	return render_template('quiz.html', quizItems=quizData, navbar=navbarActive)

@app.route('/quizResults', methods=['POST'])
def quizResults():
	score = 0
	quizResultsDataForRender = []
	for i in range(0, 10):
		id = request.form['id' + str(i)]
		quizItem = quizItems.query.filter_by(id=id).first()
		question = quizItem.question
		questionImage = quizItem.questionImage
		correctAnswer = quizItem.answer
		otherChoices = []
		otherChoices.append(quizItem.answer)
		otherChoices.append(quizItem.otherChoice1)
		otherChoices.append(quizItem.otherChoice2)
		otherChoices.append(quizItem.otherChoice3)
		if quizItem.otherChoice2 != '':
			random.shuffle(otherChoices)
		answer = request.form['answer' + str(i)]
		if quizItem.answer == request.form['answer' + str(i)]:
			result = 'Correct'
			score += 1
		else:
			result = 'Incorrect'
		i += 1
		quizResultItem = {'questionRender': question, 'questionImage': questionImage, 'correctAnswer': correctAnswer, 'otherChoices' : otherChoices, 'userAnswer': answer, 'quizResult': result}
		quizResultsDataForRender.append(quizResultItem)
	navbarActive = 'quiz'
	return render_template('quizResults.html', navbar=navbarActive, quizResultsData=quizResultsDataForRender, finalScore=score)
	
def isFileAllowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
	db.create_all()
	app.run()
	