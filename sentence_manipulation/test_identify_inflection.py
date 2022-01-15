import spacy

from sentence_manipulation.detect_inflection import detect_inflection, isolate_auxiliaries


def test_detect_inflection():
    nlp = spacy.load("en_core_web_sm")
    sentences = [
        'The car is chased by the dog.', 'The car gets chased by the dog.', 'The food gets brought by me.',
        'The cars are chased by the dog.', 'The cars get chased by the dog.', 'The car was chased by the dog.',
        'The cars were chased by the dog.', 'The car got chased by the dog.',
        'The car is being chased by the dog.', 'The car is getting chased by the dog.',
        'The cars are being chased by the dog.', 'The cars are getting chased by the dog.',
        'The car was being chased by the dog.', 'The car was getting chased by the dog.',
        'The cars were being chased by the dog.', 'The cars were getting chased by the dog.',
        'The car has been chased by the dog.', 'The car has got chased by the dog.',
        'The cars have been chased by the dog.', 'The cars have got chased by the dog.',
        'The car had been chased by the dog.', 'The car had got chased by the dog.',
        'The cars had been chased by the dog.', 'The cars had got chased by the dog.',
        'The car will be chased by the dog.', 'The car will get chased by the dog.',
        'The cars will be chased by the dog.', 'The cars will get chased by the dog.',
        'The car will have been chased by the dog.', 'The car will have got chased by the dog.',
        'The cars will have been chased by the dog.', 'The cars will have got chased by the dog.',
        'The car should be chased by the dog.', 'The car should get chased by the dog.',
        'The car should have been chased by the dog.', 'The car should have got chased by the dog.'
                 ]
    inflections = [
        ('simple present', '3rd person singular'),
        ('simple present', '3rd person singular'),
        ('simple present', '3rd person singular'),
        ('simple present', 'non-3rd person singular'),
        ('simple present', 'non-3rd person singular'),
        ('simple past', '1st or 3rd person singular'),
        ('simple past', 'not 3rd person singular (could be 1st)'),
        ('simple past', 'unknown'),
        ('present progressive', '3rd person singular'),
        ('present progressive', '3rd person singular'),
        ('present progressive', 'non-3rd person singular'),
        ('present progressive', 'non-3rd person singular'),
        ('past progressive', '1st or 3rd person singular'),
        ('past progressive', '1st or 3rd person singular'),
        ('past progressive', 'not 3rd person singular (could be 1st)'),
        ('past progressive', 'not 3rd person singular (could be 1st)'),
        ('present perfect', '3rd person singular'),
        ('present perfect', '3rd person singular'),
        ('present perfect', 'non-3rd person singular'),
        ('present perfect', 'non-3rd person singular'),
        ('past perfect', 'unknown'),
        ('past perfect', 'unknown'),
        ('past perfect', 'unknown'),
        ('past perfect', 'unknown'),
        ('simple future', 'unknown'),
        ('simple future', 'unknown'),
        ('simple future', 'unknown'),
        ('simple future', 'unknown'),
        ('future perfect', 'unknown'),
        ('future perfect', 'unknown'),
        ('future perfect', 'unknown'),
        ('future perfect', 'unknown'),
        ('aux: should plus be', 'unknown'),
        ('aux: should plus be', 'unknown'),
        ('aux: should plus have been', 'unknown'),
        ('aux: should plus have been', 'unknown')
        ]
    for sent, inf in zip(sentences, inflections):
        assert detect_inflection(isolate_auxiliaries(nlp(sent))) == inf


if __name__ == '__main__':
    test_detect_inflection()
