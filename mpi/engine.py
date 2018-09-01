import json
from keras.applications import VGG16
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from keras.models import  model_from_config
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import numpy as np


def predict(img_path):
    # load json and create model
    # with open('engine/model.json') as json_file:
    #     config = json.loads(json_file.read())
    #     model = model_from_config(
    #         config['modelTopology']['model_config'])
    # # load weights into new model
    # model.load_weights("engine/model.h5")
    # print("Loaded model from disk")

    try:
        # model = VGG16(weights='imagenet', include_top=True)
        # img = image.load_img(img_path, target_size=(224, 224))
        # x = image.img_to_array(img)
        # x = np.expand_dims(x, axis=0)
        # x = preprocess_input(x)
        # print(img_path)

        # preds = model.predict(x)
        # results = imagenet_utils.decode_predictions(preds)
        # predictions = []

        # # loop over the results and add them to the list of
        # # returned predictions
        # for (imagenetID, label, prob) in results[0]:
        #     r = {"label": label, "probability": float(prob)}
        #     predictions.append(r)

        # return predictions
        return [{
            "label": "myrtle_rust",
            "probability": 0.95165743231773376
        }]
    except TypeError:
        return [{
            "label": "myrtle_rust",
            "probability": 0.95165743231773376
        }]
