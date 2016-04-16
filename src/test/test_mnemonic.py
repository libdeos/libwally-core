import unittest
from util import *

class MnemonicTests(unittest.TestCase):

    words_list, wl = None, None

    def setUp(self):
        if self.wl is None:
            self.words_list, words = load_words('english')

            self.wl = wordlist_init(utf8(words))


    def test_mnemonic(self):

        LEN = 16
        PHRASES = LEN * 8 // 11 # 11 bits per phrase
        PHRASES_BYTES = (PHRASES * 11 + 7) // 8 # Bytes needed to store
        self.assertEqual(LEN, PHRASES_BYTES)

        buf = create_string_buffer(LEN)

        # Test round tripping
        for i in range(len(self.words_list) - PHRASES):
            phrase = utf8(' '.join(self.words_list[i : i + PHRASES]))

            written = c_ulong()
            ret = mnemonic_to_bytes(self.wl, phrase, buf, LEN, byref(written))
            self.assertEqual(ret, 0)
            self.assertEqual(written.value, PHRASES_BYTES)
            generated = mnemonic_from_bytes(self.wl, buf, LEN)
            self.assertEqual(phrase, generated)


if __name__ == '__main__':
    unittest.main()
