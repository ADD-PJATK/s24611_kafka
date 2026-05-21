import argparse
import json
import os
import sys
import re

def main():
    parser = argparse.ArgumentParser(description="Local Data Anonymizer")
    parser.add_argument("--mapping", required=True, help="Path to mapping JSON file")
    parser.add_argument("--input", required=True, help="Path to input file")
    parser.add_argument("--output", required=True, help="Path to output file")
    parser.add_argument("--dry-run", action="store_true", help="Print replacements without writing output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    # Load mapping
    try:
        with open(args.mapping, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
    except Exception as e:
        sys.stderr.write(f"Error reading mapping file: {e}\n")
        sys.exit(1)

    # Validate mapping
    if "replacements" not in mapping:
        sys.stderr.write("Error: mapping file missing 'replacements' key.\n")
        sys.exit(1)

    options = mapping.get("options", {})
    case_sensitive = options.get("case_sensitive", False)

    for i, rule in enumerate(mapping["replacements"]):
        if "find" not in rule or "replace" not in rule:
            sys.stderr.write(f"Error: Rule {i} is missing 'find' or 'replace'.\n")
            sys.exit(1)
        if not isinstance(rule["find"], list) or len(rule["find"]) == 0:
            sys.stderr.write(f"Error: Rule {i} 'find' must be a non-empty array.\n")
            sys.exit(1)
        for f_str in rule["find"]:
            if not isinstance(f_str, str) or len(f_str) == 0:
                sys.stderr.write(f"Error: Rule {i} 'find' array contains empty or non-string values.\n")
                sys.exit(1)
        if not isinstance(rule["replace"], str):
            sys.stderr.write(f"Error: Rule {i} 'replace' must be a string.\n")
            sys.exit(1)

    # Read input
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        sys.stderr.write("Error: Input file is not valid UTF-8.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error reading input file: {e}\n")
        sys.exit(1)

    # Apply replacements
    # Policy: For each rule in order, for each find entry in order, replace all occurrences left-to-right.
    flags = 0 if case_sensitive else re.IGNORECASE
    
    total_replacements = 0
    stats = {}

    for rule in mapping["replacements"]:
        rep = rule["replace"]
        for find_str in rule["find"]:
            # Use regex to do the replacement, handling case sensitivity
            pattern = re.compile(re.escape(find_str), flags)
            content, count = pattern.subn(rep, content)
            
            if count > 0:
                stats[find_str] = stats.get(find_str, 0) + count
                total_replacements += count
                if args.verbose:
                    print(f"Replaced {count} occurrences of '{find_str}' with '{rep}'")

    if args.dry_run:
        print(f"Dry run complete. Total replacements: {total_replacements}")
        for k, v in stats.items():
            print(f" - '{k}': {v} replacements")
        sys.exit(0)

    # Write output
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        if args.verbose:
            print(f"Successfully wrote anonymized output to {args.output}")
        else:
            print(f"Anonymized file saved to {args.output}")
    except Exception as e:
        sys.stderr.write(f"Error writing output file: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
