def normalize_name(name):
    #remove extra spaces, convert to lowercase and remove special characters
    name = name.strip().lower()
    for c in name:
        if ord(c)<97 or ord(c)>122:
            name = name.replace(c,'')
    return name
    #outputs are always consistent
    #example inputs : "Alfa-romeo", "Alfa Romeo ", " al#fa romeo"
    #example output : "alfaromeo"
