import random

class TestingModule:

    def __init__(self, classes, minimum_confidence):
        self.testable_symbols = classes
        self.minimum_confidence = minimum_confidence
        self.user_score_by_letter = { i : 0.0 for i in self.testable_symbols }
        self.show_symbol = False
        self.score_multiplier = 1.0

    def get_new_test_symbol(self):
        self.set_show_symbol(False)
        return self.testable_symbols[random.randint(0, len(self.testable_symbols) - 1)]

    def check_symbol(self, result, symbol_to_test):
        detected_symbols, coord = result
        n = len(detected_symbols)
        for i in range(n):
            if (self.testable_symbols[int(detected_symbols[i])] == symbol_to_test and coord[i][4].item() > self.minimum_confidence):
                print("detected %s with confidence: %.5f" % (symbol_to_test, float(coord[i][4].item())))
                self.set_score(symbol_to_test, self.get_score(symbol_to_test) + self.get_score_multiplier())
                print ("Your score for the letter %s is %.2f" % (symbol_to_test, self.get_score(symbol_to_test)))
                return True
    
    def get_score(self, symbol):
        return self.user_score_by_letter[symbol]
    
    def set_score(self, symbol, val):
        self.user_score_by_letter[symbol] = val

    def get_show_symbol(self):
        return self.show_symbol
    
    def set_show_symbol(self, val):
        self.show_symbol = val
        if val:
            self.set_score_multiplier(0.5)
        else:
            self.set_score_multiplier(1.0)

    def get_score_multiplier(self):
        return self.score_multiplier
    
    def set_score_multiplier(self, val):
        self.score_multiplier = val
