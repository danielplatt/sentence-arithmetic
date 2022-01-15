from sentence_manipulation.passive_to_active import passive_to_active


def test_passive_to_active():
    sent = 'The car was chased by the dog.'
    assert passive_to_active(sent) == 'the dog chased The car . '


if __name__ == '__main__':
    test_passive_to_active()
