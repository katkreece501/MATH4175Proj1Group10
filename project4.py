# python3 -m pip install tabulate
from tabulate import tabulate
from fractions import Fraction

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

# Filters 4-tuples to find "right" pairs for a given differential trail.
#
# Input: tuples - list of (x, x_star, y, y_star) as 6-bit integers
#        predicted_diff: the expected difference at the target bits
#        bit_mask: bitmask selecting which output bits the trail targets
# Output: list of right 4-tuples
def filter_right_tuples(tuples: list, predicted_diff: int, bit_mask: int) -> list:
    right = []
    for x, x_star, y, y_star in tuples:
        output_diff = y ^ y_star
        if (output_diff & bit_mask) == predicted_diff:
            right.append({
                "x":      format(x,      "06b"),
                "x_star": format(x_star, "06b"),
                "y":      format(y,      "06b"),
                "y_star": format(y_star, "06b"),
                "y^y*":   format(output_diff, "06b"),
            })
    return right

def format_tuple_table(right_list):
        rows = [[d["x"], d["x_star"], d["y"], d["y_star"], d["y^y*"]] for d in right_list]
        return tabulate(rows, headers=["x", "x*", "y", "y*", "y^y*"], tablefmt="grid")

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

    # Propagation Ratios for the three trails
    # Each ratio is the product of (DDT count / 8) for each active S-box in the trail

    # Trail Tr1 (P6 -> H6): S12(001->001), S22(001->001)
    R1 = (ddt_table[1][1] / 8) * (ddt_table[1][1] / 8)

    # Trail Tr2 (P6 -> H5,H6): S12(001->011), S21(001->001), S22(001->001)
    R2 = (ddt_table[1][3] / 8) * (ddt_table[1][1] / 8) * (ddt_table[1][1] / 8)

    # Trail Tr3 (P6 -> H4,H5,H6): S12(001->011), S21(001->011), S22(001->001)
    R3 = (ddt_table[1][3] / 8) * (ddt_table[1][3] / 8) * (ddt_table[1][1] / 8)

    # Append results to output file
    with open("Project4.txt", "a") as f:
        f.write("\n\nParts 2 & 3: Propagation Ratios\n\n")
        ratio_data = [
            ["Tr1 (P6 -> H6)", f"{Fraction(R1).limit_denominator()}", R1],
            ["Tr2 (P6 -> H5,H6)", f"{Fraction(R2).limit_denominator()}", R2],
            ["Tr3 (P6 -> H4,H5,H6)", f"{Fraction(R3).limit_denominator()}", R3],
        ]
        f.write(tabulate(ratio_data,
                         headers=["Trail", "Ratio (fraction)", "Ratio (decimal)"],
                         tablefmt="grid"))

    # 4-tuples (x, x*, y, y*) as 6-bit integers
    raw_tuples = [
        (0b100111, 0b100110, 0b100100, 0b111110),
        (0b000111, 0b000110, 0b110010, 0b110110),
        (0b001100, 0b001101, 0b111001, 0b100000),
        (0b011000, 0b011001, 0b011101, 0b011111),
        (0b001000, 0b001001, 0b001101, 0b000011),
        (0b011010, 0b011011, 0b101001, 0b101000),
    ]

    # Bit masks for the target output bits
    MASK_TR1 = 0b000001
    MASK_TR2 = 0b000011
    MASK_TR3 = 0b000111

    # Predicted output differences at the target bits from each trail's endpoint
    # Tr1: S22 output diff = 001 H6 bit = 1
    # Tr2: S22 output diff = 001 H5,H6 bits = 01
    # Tr3: S22 output diff = 001 H4,H5,H6 bits = 001
    PRED_TR1 = 0b000001
    PRED_TR2 = 0b000001
    PRED_TR3 = 0b000001

    right_tr1 = filter_right_tuples(raw_tuples, PRED_TR1, MASK_TR1)
    right_tr2 = filter_right_tuples(raw_tuples, PRED_TR2, MASK_TR2)
    right_tr3 = filter_right_tuples(raw_tuples, PRED_TR3, MASK_TR3)

    with open("Project4.txt", "a") as f:
        f.write("\n\nPart 4: Filtering for Right 4-Tuples\n\n")

        f.write("All 4-tuples with y^y* values:\n")
        all_rows = [
            [format(x,"06b"), format(xs,"06b"), format(y,"06b"), format(ys,"06b"), format(y^ys,"06b")]
            for x, xs, y, ys in raw_tuples
        ]
        f.write(tabulate(all_rows, headers=["x","x*","y","y*","y^y*"], tablefmt="grid"))

        f.write("\n\nRight 4-tuples for Tr1 (target: H6, mask=000001, predicted diff=000001):\n")
        f.write(format_tuple_table(right_tr1) if right_tr1 else "None found.\n")

        f.write("\n\nRight 4-tuples for Tr2 (target: H5,H6, mask=000011, predicted diff=000001):\n")
        f.write(format_tuple_table(right_tr2) if right_tr2 else "None found.\n")

        f.write("\n\nRight 4-tuples for Tr3 (target: H4,H5,H6, mask=000111, predicted diff=000001):\n")
        f.write(format_tuple_table(right_tr3) if right_tr3 else "None found.\n")

        # Pick the best single right 4-tuple for each trail
        selected = [
            ("Tr1", right_tr1[-1]),
            ("Tr2", right_tr2[-1]),
            ("Tr3", right_tr3[0]),
        ]
        f.write("\n\nSelected Right 4-Tuples (one per trail):\n")
        sel_rows = [[trail, d["x"], d["x_star"], d["y"], d["y_star"], d["y^y*"]]
                    for trail, d in selected]
        f.write(tabulate(sel_rows, headers=["Trail","x","x*","y","y*","y^y*"], tablefmt="grid"))

# Call main function
if __name__ == "__main__":
    main()