import sys
import os
from analyzer import ForensicsScanner, ReportGenerator


# Main function that runs the forensics analyzer

def main():
    print("=" * 50)
    print("       Forensics File Analyzer")
    print("=" * 50)

    # Get the folder path from the user

    folder = input("\nEnter the folder path to scan: ").strip()

    # Case 1: User typed nothing and just hit enter

    if not folder:
        print("\nNo path entered. Exiting.")
        return

    # Case 2: User typed a file path instead of a folder path

    if os.path.isfile(folder):
        print(f"\nError: '{folder}' is a file, not a folder. Please enter a folder path.")
        return

    # Create the scanner and run it

    scanner = ForensicsScanner(folder)
    scanner.scan()

    # If no files were found, exit early

    if not scanner.records:
        print("\nNo files found. Exiting.")
        return

    # Ask the user what report format they want

    print("\nExport report as:")
    print("  [1] CSV")
    print("  [2] JSON")
    print("  [3] Both")

    choice = input("\nEnter choice (1/2/3): ").strip()

    # Generate the report based on the user's choice

    reporter = ReportGenerator(scanner.records)

    if choice == "1":
        reporter.export_csv()
    elif choice == "2":
        reporter.export_json()
    elif choice == "3":
        reporter.export_csv()
        reporter.export_json()
    else:
        print("Invalid choice. No report generated.")

    print("\nDone. Thank you for using Forensics File Analyzer.")


# Only run main() if this file is executed directly

if __name__ == "__main__":
    main()