import os
from pathlib import Path
from collections import namedtuple

# Anpassad datatyp för att lagra filinformation
FileInfo = namedtuple("FileInfo", ["path", "size"])

def get_size(path):
    try:
        return sum(f.stat().st_size for f in path.glob("**/*") if f.is_file())
    except Exception as e:
        print(f"Error while processing: {path}, error: {e}")
        return 0

def get_files_in_directory(directory, files):
    try:
        for item in directory.iterdir():
            if item.is_dir():
                get_files_in_directory(item, files)
            else:
                try:
                    files.append(FileInfo(item, item.stat().st_size))
                except Exception as e:
                    print(f"Error while processing: {item}, error: {e}")
    except PermissionError as pe:
        print(f"Permission denied for: {directory}, error: {pe}")

def format_size(size_bytes):
    size_gb = size_bytes / (1024 ** 3)
    return f"{size_gb:.2f} GB"

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted.")
    except Exception as e:
        print(f"Error while deleting {file_path}, error: {e}")

def main():
    root_path = Path.home()
    output_file = "disk_usage_report.txt"
    file_infos = []

    get_files_in_directory(root_path, file_infos)

    sorted_files = sorted(file_infos, key=lambda x: x.size, reverse=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Path, Size (in GB)\n")
        f.write("====================\n")
        for file_info in sorted_files:
            formatted_size = format_size(file_info.size)
            f.write(f"{file_info.path}, {formatted_size}\n")

    print(f"Disk usage report saved to {output_file}")

    while True:
        delete_choice = input("Enter the file path you want to delete or type 'exit' to quit: ").strip()
        if delete_choice.lower() == "exit":
            break
        if Path(delete_choice).exists():
            delete_file(delete_choice)
        else:
            print(f"File not found: {delete_choice}")

if __name__ == "__main__":
    main()
