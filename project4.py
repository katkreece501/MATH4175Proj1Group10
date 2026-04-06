# python3 -m pip install tabulate
from tabulate import tabulate

# Participating students:
# Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran

# Constructs a Difference Distribution Table (DDT)
# Input: sbox - dictionary representing an S-box
# Input: l - int number of bits accepted by the S-box
# Output: DDT, represented as a list, with each element of the list being a row in the table
def construct_ddt(sbox: dict, l: int) -> list:
    table_size = 2**l # For l = 3, 2^3 = 8, so 8x8 table 
    table = []

    for x_prime in range(table_size):
        y_prime_freq = {i: 0 for i in range(table_size)}
        for x in range(table_size):
            x_star = x ^ x_prime
            y = sbox[x]
            y_star = sbox[x_star]
            y_prime = y ^ y_star
            y_prime_freq[y_prime] += 1
        table.append(list(y_prime_freq.values()))
    
    return table

def main():
    # S-Box definition:
    # Input:  0, 1, 2, 3, 4, 5, 6, 7
    # Output: 6, 5, 1, 0, 3, 2, 7, 4
    sbox = {0: 6, 1: 5, 2: 1, 3: 0, 4: 3, 5: 2, 6: 7, 7: 4}

    # Set S-box bit length
    l = 3

    # Construct Difference Distribution Table (DDT)
    ddt_table = construct_ddt(sbox, l)

    # Format the table for output using tabulate
    headers = ["Input Diff/ Output Diff"] + [f"{i}" for i in range(2**l)]
    table_string = tabulate(ddt_table, headers=headers, showindex="always", tablefmt="grid")

    # Write output to file
    with open("Project4.txt", "w") as f:
        f.write(f"Project 4: Cryptography MATH 4175\n")
        f.write(f"Participating Students:\n")
        f.write(f"Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran\n\n")
        f.write("Part 1: Difference Distribution Table (ND(a',b'))\n")
        f.write("Rows: Input Difference, Columns: Output Difference\n\n")
        f.write(table_string)

# Call main function
if __name__ == "__main__":
    main()