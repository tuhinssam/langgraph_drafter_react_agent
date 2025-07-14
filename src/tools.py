from langchain_core.tools import tool

@tool
def update(content: str) -> str:
    """
    updates the document with provided content
    """
    global document_content
    document_content = content
    return f"document has been updated successfully. current content is\n: {document_content}"

@tool
def save(filename: str) -> str:
    """
    save the current document to a text file and finish the process
    :Args
        filename: name for the text file
    """
    global document_content
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    try:
        with open(filename, "w") as f:
            f.write(document_content)
        print(f"\nDocument saved to {filename}")
        return f"Document has been saved successfully to '{filename}'."
    except FileNotFoundError as e:
        return f"error saving document to {filename}: {str(e)}"
