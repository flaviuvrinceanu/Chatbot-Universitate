from .Filter_class import Filter
from .Normalizer_class import Normalizer
from .Tokenizer_class import Tokenizer
from .Translator_class import Translator
from .Spacy_Model import Model
from .utils.exceptions.Exceptions import BannedWordException, UncertainPerceptionException

class Preprocessor:
    def __init__(self):
        self.normalizer = Normalizer()
        self.filter = Filter()
        self.tokenizer = Tokenizer()
        self.translator = Translator()
        self.model = Model()

    def begin_pipeline(self, text):

        ### Part I: Normalization
        # lowercasing + removing additional white spaces
        normalized_text = self.normalizer.normalize(text)

        ### Part II: Tokenization
        # Using NLP we will try to tokenize all words from a text

        token_list = self.tokenizer.tokenize(normalized_text)

        ### Part III: Filtering
        # Texts with banned words will not be forwarded
        # and a message be shown

        try:
            self.filter.filter(normalized_text)
        except BannedWordException:
            return "none"

        ### Part IV: Model Use & Translating Message
        # We will try pipelining our text through the model

        try:
            intent = self.model.get_intent(normalized_text)
            final_input = self.translator.intent_to_request(intent)

        except UncertainPerceptionException:
            final_input = text

        ### PART V: returning the final input

        return final_input

if __name__ == "__main__":
    p = Preprocessor()
    text = "Cati ani de adrese am?"
    print(p.begin_pipeline(text))
