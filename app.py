from flask import Flask, render_template, request
from keras.models import load_model
# from keras.preprocessing import image
from keras.utils import load_img, img_to_array 
import math

app = Flask(__name__)

dic = {0 : 'Crying', 1 : 'Not Crying'}

model = load_model('model.h5')

model.make_predict_function()

def predict_label(img_path):
	i = load_img(img_path, target_size=(100,100))
	i = img_to_array(i)/255.0
	i = i.reshape(1, 100,100,3)
	p = model.predict(i)[0]
	if p[0] > p[1]:
		return dic[0]
	return dic[1]


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/about")
def about_page():
	return "BANNARI AMMAN INSTITUTE OF TECHNOLOGY !!!"

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)