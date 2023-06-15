'''
This script walks through a complete diirectory and evaluates the integrity of a ll zip files it finds.
Useful for ensuring that zip files downloaded correctly when no checksum was available (e.g. from dropbox)
'''
import os
import sys
import zipfile
import concurrent.futures

class NoDirectoryProvidedError(Exception):
    pass

def test_zip_file(zip_file_path):
    try:
        with zipfile.ZipFile(zip_file_path) as zip_file:
            if zip_file.testzip() is not None:
                return False
            else:
                return True
    except zipfile.BadZipFile:
        return False

def process_directory(directory):
    failed_files = []
    passed_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                zip_file_path = os.path.join(root, file)
                result = test_zip_file(zip_file_path)
                if result:
                    passed_count += 1
                else:
                    failed_files.append(zip_file_path)
    return passed_count, failed_files

def main():
    if len(sys.argv) < 2:
        directory_path = os.getcwd()
        print("No directory path provided. Using current directory:", directory_path)
    else:
        directory_path = sys.argv[1]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.submit(process_directory, directory_path).result()

    passed_count, failed_files = results

    total_files = passed_count + len(failed_files)

    directory_name = os.path.basename(directory_path)
    output_file = f"zip_test_results_{directory_name}.txt"

    with open(output_file, 'w') as file:
        file.write(f"Total files processed: {total_files}\n")
        file.write(f"Passed files: {passed_count}\n")
        file.write(f"Failed files: {len(failed_files)}\n\n")
        file.write("List of failed files:\n")
        for failed_file in failed_files:
            file.write(f"{failed_file}\n")

    print(f"Zip test results saved to {output_file}.")

if __name__ == '__main__':
    main()

