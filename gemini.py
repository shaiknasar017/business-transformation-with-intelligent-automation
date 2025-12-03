import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") # Make sure to add this to your .env file!

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file.")
    print("👉 Get one here: https://aistudio.google.com/app/apikey")
    exit()

# 2. Configure Gemini
print("⚙️ Configuring Google Gemini...")
genai.configure(api_key=api_key)

# We use 'gemini-1.5-flash' because it's fast and cheap for automation
model = genai.GenerativeModel('gemini-1.5-flash')

def test_text_logic():
    print("\n--- TEST 1: TEXT ANALYSIS ---")
    
    # Simulate a messy business email
    manual_input = """
    URGENT: Invoice #9922 from CyberDyne Systems.
    Total due is $4,500.25. 
    Please pay by 2025-12-15. 
    Notes: Late fees apply after 30 days.
    """
    
    prompt = """
    You are a Data Extraction Agent. 
    Extract the following fields from the text below and return strictly valid JSON:
    - vendor_name
    - invoice_number
    - total_amount
    - due_date
    - late_fee_policy (boolean)

    Input Text:
    """ + manual_input

    try:
        response = model.generate_content(prompt)
        print("✅ Gemini Response Received:")
        print(response.text)
    except Exception as e:
        print(f"❌ Text Test Failed: {e}")

def test_vision_logic():
    print("\n--- TEST 2: VISION ANALYSIS ---")
    
    # Create a dummy image for testing if one doesn't exist
    img_path = "test_image.jpg"
    
    if not os.path.exists(img_path):
        # Create a simple red image just to test the connection
        img = PIL.Image.new('RGB', (100, 30), color = (73, 109, 137))
        img.save(img_path)
        print(f"ℹ️ Created temporary test image: {img_path}")

    try:
        sample_file = PIL.Image.open(img_path)
        
        prompt = "Analyze this image. Describe what you see in 10 words or less. Return JSON format."
        
        response = model.generate_content([prompt, sample_file])
        print("✅ Vision Response Received:")
        print(response.text)
        
    except Exception as e:
        print(f"❌ Vision Test Failed: {e}")

if __name__ == "__main__":
    print("🤖 STARTING GEMINI CONNECTION TEST...")
    test_text_logic()
    test_vision_logic()
    print("\n🏁 TEST COMPLETE.")
