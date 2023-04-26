import os
from pathlib import Path
from collections import namedtuple

# Anpassad datatyp för att lagra filinformation
#Adapted datatype for storing file information
FileInfo = namedtuple("FileInfo", ["path", "size"])

def get_size(path): #Gathers the size of the file and also locates the path for said file
    try:
        return sum(f.stat().st_size for f in path.glob("**/*") if f.is_file())
    except Exception as e:
        print(f"Error while processing: {path}, error: {e}")
        return 0

def get_files_in_directory(directory, files): #This functions retrieves the neccessary information about the file and the directory it is located in, error handling for permission issues is also included. Since some os files are "off-limits" unless you have root access
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

def format_size(size_bytes):            #Since it is standard to show files size in bytes, which makes it unreadable. This function makes sure to convert bytes to gigabytes
    size_gb = size_bytes / (1024 ** 3)
    return f"{size_gb:.2f} GB"


#This is the input function that gets exectuted once the script has done its search and sorted the files in the txt document that is generated, 
#in order to delete a file you have to for example write this in the input box: C:\Users\username\directory\directory\directory\directory\directory\file.mp4 48000.cfa
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
