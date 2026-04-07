import os
import json
import csv
from datetime import datetime
from colorama import Fore, Style, init

# This initializes colorama and resets the colored text automatically

init(autoreset=True)

# A dictionary of known file extensions and what type they are

KNOWN_EXTENSIONS = {
    ".txt": "Text", ".pdf": "Document", ".docx": "Document",
    ".jpg": "Image", ".jpeg": "Image", ".png": "Image",
    ".mp4": "Video", ".mov": "Video", ".avi": "Video",
    ".mp3": "Audio", ".wav": "Audio",
    ".py": "Script", ".js": "Script", ".bat": "Script", ".sh": "Script",
    ".exe": "Executable", ".dll": "Executable",
    ".zip": "Archive", ".rar": "Archive", ".7z": "Archive",
    ".csv": "Data", ".json": "Data", ".xml": "Data",
}

# Extensions that are considered suspicious

SUSPICIOUS_EXTENSIONS = {".exe", ".bat", ".sh", ".dll"}


class FileRecord:

    # Represents a single file found during the scan.

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.extension = os.path.splitext(filepath)[1].lower()
        self.file_type = KNOWN_EXTENSIONS.get(self.extension, "Unknown")
        self.flags = []
        self.unreadable = False

        # Case 3: File is locked or unreadable — catch permission errors gracefully

        try:
            self.size_bytes = os.path.getsize(filepath)
            self.modified_time = datetime.fromtimestamp(
                os.path.getmtime(filepath)
            ).strftime("%Y-%m-%d %H:%M:%S")
        except (PermissionError, OSError):
            self.size_bytes = -1
            self.modified_time = "Unreadable"
            self.unreadable = True
            self.flags.append("File unreadable or access denied")
            return

        self._analyze()

    def _analyze(self):

        # Runs checks on the file and populates self.flags with any suspicious findings.

        # Flag 1: Suspicious extension

        if self.extension in SUSPICIOUS_EXTENSIONS:
            self.flags.append("Suspicious extension")

        # Flag 2: Unknown file type

        if self.file_type == "Unknown":
            self.flags.append("Unknown file type")

        # Flag 3: Empty file

        if self.size_bytes == 0:
            self.flags.append("Empty file")

        # Flag 4: Mismatched extension

        if self.extension in {".jpg", ".jpeg", ".png"} and self.size_bytes < 1000:
            self.flags.append("Unusually small image — possible mismatch")

    def is_suspicious(self):
        return len(self.flags) > 0

    def to_dict(self):

        # Converts the file record to a dictionary for simplicity.

        return {
            "filename": self.filename,
            "filepath": self.filepath,
            "extension": self.extension,
            "file_type": self.file_type,
            "size_bytes": self.size_bytes,
            "modified_time": self.modified_time,
            "suspicious": self.is_suspicious(),
            "flags": ", ".join(self.flags) if self.flags else "None",
        }


class ForensicsScanner:

    # Scans a directory and builds a list of FileRecord objects.

    def __init__(self, target_folder):
        self.target_folder = target_folder
        self.records = []

    def scan(self):

        # Walks through every file in the target folder and scans it.

        print(f"\n{Fore.CYAN}Scanning: {self.target_folder}{Style.RESET_ALL}")
        print("-" * 50)

        if not os.path.exists(self.target_folder):
            print(f"{Fore.RED}Error: Folder not found.{Style.RESET_ALL}")
            return

        for root, dirs, files in os.walk(self.target_folder):
            for filename in files:
                filepath = os.path.join(root, filename)
                record = FileRecord(filepath)
                self.records.append(record)

                if record.unreadable:
                    print(
                        f"{Fore.YELLOW}[LOCKED]  {record.filename} "
                        f"— File unreadable or access denied{Style.RESET_ALL}"
                    )
                elif record.is_suspicious():
                    print(
                        f"{Fore.RED}[FLAGGED] {record.filename} "
                        f"— {', '.join(record.flags)}{Style.RESET_ALL}"
                    )
                else:
                    print(f"{Fore.GREEN}[CLEAN]   {record.filename}{Style.RESET_ALL}")

        print("-" * 50)
        print(f"Scan complete. {len(self.records)} file(s) found.")


class ReportGenerator:

    # Takes the scan results and writes them to a file. Supports both CSV and JSON formats.

    def __init__(self, records, output_folder="reports"):
        self.records = records
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def export_csv(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_folder, f"report_{timestamp}.csv")

        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.records[0].to_dict().keys())
            writer.writeheader()
            for record in self.records:
                writer.writerow(record.to_dict())

        print(f"\n{Fore.YELLOW}CSV report saved: {path}{Style.RESET_ALL}")

    def export_json(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_folder, f"report_{timestamp}.json")

        with open(path, "w") as f:
            json.dump([r.to_dict() for r in self.records], f, indent=4)

        print(f"{Fore.YELLOW}JSON report saved: {path}{Style.RESET_ALL}")