# Participating students: 
# Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran

def division_algorithm(a: int, b: int):
    # Defining starting values of the u, v, and q with lists
    u = [1, 0, a]
    v = [0, 1, b]
    q = 0
    # We'll need to store the old values of the u variables to update the v variables
    old_u = [1, 2, 3]

    # Print statements would be replaced by the file print outs in the final program
    print("For a =", a, " and b = ", b)
    while (v[2] > 0):
        print(u[0], v[0], u[1], v[1], u[2], v[2], q)
        q = u[2] // v[2]
        old_u[0] = u[0]
        old_u[1] = u[1]
        old_u[2] = u[2]
        u[0] = v[0]
        u[1] = v[1]
        u[2] = v[2]
        v[0] = old_u[0] - (q * v[0])
        v[1] = old_u[1] - (q * v[1])
        v[2] = old_u[2] - (q * v[2])

    print(u[0], v[0], u[1], v[1], u[2], v[2], q)
    print("x = ", u[0])
    print("y = ", u[1])
    print("gcd = ", u[2])
    print()

def main():
    division_algorithm(768336, 78192)
    division_algorithm(494752, 296864)
    division_algorithm(17601969, 2364768)

if __name__ == "__main__":
    main()