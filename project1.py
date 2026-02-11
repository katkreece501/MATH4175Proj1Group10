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
        
        for i in range(3):
            old_u[i] = u[i]
            u[i] = v[i]
            v[i] = old_u[i] - (q * v[i])

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