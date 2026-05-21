# Local Data Anonymizer

A simple, self-contained batch anonymization tool that runs locally to replace sensitive information in text files (including `.json`, `.txt`, `.md`, `.csv`) based on a mapping configuration file. It does not use any external APIs or cloud services.

## Prerequisites
- Python 3.6 or higher.
- No external Python dependencies required (uses only standard library).

## Installation
Clone or download the repository, and ensure you have Python installed. You can run the script directly.

## Usage
The anonymizer runs from the command line. Provide the mapping file, the input file to anonymize, and the output path where the anonymized file should be saved.

```bash
python anonymize.py --mapping <mapping_file> --input <input_file> --output <output_file>
```

**Optional arguments:**
- `--dry-run`: Prints out the replacements that would occur without writing any file.
- `-v`, `--verbose`: Prints detailed logs to the console for each replacement made.

### Examples

**1. JSON file (`.json`)**
```bash
python anonymize.py --mapping examples/mapping.json --input examples/data.json --output out/data.anon.json
```

**2. CSV file (`.csv`)**
```bash
python anonymize.py --mapping examples/mapping.json --input examples/users.csv --output out/users.anon.csv
```

**3. Text file (`.txt`)**
```bash
python anonymize.py --mapping examples/mapping.json --input examples/log.txt --output out/log.anon.txt
```

## Mapping Format
The tool expects a JSON file with the following format:

```json
{
  "replacements": [
    {
      "find": ["Anna Nowak", "A. Nowak"],
      "replace": "PERSON_A"
    },
    {
      "find": ["anna@firma.test"],
      "replace": "EMAIL_A"
    }
  ],
  "options": {
    "case_sensitive": false
  }
}
```

- **`replacements`**: An array of rules.
  - **`find`**: An array of strings that will be searched and replaced by the single token. It must contain at least one non-empty string.
  - **`replace`**: A single string token that acts as the substitute.
- **`options`**: (Optional) Global options.
  - **`case_sensitive`**: If `false` (default), replacements are case-insensitive. If `true`, replacements match the exact case.

## Edge-case Policy: Overlapping Matches & Execution Order
The policy for how substitutions are applied is as follows:
1. **Rule Order**: Rules are processed sequentially in the exact order they appear in the `replacements` array.
2. **Find Order**: Within each rule, the `find` entries are evaluated sequentially in the exact order they appear in the array.
3. **Scan Policy**: For each `find` string, the script scans the text left-to-right and replaces all occurrences with the `replace` token.

## Important Notes
- **No external APIs**: All data processing happens locally on your machine.
- **No HTTP calls**: No data is sent anywhere - everything stays in-memory.
- **No LLM/AI calls**: This is a deterministic string replacement tool, not ML-based.
