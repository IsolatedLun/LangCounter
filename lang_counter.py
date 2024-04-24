import json

from options import *

class LangCounter:
    def __init__(self, language: str, options: dict = {}):
        self.language = language
        self.options = options
        self.data = self.load_language_data()

        if options == {}:
            self.load_options()

    def load_language_data(self):
        with open(f"languages/{self.language}.json", "r", encoding='utf-8') as f:
            return {int(eval(k)): v.lower() for k,v in json.load(f).items()}
        
    def load_options(self):
        func_name = f"load_{self.language}_options"
        if func_name in globals():
            self.options = globals()[func_name]()

    def wordify(self, n: str):
        DATA = self.data
        output = ""
        
        n = n.replace(",", "")
        n_float = None
        if len(n.split(".")) > 1:
            a, b, *_ = n.split(".")
            n = a 
            n_float = b

        bases = []
        non_zero_bases_count = 0
        for i in range(0, len(n)):
            digit = int(n[i])
            if digit != 0: non_zero_bases_count += 1
            
            exponent = 10**(len(n) - i - 1)
            bases.append((digit, exponent))

        i = 0
        while i < len(bases):
            digit, base = bases[i]
            if digit == 0:
                i += 1; continue
            
            # >= 0_000_000
            if base >= 10**6:
                real_base, offset = self.find_closest_base(base)
                result = ""

                distance = base // real_base
                add_comma = i < non_zero_bases_count
                original_i = i
                if distance == 100:
                    middle = f" {DATA[10**offset]} " if offset < 2 else " "
                    result += self.wordify(n[i:i+3]) + middle + DATA[real_base]
                    i += 3
                elif distance == 10:
                    middle = f" {DATA[10**offset]} " if offset > 1 else " "
                    result += self.wordify(n[i:i+2]) + middle + DATA[real_base]
                    i += 2
                else:
                    middle = f" {DATA[10**offset]} " if offset > 0 else " "
                    result += DATA[digit] + middle + DATA[real_base] 
                    i += 1

                if self.options.get("format_large"):
                    result = self.options["format_large"](self.data, bases[original_i], result)
                output += result 
                if add_comma:
                    output += ", "

                continue;
            
            # 000_000
            if len(n) - i - 3 >= 3:
                output += self.wordify(n[i:i+3]) + f" {DATA[1000]}, "
                i += 3; continue

            # 00_000
            if len(n) - i - 3 >= 2:
                output += self.parse_ten_thousands(n, bases[i], bases[i + 1], i)
                i += 2; continue

            # 00
            if len(bases) - i == 2:
                output += self.parse_tens(n, bases[i], bases[i + 1], i)
                break
            
            # 0
            else: output += self.parse_ones(bases[i])
                

            i += 1

        if n_float is not None:
            output += "point " + self.wordify(n_float)
        return output
    
    def parse_ones(self, base_tup):
        temp = ""
        digit, base = base_tup

        if digit == 1 and base != 1: 
            temp += self.data[1] + " " + self.data[base] + " "
        else: 
            temp += self.data[digit] + " "
            if base != 1:
                temp += self.data[base] + " "

        return temp
    
    def parse_tens(self, n: str, base_tup, next_base_tup, i):
        temp = ""
        sub = int(n[i: i + 2])
        digit, base = base_tup
        if self.data.get(sub, False):
            temp += self.data[sub] + " "
        else:
            temp += self.data[digit * base] + " "
            if(next_base_tup[0] != 0):
                temp += self.data[next_base_tup[0]]

        if self.options.get("format_tens", False):
            temp = self.options["format_tens"](self.data, [base_tup, next_base_tup], temp)
        return temp
    
    def parse_ten_thousands(self, n: str, base_tup, next_base_tup, i):
        temp = ""
        sub = int(n[i:i+2])
        digit, _ = base_tup
        if self.data.get(sub, False):
            temp += self.data[sub]
        else:
            temp += self.data[digit * 10]    
            if next_base_tup[0] != 0:
                temp += " " + self.data[next_base_tup[0]]
        
        temp += f" {self.data[1000]}, "
        return temp
    
    def find_closest_base(self, b: int):
        if self.data.get(b, False): return (b, 0)
        i = 0 #  to avoid infinite loops
        while i < len(self.data):
            if self.data.get(b, False): return (b, i)
            b = b // 10
            i += 1

english_counter = LangCounter("french", {})
result = english_counter.wordify("124150478")
print(result)