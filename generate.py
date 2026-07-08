import os
import google.generativeai as genai
from analyze import build_summary

def build_prompt(langs, entries, key_files):
    lang_list = ", ".join(set(lang for _, lang in langs)) or "Unknown"

    prompt = f"""You are a technical documentation assistant.
Based on the information below about a software project, write clear and well-structured documentation in Markdown.

Include these sections:
1. Project Overview (what the project does)
2. Tech Stack (languages and main dependencies)
3. Project Structure (explain the main folders/files)
4. Getting Started (how to install and run it)

Be concise and accurate. Only state what you can infer from the provided information.

--- PROJECT INFO ---

Detected languages: {lang_list}

Entry points: {", ".join(entries) if entries else "none found"}

Key files content:
"""
    for name, content in key_files.items():
        prompt += f"\n### {name}\n```\n{content}\n```\n"

    return prompt

def generate_docs(langs, entries, key_files):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY not set. Run: export GEMINI_API_KEY='your-key'")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = build_prompt(langs, entries, key_files)
    print("Sending to Gemini... (this may take a few seconds)")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    root, langs, entries, key_files = build_summary("downloaded_repo")

    docs = generate_docs(langs, entries, key_files)

    print("\n\n=== GENERATED DOCUMENTATION ===\n")
    print(docs)

    # Save to a file
    with open("GENERATED_DOCS.md", "w", encoding="utf-8") as f:
        f.write(docs)
    print("\n\nSaved to GENERATED_DOCS.md")
