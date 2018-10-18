class PhoneConverter1:
    rules_1 = [
        "aàáảãạ",
        "ăằắẳẵặ",
        "âầấẩẫậ",
        "eèéẻẽẹ",
        "êềếểễệ",
        "iìíỉĩị",
        "oòóỏõọ",
        "ôồốổỗộ",
        "ơờớởỡợ",
        "uùúủũụ",
        "ưừứửữự",
        "yỳýỷỹỵ"
    ]
    rules_2 = [
        "awă",
        "aaâ",
        "eeê",
        "ooô",
        "owơ",
        "uwư",
        "ddđ"
    ]
    w2p = {}
    p2w = {}
    for words in rules_1:
        original = words[0]
        words = words[1:]
        for rule in rules_2:
            if original == rule[2]:
                original = rule[0:2]
        tones = "fsrxj"
        for i, w in enumerate(words):
            w2p[w] = original + tones[i]
    for rule in rules_2:
        w2p[rule[2]] = rule[0:2]
    for key, value in w2p.items():
        p2w[value] = key

    @staticmethod
    def word2phone(word):
        w2p = PhoneConverter1.w2p
        phone = ""
        for w in word:
            if w in w2p:
                phone += w2p[w]
            else:
                phone += w
        return phone

    @staticmethod
    def phone2word(phone):
        p2w = PhoneConverter1.p2w
        i = 0
        word = ""
        while i < len(phone):
            if phone[i:i+3] in p2w:
                p = phone[i:i+3]
                word += p2w[p]
                i += 3
            elif phone[i:i+2] in p2w:
                p = phone[i:i+2]
                word += p2w[p]
                i += 2
            else:
                p = phone[i:i+1]
                word += p
                i += 1
        return word

if __name__ == '__main__':
    tests = [
        ("con hoẵng", "con hoawxng"),
        ("lựu đạn", "luwju ddajn"),
        ("kiểm tra", "kieerm tra"),
        ("ủy ban", "ury ban"),
        ("cà phê", "caf phee"),
        ("khách sạn", "khasch sajn"),
        ("đúng", "ddusng"),
        ("xã hội", "xax hooji")
    ]
    for test in tests:
        assert (test[0] == PhoneConverter1.phone2word(test[1]))
        assert (test[1] == PhoneConverter1.word2phone(test[0]))
