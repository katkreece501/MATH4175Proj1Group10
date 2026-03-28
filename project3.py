# python3 -m pip install tabulate
from tabulate import tabulate

# Participating students:
# Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran

# Constructs a Normalized Linear Approximation Table (NLAT) for a given S-box and bit length l. 
def construct_nlat(sbox, l):
    num_elements = 2**l
    midpoint = 2**(l - 1) # Normalization factor: 4 for l=3
    table = []

    for a in range(num_elements):
        row = []
        for b in range(num_elements):
            matches = 0
            for x in range(num_elements):
                # Calculate bitwise dot product parity for input and output 
                input_parity = bin(x & a).count('1') % 2
                output_parity = bin(sbox[x] & b).count('1') % 2
                
                if input_parity == output_parity:
                    matches += 1
            
            # Apply normalization: N_L(a, b) - 4 
            row.append(matches - midpoint)
        table.append(row)
    return table

def main():
    # S-Box definition: 
    # Input:  0, 1, 2, 3, 4, 5, 6, 7
    # Output: 6, 5, 1, 0, 3, 2, 7, 4
    sbox = {0: 6, 1: 5, 2: 1, 3: 0, 4: 3, 5: 2, 6: 7, 7: 4}
    
    # Set S-box bit length
    l = 3 
    
    # Create the Normalized Linear Approximation Table (NLAT)
    nlat_table = construct_nlat(sbox, l)
    
    # Format the table for output using tabulate
    headers = ["InputSums/OutputSums"] + [f"{i}" for i in range(2**l)]
    table_string = tabulate(nlat_table, headers=headers, showindex="always", tablefmt="grid")

    # Save the NLAT to the output file 
    with open("Project3.txt", "w") as f:
        f.write(f"Project 3: Cryptography MATH 4175\n")
        f.write(f"Participating Students:\n") 
        f.write(f"Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran\n\n") 
        f.write("Part 1: Normalized Linear Approximation Table (NL(a,b) - 4)\n") 
        f.write("Rows: Input Sums, Columns: Output Sums\n\n") 
        f.write(table_string)

if __name__ == "__main__":
    main()