# Forensics File Analyzer

A command-line Python tool inspired by digital forensics workflows.
It scans a folder, extracts file metadata, flags suspicious files,
and exports a full report in CSV or JSON format.

---

## Features

- Recursively scans any folder and all its subfolders
- Extracts metadata: filename, extension, file type, size, and last modified time
- Flags suspicious files based on:
  - Known dangerous extensions (.exe, .bat, .dll, .sh)
  - Unknown file types
  - Empty files
  - Unusually small image files (possible extension mismatch)
- Color-coded terminal output (green = clean, red = flagged)
- Exports results as CSV and/or JSON reports with timestamps

---

## Project Structure
```
forensics-analyzer/
│
├── analyzer.py        # Core classes: FileRecord, ForensicsScanner, ReportGenerator
├── main.py            # Entry point — runs the program
├── reports/           # Output folder for generated reports
├── requirements.txt   # Project dependencies
└── README.md          # You are here
```

---

## How To Run

**1. Clone the repository:**

git clone https://github.com/xMostafaHusseinx/forensics-analyzer.git
cd forensics-analyzer

**2. Create and activate a virtual environment:**

python -m venv venv

venv\Scripts\Activate.ps1        # Windows

or

source venv/bin/activate          # Mac/Linux

**3. Install dependencies:**

pip install -r requirements.txt

**4. Run the program:**

python main.py

---

## Technologies Used

- Python 3
- colorama — terminal color output
- os, json, csv, datetime — Python standard library

## Skills Demonstrated

- Object-Oriented Programming (three cooperating classes)
- File system traversal and metadata extraction
- Data serialization (CSV and JSON)
- Defensive programming and input validation
- Clean project structure and documentation

## Author

Mostafa Aly Sayed Aly Hussein  