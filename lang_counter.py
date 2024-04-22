DATA = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    12: "Twelve",
    13: "Thirteen",
    14: "Fourteen",
    15: "Fifteen",
    16: "Sixteen",
    17: "Seventeen",
    18: "Eighteen",
    19: "Nineteen",
    20: "Twenty",
    30: "Thirty",
    40: "Forty",
    50: "Fifty",
    60: "Sixty",
    70: "Seventy",
    80: "Eighty",
    90: "Ninety",
    10**2: "Hundred",
    10**3: "Thousand",
    10**6: "Million",
    10**9: "Billion",
    10**12: "Trillion",
    10**15: "Quadrillion",
    10**18: "Quintillion",
    10**21: "Sextillion",
    10**24: "Septillion",
    10**27: "Octillion",
    10**30: "Nonillion",
    10**33: "Decillion",
    10**36: "Undecillion",
    10**39: "Duodecillion",
    10**42: "Tredecillion",
    10**45: "Quattuordecillion",
    10**48: "Quindecillion",
    10**51: "Sexdecillion",
    10**54: "Septendecillion",
    10**57: "Octodecillion",
    10**60: "Novemdecillion",
    10**63: "Vigintillion"
}

def construct_number(n: str):
    def find_closest_base(b: int):
        if DATA.get(b, False): return (b, 0)
        i = 0 #  to avoid infinite loops
        while i < len(DATA):
            if DATA.get(b, False):
                return (b, i)
            b = b // 10
            i += 1
    
    n = n.replace(',', '')
    n_float = None
    if len(n.split('.')) > 1:
        a, b, *_ = n.split('.')
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
    output = ""
    while i < len(bases):
        digit, base = bases[i]
        if digit == 0:
            i += 1; continue
        
        # >= 0_000_000
        if base >= 10**6:
            real_base, offset = find_closest_base(base)

            distance = base // real_base
            add_comma = i < non_zero_bases_count
            if distance == 100:
                middle = f" {DATA[10**offset]} " if offset < 2 else " "
                output += construct_number(n[i:i+3]) + middle + DATA[real_base]
                i += 3
            elif distance == 10:
                middle = f" {DATA[10**offset]} " if offset > 1 else " "
                output += construct_number(n[i:i+2]) + middle + DATA[real_base]
                i += 2
            else:
                middle = f" {DATA[10**offset]} " if offset > 0 else " "
                output += DATA[digit] + middle + DATA[real_base] 
                i += 1

            if add_comma:
                output += ", "
            continue;
        
        # 000_000
        if len(n) - i - 3 >= 3:
            output += construct_number(n[i:i+3]) + " Thousand, "
            i+=3; continue

        # 00_000
        if len(n) - i - 3 >= 2:
            sub = int(n[i:i+2])
            if DATA.get(sub, False):
                output += DATA[sub]
            else:
                output += DATA[digit * 10]    
                if bases[i + 1][0] != 0:
                    output += " " + DATA[bases[i + 1][0]]
            
            output += " Thousand, "
            i += 2; continue

        # 00
        if len(bases) - i == 2:
            sub = int(n[i: i + 2])
            if DATA.get(sub, False):
                output += DATA[sub] + " "
                break

            output += DATA[digit * base] + " "
            if(bases[i + 1][0] != 0):
                output += DATA[bases[i + 1][0]]
            break
        
        # 0
        else:
            if digit == 1 and base != 1: output += "One " + DATA[base] + " "
            else: 
                output += DATA[digit] + " "
                if base != 1: output += DATA[base] + " "

        i += 1

    if n_float:
        output += "point " + construct_number(n_float)
    return output

print(construct_number("562049874356201987563201478905632014785632014785632014785632014999"))