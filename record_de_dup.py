import os
import sys
import glob


def delete_mkv_files(directory):
    pattern = os.path.join(directory, "**", "*.mkv")
    mkv_files = glob.glob(pattern, recursive=True)

    if not mkv_files:
        print(f"No .mkv files found in: {directory}")
        return

    for f in mkv_files:
        os.remove(f)
        print(f"Deleted: {f}")

    print(f"\nDone. Deleted {len(mkv_files)} .mkv file(s).")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.path.join(os.path.expanduser("~"), "Videos")

    if not os.path.isdir(target_dir):
        print(f"Directory not found: {target_dir}")
        sys.exit(1)

    delete_mkv_files(target_dir)
