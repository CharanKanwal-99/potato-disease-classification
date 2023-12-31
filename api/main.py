from fastapi import FastAPI,UploadFile
import uvicorn
import numpy as np
import tensorflow as tf
from io import BytesIO
from PIL import Image
import requests

MODEL = tf.keras.models.load_model("../models/1")

CLASS_NAMES = ['Early Blight','Late Blight','Healthy']
app = FastAPI()

endpoint = 'http://localhost:8501/v1/models/potatoes_model:predict'


def read_file_as_image(data):
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post('/prediction')
async def prediction(file:UploadFile= File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image,0)
    
    json_data = {'instances': img_batch.tolist()}

    response = requests.post(endpoint, json=json_data)
    prediction = np.array(response.json()['predictions'][0])

    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])

    return {
        'class': predicted_class,'confidence': float(confidence)
    }




if __name__ == "__main__":
    uvicorn.run(app, host='localhost',port=8000)
