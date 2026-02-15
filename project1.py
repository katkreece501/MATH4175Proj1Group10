#python3 -m pip install tabulate
from tabulate import tabulate

# Participating students:
# Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran

# Performs the division algorithm to find the greatest common divisor of a and b
# For best performance, a >= b should be true
def division_algorithm(a: int, b: int):
    # Defining starting values of the u, v, and q with lists
    u = [1, 0, a]
    v = [0, 1, b]
    q = 0
    # We'll need to store the old values of the u variables to update the v variables
    old_u = [1, 2, 3]
    # Used to build the table in the program before it's written to the output file
    table = []

    # Main algorithm loop. Runs until v3 <= 0.
    while (v[2] > 0):
        table.append([u[0], v[0], u[1], v[1], u[2], v[2], q])
        q = u[2] // v[2]
        
        for i in range(3):
            old_u[i] = u[i]
            u[i] = v[i]
            v[i] = old_u[i] - (q * v[i])
    # Adding the final row where v3 = 0
    table.append([u[0], v[0], u[1], v[1], u[2], v[2], q])

    #Open textfile and write table information to it
    with open("DivisionOutput.txt", "a") as textFile:
        textFile.write(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        textFile.write(f"For a = {a} and b = {b}\n\n")
        # The table itself being written
        textFile.write(
            tabulate(table, headers=["u1","v1","u2","v2","u3","v3","q"]))
        
        # Specifically naming x, y, and the gcd
        textFile.write(f"\n\nx = {u[0]}\n")

        textFile.write(f"y =  {u[1]}\n")

        textFile.write(f"gcd = {u[2]}\n")

def main():
    # Adding our names and project title
    with open("DivisionOutput.txt", "a") as textFile:
        textFile.write(f"Project 1: Cryptography MATH 4175\n")
        textFile.write(f"Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran\n")
    # Calling the division algorithm function on the pairs
    division_algorithm(768336, 78192)
    division_algorithm(494752, 296864)
    division_algorithm(17601969, 2364768)

# This calls the main function
if __name__ == "__main__":
    main()
