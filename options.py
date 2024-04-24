def load_english_options():
    return {
        "format_tens": lambda x: x.replace(" ", "-")
    }

def load_french_options():
    def format_tens(data, bases, x: str):
        tens, ones = bases
        if(ones[0] == 1):
            x = x.replace(" un", " et un")
        elif(ones[0] < 7 and (tens[0] == 9 or tens[0] == 7)):
            x = x.replace("-dix", "-" + data[10 + ones[0]]).split(" ")[0]

        return x
    
    def format_large(data, base_tup, x: str):
        digit, base = base_tup

        if digit > 1:
            x = x.replace(data[base], data[base] + "s")

        return x
    
    return {
        "format_tens": format_tens,
        "format_large": format_large
    }