from good import load_model, predict
import pytest


# Тест load_model
def test_load_model():
    pipe = load_model()
    assert load_model().tokenizer.name_or_path == 'Helsinki-NLP/opus-mt-en-ru', 'Helsinki-NLP/opus-mt-en-ru'
    assert load_model().tokenizer.vocab_size == 62518, '62518'
    assert load_model().tokenizer.model_max_length == 512, '512'

# Тест predict
def test_predict():
    for key in dict_test.keys():
        assert predict(key) == dict_test[key]


dict_test = {'Hello': 'Здравствуйте.'
    , 'I love you': 'Я люблю тебя'
    , 'Hot summer nights': 'Горячие летние ночи'
    , 'The crazy days, city lights': 'Сумасшедшие дни, городские огни'
    , "I'll be back": 'Я вернусь.'
             }
