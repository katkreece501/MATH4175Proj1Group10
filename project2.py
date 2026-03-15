#python3 -m pip install wordsegment
from collections import deque
from wordsegment import load, segment

# Participating students:
# Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran

# Splits a given string into m substrings, with the first letter being in the first substring, 2nd letter in second substring, etc.
# Note substrings may not all be the same length
# Returns substrings as a Python dictionary, with the key being an integer 1 to m inclusive, and the corresponding value
# being the substrings
def substring(string: str, m: int):
    # Create the dictionary of substrings
    substrings = {i: "" for i in range(1, m+1)}
    # Substring we're looking at 
    stringNum = 1
    # Iterate through the string, and add each character to the right substring
    for char in string:
        substrings[stringNum] += char
        # Increment stringNum, keeping it between 1 and m inclusive
        stringNum = stringNum + 1
        if stringNum == m + 1:
            stringNum = 1
    return substrings

# Records the raw frequencies of characters in a string
# Not case sensitive, ie 'a' and 'A' will have different frequencies
# Returns a dictionary with characters in the string as key, and the frequencies being the corresponding values
def frequencyCounter(string: str):
    # To store frequencies
    letter_dict = {}
    # Iterate through the string and count characters
    for char in string:
        if char in letter_dict:
            letter_dict[char] += 1
        else:
            letter_dict[char] = 1
    return letter_dict

# Calculates the indices of coincidence for a dictionary of substrings
# Returns a list iOC, where iOC[i] holds the index of coincidence for substring i + 1
def indexOfCoincidence(substrings: dict, m: int):
    # List to hold the indices
    iOC = [0 for _ in range (0, m)]
    # Track what substring we're on
    i = 0
    # Iterate through substrings
    for substring in substrings.values():
        sumFreq = 0
        letters = frequencyCounter(substring)
        # Sum up the letter frequency times the letter frequency - 1 for all the letters in the substring
        for freq in letters.values():
            sumFreq += freq * (freq - 1)
        n = len(substring)
        # Compute index of coincidence and store it
        iOC[i] = sumFreq / (n * (n - 1))
        i += 1
    return iOC

