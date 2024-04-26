def load_english_options():
    def format_tens(data, bases, x: str):
        x = x.strip()
        # Ingores 11-19
        if bases[1][0] != 0:
            x = x.replace(" ", "-")
        return x
    
    return {
        "format_tens": format_tens
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
            base_str = x.split(" ")[-1]
            x = x.replace(base_str, base_str + "s")
        else:
            x = x.replace("un ", "")

        return x
    
    return {
        "format_tens": format_tens,
        "format_large": format_large
    }