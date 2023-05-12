from textblob import TextBlob
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from textblob.en.sentiments import NaiveBayesAnalyzer


class Analyser:
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    def recognize_language(text):
        if 'а' in text or 'о' in text or 'у' in text or 'и' in text or 'е' in text or 'я' in text:
            return "ru"
        else:
            return "en"

    def get_tone(text):
        lang = Analyser.recognize_language(text)
        if lang == 'en':
            return Analyser.sentiment_en([text])
        else:
            return Analyser.sentiment_ru([text])

    def sentiment_en(text):
        blob_object = TextBlob(text, analyzer=NaiveBayesAnalyzer())
        result = blob_object.sentiment
        if abs(result.p_pos - result.p_neg) < 0.1:
            return "neu"
        else:
            return result.classification

    def sentiment_ru(text):
        result = Analyser.model.predict(text, k=2)[0]
        if "negative" in result and result["negative"] > 0.6:
            return "neg"
        elif "positive" in result and result["positive"] > 0.6:
            return "pos"
        else:
            return "neu"


