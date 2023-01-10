import main
import pytest


# Тест load_model
def test_load_model():
    pipe = main.load_model()
    assert pipe.tokenizer.name_or_path == 'Helsinki-NLP/opus-mt-en-ru', 'Helsinki-NLP/opus-mt-en-ru'
    assert pipe.tokenizer.vocab_size == 62518, '62518'
    assert pipe.tokenizer.model_max_length == 512, '512'

# Тест predict
def test_predict(a, b):
    for key in dict_test.keys():
        assert main.predict(key) == dict_test[key]


pipe = None
dict_test = {'Hello': 'Привет.'
    , 'I love you': 'Я люблю тебя.'
    , 'Hot summer nights': 'Горячие летние ночи'
    , 'The crazy days, city lights': 'Сумасшедшие дни, городские огни'
    , "I'll be back": 'Я вернусь.'
             }
