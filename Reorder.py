import re
from pypdf import PdfReader, PdfWriter

def get_sort_key(text):
    """
    Finds the Roll No in the text and returns a tuple (rank, roll_no) 
    to sort by series first, then by number.
    """
    # Regex to find a Roll No like 25CG012, 24C0123, etc.
    match = re.search(r'\b(2[345][A-Z0-9]+)\b', text)
    if not match:
        return (99, "") # Put pages without IDs at the end
    
    roll = match.group(1).upper()
    
    # Assign priority ranks based on your requirement
    if roll.startswith("25CG"): rank = 1
    elif roll.startswith("25CAI"): rank = 2
    elif roll.startswith("25CDS"): rank = 3
    elif roll.startswith("24C0"): rank = 4
    elif roll.startswith("23C0"): rank = 5
    else: rank = 6
    
    return (rank, roll)

def reorder_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    pages_data = []
    
    print("Reading and analyzing pages...")
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        sort_key = get_sort_key(text)
        pages_data.append((sort_key, page))
    
    # Sort pages based on the rank first, then the roll number string
    pages_data.sort(key=lambda x: x[0])
    
    print("Writing sorted PDF...")
    for _, page in pages_data:
        writer.add_page(page)
        
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"Success! Sorted file saved as: {output_path}")

# Usage
reorder_pdf("caution_letters_original.pdf", "caution_letters_SORTED.pdf")