# Outputs substrings and corresponding indices of coincidence to the output file
def outputSubstringsIOC(substrings: dict, iOC: list, m: int):
    with open("VigenereDecryption.txt", "a") as textFile:
        textFile.write(f"For m = {m}:\n")
        # Iterate through each substring
        for num, substr in substrings.items():
            # Properly format output
            textFile.write(f"Substring y{num} =\n")
            textFile.write(f"{substr}\n")
            textFile.write(f"Index of Coincidence for y{num}: {iOC[num - 1]}\n\n")
        textFile.write(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

# Converts a substring into a frequency vector
def frequencyVector(string : str):
    # Count occurrences of each letter
    counts = [0] * 26

    for char in string:
        # Convert letter to number 0-25
        index = ord(char) - ord('A')   
        counts[index] += 1

    lengthOfSubstring = len(string)

    # Convert counts into probabilities
    freqVector = []
    for count in counts:
        freqVector.append(count / lengthOfSubstring)

    return freqVector

#shift frequency vector by n amount
def shiftFrequencyVector(freqVector : list, shiftAmount : int):
    freqVectorDeque = deque(freqVector)
    freqVectorDeque.rotate(-shiftAmount)
    return list(freqVectorDeque)

# Computing the dot products for the 26 vectors 
# Tracks which shift produces the highest dot product, which will correspond to a character in the key word
def computeDotProducts(freqVector: list):
    englishFreq = [
        0.082, 0.015, 0.028, 0.043, 0.127, 0.022,
        0.020, 0.061, 0.070, 0.002, 0.008, 0.040,
        0.024, 0.067, 0.075, 0.019, 0.001, 0.060,
        0.063, 0.091, 0.028, 0.010, 0.023, 0.001,
        0.020, 0.001
    ]

    #compute all dot products and store here 
    dotProducts = []

    # To track which shift produces the highest dot product
    highestShift = -1
    highestDot = -1
    for shift in range(26):
        freqVectorShifted = shiftFrequencyVector(freqVector, shift)

        # Compute dot product
        dot = 0
        for j in range(len(englishFreq)):
            dot += freqVectorShifted[j] * englishFreq[j]

        # Update highestDot/highestShift if needed
        if dot > highestDot:
            highestDot = dot
            highestShift = shift

        # Multiply by 100 to make it look cleaner
        dotProducts.append(dot * 100)

    return dotProducts, highestShift

# Computes the dot products for all 7 substrings, along with the keyword
def computeDotProductTableKeyword(substrings: dict):

    table = {}
    keyword = ""
    numToLetter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
                   13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

    # Iterate over each substring
    for num, substr in substrings.items():
        # Convert substring to frequency vector
        freqVec = frequencyVector(substr)
        # Compute dot products for all 26  shifts
        dots, charNum = computeDotProducts(freqVec)
        # Store in table under substring number
        table[num] = dots
        # Get the corresponding character to the highest shift for the keyword
        keyword += numToLetter[charNum]

    return table, keyword

# Outputs the dot product table to the text file
def outputDotProductTable(table: dict):
   
    with open("VigenereDecryption.txt", "a") as textFile:
        textFile.write("Dot Product Table (rows = shifts 0-25)\n\n")

        # Iterate through each shift
        for shift in range(26):
            row = []
            # Collect dot products for this shift from all 7 substrings
            for col in range(1, 8):
                # Format each dot product to 3 decimal places
                row.append(f"{table[col][shift]:.3f}")

            # Write the row to file
            textFile.write(f"{shift:2}: " + "  ".join(row) + "\n")

        textFile.write("\n")
   
# Decrypts a given ciphertext using the Vigenère cipher decryption formula and a given keyword
def decryptVigenere(ciphertext: str, keyword: str):
    decryptedText = ""
    keywordLength = len(keyword)

    for i, char in enumerate(ciphertext):
        # Convert character and corresponding keyword character to numbers 0-25
        charIndex = ord(char) - ord('A')
        keyIndex = ord(keyword[i % keywordLength]) - ord('A')

        # Decrypt character using Vigenère decryption formula
        decryptedCharIndex = (charIndex - keyIndex) % 26
        decryptedChar = chr(decryptedCharIndex + ord('A'))

        decryptedText += decryptedChar

    return decryptedText

# Takes the raw decrypted text and formats it with spaces from the wordsegment library
def formatWithSpaces(rawText):
    load()
    words = segment(rawText)
    result = " ".join(words).capitalize()
    return result
    
def main():
    # Open file, and add names
    with open("VigenereDecryption.txt", "w") as textFile:
        textFile.write(f"Project 2: Cryptography MATH 4175\n")
        textFile.write(f"Trisha Bajpai, Tommy Dalessio, Kathleen Reece, Theo Tran\n\n")

    # The ciphertext to be decrypted
    ciphertext = (
        "LDMUPTDJPUVYXRXFCJEMFWDIJMIHFWVUHMODWTNLCVTAKFXQLLPMUESSJKBVNXLFCBYPPL"
        "TAZKJEQVOMTFVLLUWWELRKAEYZQZWOMIGILFNMTPRWEKVKSWKGSMMPVZWDIMPSQSJMNDGD"
        "DAAVPRPSEVJEVHSIXIZHXUPARYHVWNDZNIVVAAZRRHVEVRHEBLDIKRMYWOCJPVVKKTVNSQ"
        "LNWCZZHJWKTPWVLKBYPMUVWBRLWDJAALWXOSSMEQSUUAUVYXLKOWDPXLEAALYEEDABFCIF"
        "GRMIELHUKVKPRWGBMCPGWJKVZNGREICETGDLEWEDJUGIBYPXHUDVFWSJQLZFGMGWNMMPRL"
        "FNMJASQKABFLGRMNBFCHHJKZUFPBSQBYZVLRALNLVUSJBZDWXWZJPLJHVAZRWNXVCMWZVH"
        "PWUGWIPSJGTZQPMJQTLXLGJAJPVYAYMJYSZWJKIJTWUAZKLMQUKUDFRLUWBZZRVTULVQEX"
        "DPEZELWZASVJRHUAAJLVBLKLVNVBHPBYPGREICETGDLEWEDWRDATPTRWZAPRYHVGBBYPIQ"
        "VQAVCXKAOIGAPLWOJFELZZAVKSIGSPIZDMQEKBZZRRNAZVWIFLNWETGQWPEFCOVGNIKCIV"
        "LKVRYIOWYBIZRLUZMMTGHABBYPGREICETGDLEWEDTUGRQUPVLKOMIGIGOEBYLADJNIEEWH"
        "WGQERXKGOMTZQPMJQTLXLGJAKSISJKDZOIUUWVEZXSJKDZOIWZALREEEWYILDILLDIJOIV"
        "ACVVOXKWPMTSRRDKOPDYFZPPREMWUWVEZXEWWKTPWVWZJPLRBLDQIOTDJPGNPHRFKBYLZH"
        "SJGJTPYWNJLWPHLOIEOXKWZQJNYVKEWEDALLDQEELHWTMTFXLNAJILRFZWZVDXLDHWERSL"
        "FCEYTPHLDMIPLDKJWKJIWTAMELHHUEAZZRZZABYPVWGOMVVPHYEACLXLGJEVXYVLSWIVAL"
        "LDKFYKUWOAZYHXKPZPLGDVAUZNWSJEDRNCJJKCGDEQVKBYPVVLKKILJWSJIGAVRSYPKSEW"
        "SZLIPWVWOICWSILDMDFPWALTVNSPHABZYKFGJKVCRVLDIKSEYWXMVYXKWBWTFWRXOWDFGK"
        "VAJREIEMPEVNEQSHTRRVHWPPREAHOETCYIHVKVXZMQYDWEPWWSJLZYJRJIMUAYEDEKUPFD"
        "LAISZYWZKESPWWLKXIZXHUPTZMIULUIEOWHUQZZECLFXWKSSXJHINDEQVKCIEIFZJWCZKB"
    )

    # For m = 6, 7, 8, split ciphertext into m substrings and compute index of coincidence for each
    # This will verify that m = 7 is the correct guess for the keyword
    substrings6 = substring(ciphertext, 6)
    substrings7 = substring(ciphertext, 7)
    substrings8 = substring(ciphertext, 8)
    iOC6 = indexOfCoincidence(substrings6, 6)
    iOC7 = indexOfCoincidence(substrings7, 7)
    iOC8 = indexOfCoincidence(substrings8, 8)
    outputSubstringsIOC(substrings6, iOC6, 6)
    outputSubstringsIOC(substrings7, iOC7, 7)
    outputSubstringsIOC(substrings8, iOC8, 8)

    # Explanation for why m = 7 is the correct guess
    explanation = (
        "Our outputs verify that m = 7 is the correct guess for the length of the keyword. For m = 6 and m = 8, "
        "the indices of coincidence for each substring are all somewhat close to 0.038, which is the expected "
        "index of coincidence for a completely random substring. By contrast, for m = 7, all the substrings have "
        "indices of coincidence that are close to or exceeding 0.065, which would be the index of coincidence for a "
        "substring with letter frequencies approaching those of the English language as a whole. Thus, this indicates "
        "that each of the substrings for m = 7 is likely to be a ciphertext encrypted with the same key, which would be "
        "expected for a ciphertext encrypted with the Vigenère cipher with a keyword of length 7."
    )

    # Write explanation to the file
    with open("VigenereDecryption.txt", "a") as textFile:
        textFile.write(f"{explanation}\n\n")

    dotTable, keyword = computeDotProductTableKeyword(substrings7)
    outputDotProductTable(dotTable)

    # Keyword gotten from columns
    decryptedText = decryptVigenere(ciphertext, keyword)
    with open("VigenereDecryption.txt", "a") as textFile:
        textFile.write(f"From the table, the keyword is {keyword}\n\n")
        textFile.write(f"Decrypted Text:\n{decryptedText}\n\n")
    
    # Write final decryption to the file formatted with spaces and punctuation
    # 1. Add spaces to the decryption
    formattedDecryption = formatWithSpaces(decryptedText)
    
    # 2. Add punctuation to the decryption
    replacements = [
        ("whom we serve in recent months", "whom we serve. In recent months,"),
        ("however we have", "however, we have"),
        ("to their data as a result", "to their data. As a result,"),
        ("issued by a federal judge for example", "issued by a federal judge. For example,"),
        ("end user this applies", "end user. This applies"),
        ("an electronic device if the", "an electronic device. If the"),
        ("any third party we do not have any silver bullets and", "any third party. We do not have any silver bullets, and"),
        ("are still ongoing while", "are still ongoing. While"),
        ("seek legislation we must", "seek legislation, we must"),
        ("congress industry academics privacy groups and others", "Congress, industry, academics, privacy groups, and others"),
        ("so much debate but", "so much debate. But"),
        ("ongoing honest and informed", "ongoing, honest, and informed"),
    ]

    for old, new in replacements:
        formattedDecryption = formattedDecryption.replace(old, new)

    if not formattedDecryption.endswith("."):
        formattedDecryption += "."

    with open("VigenereDecryption.txt", "a") as textFile:
        textFile.write(f"Decrypted Text Formatted with Spaces and Punctuation:\n{formattedDecryption}\n")
    
if __name__ == "__main__":
    main()