

def getCoeffs():
    with open("src/analysis/coeffs.txt") as f:
        lines = f.readlines()

    labels = list()
    coefficients = dict()
    while not '*' in lines[i]:
        labels.append(lines[i])
        i += 1
    i += 1

    while i < len(labels):
        temp = dict()
        j = 0
        var_name = lines[i]
        i += 1
        while not '*' in lines[i]:
            temp.update({labels[j] : float(lines[i])})
            i += 1
            j += 1
        coefficients.update({var_name : temp})
        i += 1
    
    return coefficients

    


    
