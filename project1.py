# Participating students: 
# Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran

def division_algorithm(a: int, b: int):
    # Defining starting values of the u, v, and q variables
    # Probably a more elegant way to do this - maybe a list of u variables and a list of v variables?
    u1 = 1
    v1 = 0
    u2 = 0
    v2 = 1
    u3 = a
    v3 = b
    q = 0
    # We'll need to store the old values of the u variables to update the v variables
    old_u1 = 1
    old_u2 = 2
    old_u3 = 3

    # Print statements would be replaced by the file print outs in the final program
    print("For a =", a, " and b = ", b)
    while (v3 > 0):
        print(u1, v1, u2, v2, u3, v3, q)
        q = u3 // v3
        old_u1 = u1
        old_u2 = u2
        old_u3 = u3
        u1 = v1
        u2 = v2
        u3 = v3
        v1 = old_u1 - (q * v1)
        v2 = old_u2 - (q * v2)
        v3 = old_u3 - (q * v3)

    print(u1, v1, u2, v2, u3, v3, q)
    print("x = ", u1)
    print("y = ", u2)
    print("gcd = ", u3)
    print()

def main():
    division_algorithm(768336, 78192)
    division_algorithm(494752, 296864)
    division_algorithm(17601969, 2364768)

if __name__ == "__main__":
    main()