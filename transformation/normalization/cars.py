def normalize_name(name):
    #remove extra spaces, convert to lowercase and remove special characters
    name = name.strip().lower()
    special_letters = {('à', 'â', 'ä', 'á', 'ã', 'å'):"a",
                       ('ç'):"c",
                       ('é', 'è', 'ê', 'ë'):"e",
                       ('î', 'ï', 'í', 'ì'):"i",
                       ('ô', 'ö', 'ò', 'ó', 'õ'):"o",
                       ('ù', 'û', 'ü', 'ú'):"u"}
    for c in name:
        for special_tuple in special_letters:
            if c in special_tuple:
                name = name.replace(c,special_letters[special_tuple])
        if ord(c)<97 or ord(c)>122:
            name = name.replace(c,'')
    return name
    #outputs are always consistent
    #example inputs : "Alfa-romeo", "Alfa Romeo ", " al#fa romeo", "Âlfä-ròmeõ"
    #example output : "alfaromeo"

