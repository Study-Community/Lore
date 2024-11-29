from PyPDF2 import PdfMerger

def merge_pdfs(output_path, *input_paths):
    merger = PdfMerger()
    for path in input_paths:
        merger.append(path)
    merger.write(output_path)
    merger.close()
    print(f"PDFs merged into {output_path}")

if __name__ == "__main__":
    input_paths = input("Enter PDF paths (comma-separated): ").split(",")
    output_path = input("Enter output PDF path: ")
    merge_pdfs(output_path, *input_paths)