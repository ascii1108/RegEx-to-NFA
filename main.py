from char_type import charType
from expression_tree import createExpressionTree
from nfa_operations import arrangeNFA
from nfa_output import output_nfa, visualize_nfa
from regex_formatting import validateRegex, formatRegex
from regex_operations import computeRegEx

if __name__ == "__main__":
    print("Welcome to the Regular Expression Compiler!")
    print("These are the valid operations and their symbols:")
    print("Concatenation: .")
    print("Union: +")
    print("Kleene Star: *")
    print("Positive Closure: ^")
    print("Optional: ?")
    print("Grouping: ( and )")
    print("Range of characters: - (within [ and ])")
    print("Minimum and Maximum occurrences: {min,max} ")
    print("-------------------------------")

    while True:
        regex = input("Enter a regular expression (or 'q' to quit): ").strip()
        if regex.lower() == 'q':
            break
        try:
            if not validateRegex(regex):
                continue
            formattedRegEx = formatRegex(regex)
            RegExTree = createExpressionTree(formattedRegEx)
            FA = computeRegEx(RegExTree)
            nfa = arrangeNFA(FA)
            output_nfa(nfa)
            visualize_nfa(nfa)
        except ValueError as e:
            print(f"Error: {e}")
