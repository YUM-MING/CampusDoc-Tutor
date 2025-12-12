import httpx
import os
import sys

BASE_URL = "http://127.0.0.1:8000"

def check_server():
    print(f"Checking server at {BASE_URL}...")
    try:
        response = httpx.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
    except httpx.ConnectError:
        print("❌ Server is NOT running.")
        print("Please run the server in a separate terminal: uvicorn src.api.main:app --reload")
        return False
    return False

def ingest_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"Uploading {file_path}...")
    files = {'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/pdf')}
    try:
        response = httpx.post(f"{BASE_URL}/ingest", files=files, timeout=30.0)
        if response.status_code == 200:
            print("✅ Ingest successful:", response.json())
            return True
        else:
            print("❌ Ingest failed:", response.text)
    except Exception as e:
        print(f"❌ Error during ingest: {e}")
    return False

def ask_question(question):
    print(f"Asking: '{question}'...")
    try:
        response = httpx.post(
            f"{BASE_URL}/ask", 
            json={"question": question}, 
            timeout=60.0
        )
        if response.status_code == 200:
            data = response.json()
            print("\n🤖 Answer:")
            print(data["answer"])
            print("\n📄 Citations:")
            for cite in data["citations"]:
                print(f"- [{cite['source']} p.{cite['page']}]: {cite['content'].strip()}")
            return True
        else:
            print("❌ Ask failed:", response.text)
    except Exception as e:
        print(f"❌ Error asking question: {e}")
    return False

if __name__ == "__main__":
    if not check_server():
        sys.exit(1)
    
    print("\n--- CampusDoc Tutor Verification ---")
    pdf_path = input("Enter path to a PDF file to ingest (or press Enter to skip ingest): ").strip()
    
    # Remove quotes if user pasted path as "path/to/file"
    if pdf_path.startswith('"') and pdf_path.endswith('"'):
        pdf_path = pdf_path[1:-1]
        
    if pdf_path:
        ingest_pdf(pdf_path)
    
    while True:
        q = input("\nEnter a question (or 'q' to quit): ").strip()
        if q.lower() == 'q':
            break
        if q:
            ask_question(q)
