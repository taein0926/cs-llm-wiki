import os
import re
from typing import List, Dict, Optional

# Constants for file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIKI_DIR = os.path.join(BASE_DIR, "docs", "wiki")

def read_wiki(page_name: str) -> str:
    """
    Reads the content of a markdown file from the docs/wiki directory.

    Args:
        page_name (str): The name of the wiki page (without .md extension).

    Returns:
        str: The content of the markdown file.

    Raises:
        FileNotFoundError: If the specified wiki page does not exist.
    """
    file_path = os.path.join(WIKI_DIR, f"{page_name}.md")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Wiki page '{page_name}' not found at {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_wiki(page_name: str, content: str) -> bool:
    """
    Writes content to a wiki page while preserving the 'Human Protected' section.
    This implements the core data governance logic described in the PRD.

    Args:
        page_name (str): The name of the wiki page (without .md extension).
        content (str): The new markdown content provided by the agent.

    Returns:
        bool: True if the file was written successfully, False otherwise.
    """
    if not os.path.exists(WIKI_DIR):
        os.makedirs(WIKI_DIR, exist_ok=True)
        
    file_path = os.path.join(WIKI_DIR, f"{page_name}.md")
    
    # Human Protected section markers
    TAG_START = "<!-- [Human Protected: Start] -->"
    TAG_END = "<!-- [Human Protected: End] -->"
    
    # 1. Extraction Phase: Look for existing protected content
    existing_protected_content = ""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            old_file_content = f.read()
            # Regex to find content between tags (non-greedy)
            pattern = rf"{re.escape(TAG_START)}(.*?){re.escape(TAG_END)}"
            match = re.search(pattern, old_file_content, re.DOTALL)
            if match:
                existing_protected_content = match.group(1)

    # 2. Integration Phase: Inject preserved content into the new content
    if existing_protected_content:
        # Replace the placeholder tags in the new content with the preserved data
        new_pattern = rf"({re.escape(TAG_START)})(.*?)({re.escape(TAG_END)})"
        if re.search(new_pattern, content, re.DOTALL):
            content = re.sub(new_pattern, rf"\1{existing_protected_content}\3", content, flags=re.DOTALL)
        else:
            # If agent failed to include tags, append the protected section at the end as a safety measure
            content += f"\n\n{TAG_START}{existing_protected_content}{TAG_END}\n"

    # 3. Persistence Phase: Write to file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"[Error] Failed to write wiki page '{page_name}': {e}")
        return False

def search_cve(keyword: str) -> List[Dict]:
    """
    Simulates searching an external CVE database for security vulnerabilities.
    
    Args:
        keyword (str): Search term (e.g., 'Buffer Overflow', 'TCP', 'OS Kernel').

    Returns:
        List[Dict]: A list of dictionaries containing CVE ID, severity, and summary.
    """
    # Simulated CVE database entries
    MOCK_CVE_DATA = [
        {
            "id": "CVE-2024-1024",
            "keyword": "Buffer Overflow",
            "severity": "Critical",
            "summary": "Stack-based buffer overflow in the OS memory management unit allowing RCE."
        },
        {
            "id": "CVE-2024-2048",
            "keyword": "TCP",
            "severity": "High",
            "summary": "Improper state handling in TCP stack leads to resource exhaustion and DoS."
        },
        {
            "id": "CVE-2023-5060",
            "keyword": "Memory",
            "severity": "Critical",
            "summary": "Use-after-free vulnerability in shared memory allocation logic."
        },
        {
            "id": "CVE-2024-9999",
            "keyword": "Network",
            "severity": "Medium",
            "summary": "Information disclosure vulnerability via side-channel analysis of encrypted packets."
        }
    ]
    
    # Filter simulation based on keyword (case-insensitive)
    results = [
        cve for cve in MOCK_CVE_DATA 
        if keyword.lower() in cve["keyword"].lower() or keyword.lower() in cve["summary"].lower()
    ]
    
    # Fallback result if no match is found
    if not results:
        results = [{
            "id": "CVE-INFO-ONLY",
            "keyword": keyword,
            "severity": "N/A",
            "summary": f"No active critical CVEs found for '{keyword}', but security audits are recommended."
        }]
    
    return results

if __name__ == "__main__":
    print("=== [MCP Wiki Tools] Self-Test Routine ===")
    
    # Test 1: CVE Search Simulation
    print("\n[Test 1] Searching for 'Buffer Overflow'...")
    results = search_cve("Buffer Overflow")
    for r in results:
        print(f" > Found: {r['id']} ({r['severity']}) - {r['summary']}")

    # Test 2: Write Wiki with Human Protection
    print("\n[Test 2] Testing Data Governance (Write/Protect)...")
    test_page = "governance_test"
    
    # 2-a. Initial write (by Human or Agent)
    initial_content = f"""# Test Governance
This is some base content.
<!-- [Human Protected: Start] -->
- CRITICAL: Do not remove this system requirement note.
- Decision: Use AES-256 for all local storage.
<!-- [Human Protected: End] -->
"""
    write_wiki(test_page, initial_content)
    print(f"Created initial page '{test_page}.md'.")

    # 2-b. Agent attempt to overwrite protected content
    agent_overwrite_attempt = f"""# Updated Title by Agent
The agent is attempting to refresh this page.
<!-- [Human Protected: Start] -->
[Agent's temporary placeholder - should be replaced by preserved content]
<!-- [Human Protected: End] -->
"""
    write_wiki(test_page, agent_overwrite_attempt)
    print("Agent attempted an update (Governance should trigger).")

    # 2-c. Verify results
    verified_content = read_wiki(test_page)
    print("\n--- Final File Content ---")
    print(verified_content)
    print("--------------------------")
    
    if "Use AES-256" in verified_content:
        print("\n✅ SUCCESS: Human Protected section was PRESERVED.")
    else:
        print("\n❌ FAILURE: Human Protected section was LOST.")
