import matplotlib
matplotlib.use('Agg')
import flask
from flask import Flask, request, render_template, session
from sklearn.externals import joblib
import numpy as np
from scipy import misc
from flask import send_from_directory

from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage import measure
from skimage.measure import regionprops

import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.transform import resize
import simplejson as json
import cv2
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'sdkjfhsjkdfhskjdfhkjshdfkjshdf'
	
@app.route("/")
@app.route("/index")
def index():
	session['username'] = "Hey there!"
	return flask.render_template('index.html')

@app.route("/description")
def description():
	return flask.render_template('description.html')

@app.route('/img/<path:path>')
def send_img(path):
	return send_from_directory('./',path)

@app.route('/detect_plate', methods=['POST'])
def detectPlate():
	print(session['username'])
	if request.method=='POST':
		file = request.files['image']
		if not file: return render_template('index.html', label="No file")

		original_image = file.filename
		session['original_image'] = original_image
		print('original_image',original_image)
		filename = secure_filename(file.filename)
		
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		car_image = imread(file, as_gray=True)
		gray_car_image = car_image * 255
		fig, (ax1, ax2) = plt.subplots(1, 2)
		ax1.imshow(gray_car_image, cmap="gray")
		threshold_value = threshold_otsu(gray_car_image)
		binary_car_image = gray_car_image > threshold_value
		# print(binary_car_image)
		ax2.imshow(binary_car_image, cmap="gray")
		# ax2.imshow(gray_car_image, cmap="gray")
		# plt.show()
	label_image = measure.label(binary_car_image)

	plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0], 0.15*label_image.shape[1], 0.3*label_image.shape[1])
	plate_dimensions2 = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
	min_height, max_height, min_width, max_width = plate_dimensions
	plate_objects_cordinates = []
	plate_like_objects = []

	fig, (ax1) = plt.subplots(1)
	ax1.imshow(gray_car_image, cmap="gray")
	flag =0
	# regionprops creates a list of properties of all the labelled regions
	for region in regionprops(label_image):
	    # print(region)
	    if region.area < 50:
	        #if the region is so small then it's likely not a license plate
	        continue
	        # the bounding box coordinates
	    min_row, min_col, max_row, max_col = region.bbox

	    region_height = max_row - min_row
	    region_width = max_col - min_col
	    # print(region_height)
	    # print(region_width)

	    # ensuring that the region identified satisfies the condition of a typical license plate
	    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
	        flag = 1
	        plate_like_objects.append(binary_car_image[min_row:max_row,
	                                  min_col:max_col])
	        plate_objects_cordinates.append((min_row, min_col,
	                                         max_row, max_col))
	        rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
	                                       linewidth=2, fill=False)
	        ax1.add_patch(rectBorder)
	        # let's draw a red rectangle over those regions
	if(flag == 1):
	    # print(plate_like_objects[0])
	    # plt.show()
		plt.axis('off')
		plt.savefig('car.png',bbox_inches='tight')
	if(flag==0):
	    min_height, max_height, min_width, max_width = plate_dimensions2
	    plate_objects_cordinates = []
	    plate_like_objects = []

	    # regionprops creates a list of properties of all the labelled regions
	    for region in regionprops(label_image):
	        if region.area < 50:
	            #if the region is so small then it's likely not a license plate
	            continue
	            # the bounding box coordinates
	        min_row, min_col, max_row, max_col = region.bbox

	        region_height = max_row - min_row
	        region_width = max_col - min_col
	        # print(region_height)
	        # print(region_width)

	        # ensuring that the region identified satisfies the condition of a typical license plate
	        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
	            # print("hello")
	            plate_like_objects.append(binary_car_image[min_row:max_row,
	                                      min_col:max_col])
	            plate_objects_cordinates.append((min_row, min_col,
	                                             max_row, max_col))
	            rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
	                                           linewidth=2, fill=False)
	            ax1.add_patch(rectBorder)
	            # let's draw a red rectangle over those regions
	    # print(plate_like_objects[0])
	    # plt.show()
	    plt.axis('off')
	    plt.savefig('car.png', bbox_inches='tight')
	filename = 'car.png'
	plate_obj = plate_like_objects[0]
	# print(plate_obj)
	plate_obj = plate_obj.tolist()
	session['plate_obj'] = plate_obj
	# print("Getting out from: detectPlate", session['plate_obj'])
	return render_template('segment.html',label=filename)

characters = []

column_list = []
@app.route('/segment_characters', methods=['POST'])
def segmentCharacters():
	if request.method=='POST':
		car_image = imread('car.png')
		# print(session['plate_obj'])
		license_plate = np.invert(session['plate_obj'])

		labelled_plate = measure.label(license_plate)

		fig, ax1 = plt.subplots(1)

		ax1.imshow(license_plate, cmap="gray")

		character_dimensions = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
		min_height, max_height, min_width, max_width = character_dimensions

		# characters = []
		counter=0
		# column_list = []
		for regions in regionprops(labelled_plate):
		    y0, x0, y1, x1 = regions.bbox
		    region_height = y1 - y0
		    region_width = x1 - x0

		    if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
		        roi = license_plate[y0:y1, x0:x1]

		        rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
		                                       linewidth=2, fill=False)
		        ax1.add_patch(rect_border)

		        resized_char = resize(roi, (20, 20))
		        characters.append(resized_char)

		        column_list.append(x0)
		plt.axis('off')
		plt.savefig('segmented_car.png', bbox_inches='tight')
		print('characters',characters)
		print('column_list',column_list)
		print(type(characters)) # Iska outout kya hau?Lst
		print(type(column_list))
		
	filename = 'segmented_car.png'
	return render_template('predict.html',label = filename)

@app.route('/predict_characters', methods=['POST'])
def make_prediction():
	if request.method=='POST':
		global characters 
		global column_list
		classification_result = []
		# characters = session['plate_characters']

		for each_character in characters:
		    # converts it to a 1D array
		    each_character = each_character.reshape(1, -1);
		    result = model.predict(each_character)
		    classification_result.append(result)

		print('Classification result')
		print(classification_result)

		plate_string = ''
		for eachPredict in classification_result:
		    plate_string += eachPredict[0]

		print('Predicted license plate')
		print(plate_string)
		column_list_copy = column_list[:]
		column_list.sort()
		rightplate_string = ''
		for each in column_list:
		    rightplate_string += plate_string[column_list_copy.index(each)]

		print('License plate')
		print(rightplate_string)
		print(session['original_image'])
		original_image = session['original_image']
		filename = 'uploads/'+original_image
		characters = []
		column_list = [] 
		return render_template('result.html',  image = filename, label=rightplate_string)


if __name__ == '__main__':
	filename = 'finalized_model.sav'
	model = pickle.load(open(filename, 'rb'))
	app.run(host='0.0.0.0', port=8000, debug=True)