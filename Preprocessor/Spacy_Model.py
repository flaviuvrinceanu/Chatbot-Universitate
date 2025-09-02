import spacy
from .utils.exceptions.Exceptions import UncertainPerceptionException

class Model:
    def __init__(self):
        self.nlp = spacy.load("Preprocessor/ner_intent_model")

    def get_intent(self, text):
        doc = self.nlp(text)
        best_intent = max(doc.cats, key=doc.cats.get)
        print(doc.cats[best_intent])
        if doc.cats[best_intent] > 0.75:
            return best_intent
        else:
            raise UncertainPerceptionException

if __name__ == "__main__":
    model = Model()

    t = "Unde mă pot autentifica în portalul studenților?"
    print(model.get_intent(t))