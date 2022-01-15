from sentence_manipulation.passive_to_active import passive_to_active


def test_passive_to_active():
    sent = 'The car was chased by the dog.'
    assert passive_to_active(sent) == 'the dog chased The car . '

    sent = 'It was formed, in fact, by the Articles of Association in 1774.'
    assert passive_to_active(sent) == 'the Articles of Association formed , in fact , It in 1774 . '


if __name__ == '__main__':
    test_passive_to_active()
