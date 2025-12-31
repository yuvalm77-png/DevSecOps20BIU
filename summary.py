import os

SKIP_DIRS = {"__pycache__", ".venv", "tests"}

def merge_all_py_files_recursively(root_dir: str, output_file: str) -> None:
    output_abs = os.path.abspath(output_file)

    with open(output_file, "w", encoding="utf-8") as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # הסרה inplace של תיקיות שלא רוצים להיכנס אליהן
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

            for filename in filenames:
                if not filename.endswith(".py"):
                    continue

                file_path = os.path.join(dirpath, filename)
                file_abs = os.path.abspath(file_path)

                # לא לכלול את קובץ הפלט עצמו
                if file_abs == output_abs:
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                except Exception as e:
                    print(f"שגיאה בקריאת הקובץ {file_path}: {e}")
                    continue

                rel_path = os.path.relpath(file_path, root_dir)
                outfile.write(f"\n--- התחלה של {rel_path} ---\n")
                outfile.write(content)
                outfile.write(f"\n--- סוף של {rel_path} ---\n\n")

if __name__ == "__main__":
    output_filename = "merged_all_py_files.txt"
    merge_all_py_files_recursively(root_dir=".", output_file=output_filename)
    print(f"הקובץ המאוחד נוצר בהצלחה בשם: {output_filename}")
