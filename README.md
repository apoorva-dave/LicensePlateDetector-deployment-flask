# LicensePlateDetector-deployment-flask
Deployment of ML model using flask

Flask is a web application framework written in Python. I have deployed my previous project of LicensePlateDetector using Flask as an api.
This is an easy and quick way to see your models in production.

# Setup

1. Clone the repository
2. Run api.py. (Make sure Apache server is running)
3. Go to localhost:8000 to see your application in action. (Port 8000 has been configured in api.py)

 ![img1](https://user-images.githubusercontent.com/19779081/50811360-f9fedc80-1333-11e9-91e2-32e2110df052.PNG)
 
4. Browse an input image of car ( can download from my LicensePlateDetector repo). Click on Detect License Plate

![img2](https://user-images.githubusercontent.com/19779081/50811428-3c281e00-1334-11e9-91ea-1a4a18b6fff8.PNG)

5. Click on segment characters to segment the license plate.

![img3](https://user-images.githubusercontent.com/19779081/50811462-64178180-1334-11e9-84c8-8cbafed9349c.PNG)

6. On clicking of Predict Characters, ML trained model is loaded and is used for prediction of characters of plate.

![img4](https://user-images.githubusercontent.com/19779081/50811485-92955c80-1334-11e9-9ef9-1829d701b6f1.PNG)

A brief description about the process is mentioned in the description tab.

![img5](https://user-images.githubusercontent.com/19779081/50811547-dc7e4280-1334-11e9-8419-8e045d8d0c90.PNG)

