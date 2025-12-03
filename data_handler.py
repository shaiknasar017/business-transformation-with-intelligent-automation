To complete your Business Automation Agent, you need a **Data Handler**.

In your image, this is the "Transformation" arrow. It is responsible for physically moving files from the messy "Manual" pile, feeding them to the Core, and saving them into the clean "Intelligent" folder.

Create a new file named `data_handler.py` inside your `src` folder.

### 1\. The Data Handler (`src/data_handler.py`)

This module manages your file system. It reads text files, logs operations, and saves the final JSON.

```python
import os
import json
import shutil
from datetime import datetime

class DataHandler:
    def __init__(self, input_dir="data/raw_input", output_dir="data/processed_output"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Ensure directories exist
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def read_files(self):
        """
        Scans the input folder for text files.
        Returns a list of tuples: (filename, content)
        """
        files_found = []
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.input_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        files_found.append((filename, content))
                except Exception as e:
                    print(f"⚠️ Error reading {filename}: {e}")
        
        return files_found

    def save_result(self, original_filename, data_json):
        """
        Saves the structured JSON to the output folder.
        """
        # Create a new filename (e.g., invoice.txt -> invoice_processed.json)
        base_name = os.path.splitext(original_filename)[0]
        new_filename = f"{base_name}_processed.json"
        save_path = os.path.join(self.output_dir, new_filename)

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(data_json, f, indent=4)
            print(f"✅ Saved structured data to: {save_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False

    def archive_file(self, filename):
        """
        Moves the original file to an 'archive' folder so it's not processed twice.
        """
        archive_dir = os.path.join(self.input_dir, "archive")
        os.makedirs(archive_dir, exist_ok=True)
        
        src = os.path.join(self.input_dir, filename)
        dst = os.path.join(archive_dir, filename)
        
        shutil.move(src, dst)
        print(f"📦 Archived original file: {filename}")
```

-----

### 2\. Putting it all together (`src/main.py`)

Now, update your `main.py` one last time. This version connects the **Core** (Brain) with the **Data Handler** (Hands).

```python
from core import CoreAgent
from data_handler import DataHandler
import time

def main():
    # 1. Initialize Components
    brain = CoreAgent()
    hands = DataHandler()
    
    print("--- 🏭 Business Automation Agent Started ---")
    print(f"Monitoring folder: {hands.input_dir}...\n")

    # 2. Main Automation Loop
    while True:
        # Get files from the 'Manual' pile
        files = hands.read_files()
        
        if not files:
            # No files found, wait a bit and check again
            time.sleep(5)
            continue

        print(f"📄 Found {len(files)} new document(s). Processing...")

        for filename, content in files:
            print(f"   > Transformation started for: {filename}")
            
            # A. The Brain processes the text
            structured_data = brain.process(content)
            
            # B. The Hands save the result
            if hands.save_result(filename, structured_data):
                # C. Move original file to archive
                hands.archive_file(filename)
                
        print("\n--- ✅ Batch Complete. Waiting for new files... ---")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user.")
```

### 3\. How to test this "Data" workflow

1.  **Run the script:** Type `python src/main.py` in your terminal. It will say it is monitoring the folder.
2.  **Create a test file:** Go into your `data/raw_input` folder and create a file called `test_invoice.txt` with some messy text inside (e.g., "Invoice for $500 to John Doe").
3.  **Watch the magic:**
      * The agent detects the file.
      * It reads it.
      * It converts it to JSON.
      * It saves the JSON in `data/processed_output`.
      * It moves the text file to `data/raw_input/archive`.

[Image of data processing pipeline diagram]

**Next Step:** Would you like a **Streamlit Dashboard** code so you can view these processed files in a nice web interface instead of just looking at folders?
