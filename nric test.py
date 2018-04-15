def nric_validate(nric):
    if not nric or nric == '':
        return False
    if len(nric) != 9:
        return False

    nric_numeric = list(nric)
    nric_numeric[0] = 0
    nric_numeric[1] = int(nric[1]) * 2
    nric_numeric[2] = int(nric[2]) * 7
    nric_numeric[3] = int(nric[3]) * 6
    nric_numeric[4] = int(nric[4]) * 5
    nric_numeric[5] = int(nric[5]) * 4
    nric_numeric[6] = int(nric[6]) * 3
    nric_numeric[7] = int(nric[7]) * 2
    nric_numeric[8] = 0

    weight = 0
    weight = sum(nric_numeric)

    offset = 0
    if nric[0] == "T" or nric[0] == "G":
        offset = 4
    else:
        offset = 0

    temp = (offset + weight) % 11

    st = ["J","Z","I","H","G","F","E","D","C","B","A"]
    fg = ["X","W","U","T","R","Q","P","N","M","L","K"]

    if nric[0] == "S" or nric[0] == "T":
        alpha = st[temp]
    elif nric[0] == "F" or nric[0] == "G":
        alpha = fg[temp]

    if nric[8] == alpha:
        return True
    else:
        return False


print(nric_validate('S9419812G'))

