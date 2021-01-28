import numpy as np
from pathlib import Path
import tensorflow as tf

from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification



class Model:
    def __init__(self, model_path: str = None):
        self._model = None
        self._tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
        self._model_path = model_path
        self.load()

    def predict(self, X: str) -> float:
        encodings = self._tokenizer([X], truncation=True, max_length=200, padding=True)
        tfdataset = tf.data.Dataset.from_tensor_slices(dict(encodings))
        preds = self._model.predict(tfdataset.batch(1))
        preds = tf.keras.activations.softmax(tf.convert_to_tensor(list(preds.values()))).numpy()
        neg = preds[0][0][0]
        pos = preds[0][0][1]
        score = round(5 * pos/(neg+pos), 1)
        if score%1 != 0:
            if score%1 < 0.5:
                score = float(int(score))
            else:
                score = float(int(score + 1))
        return score

    def load(self):
        try:
            self._model = model_new = TFDistilBertForSequenceClassification.from_pretrained(self._model_path)
        except:
            self._model = None
            raise TypeError("The model cannot be loaded")
        return self


model_path = Path(__file__).parent / "text_classification_modelv3"
model = Model(model_path)


def get_model():
    return model


#if __name__ == "__main__":
#    X, y = load_boston(return_X_y=True)
#    model.train(X, y)
#    model.save()
