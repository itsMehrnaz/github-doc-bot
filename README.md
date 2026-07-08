# GitHub Doc Bot

An automated documentation generator that takes a GitHub repository, analyzes its structure, and uses an AI model to produce clear project documentation. Built with a modular, pluggable model layer so it can work with different AI backends (cloud APIs or local models).

> **Status:** Core pipeline is complete and working (download → analyze → summarize). The AI generation layer is implemented but currently untested against a live model due to regional access restrictions on cloud APIs. The model layer is intentionally designed to be swappable — see [Roadmap](#roadmap--نقشه-راه).

---

## Features

- **Repository download** — fetches any public GitHub repo as a zip archive (no `git` install required), automatically resolving the default branch (`main` or `master`).
- **Language detection** — identifies the project's language and package manager from its manifest files (`Cargo.toml`, `package.json`, `pyproject.toml`, `go.mod`, and more).
- **Structure extraction** — builds a clean file tree, skipping noise like `.git`, `node_modules`, and build artifacts.
- **Key file collection** — reads the most informative files (README, manifests, entry points) to build a compact summary that fits within a model's context window.
- **Pluggable AI layer** — a single `generate_docs()` function isolates the model backend, so switching between Gemini, OpenAI, Claude, or a local Ollama model requires changing only one function.

---

## Architecture

The pipeline runs in distinct stages, each one feeding the next:

```
GitHub URL
    │
    ▼
Download repo (zip archive)
    │
    ▼
Detect language & manifest
    │
    ▼
Extract & summarize structure   ← the core: fits a large repo into limited context
    │
    ▼
AI model (pluggable backend)
    │
    ▼
Generated documentation (README.md + structure)
```

The hardest and most valuable part is the summarization stage: instead of sending an entire codebase to the model (which would overflow the context window), the tool sends a distilled summary — the full file tree, complete manifest and README contents, and the key entry points.

---

## Project Structure

```
github-doc-bot/
├── main.py            # Downloads a repo and prints its file tree
├── analyze.py         # Detects language, collects key files, builds the summary
├── generate.py        # Sends the summary to an AI model and writes the docs
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Getting Started

### Requirements

- Python 3.9+

### Installation

```bash
git clone https://github.com/itsMehrnaz/github-doc-bot.git
cd github-doc-bot
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Usage

Download a repository and view its structure:

```bash
python main.py https://github.com/psf/requests
```

Analyze the downloaded repository:

```bash
python analyze.py
```

Generate documentation (requires access to an AI model — see below):

```bash
export GEMINI_API_KEY="your-key-here"
python generate.py
```

---

## Roadmap / نقشه راه

- [x] Repository download
- [x] Language and manifest detection
- [x] Structure extraction and summarization
- [x] AI generation layer (implemented, pending live testing)
- [ ] Local model support via Ollama (removes any dependency on cloud API access)
- [ ] Telegram bot interface — send a repo link, receive a documentation file
- [ ] Support for large repositories via chunking and multi-pass generation
- [ ] Deeper per-language analysis using `tree-sitter` for function/class signatures

---

<div dir="rtl">

## درباره پروژه

این ابزار یک تولیدکننده‌ی خودکار مستندات است: یک ریپازیتوری گیت‌هاب را می‌گیرد، ساختارش را تحلیل می‌کند و با کمک یک مدل هوش مصنوعی برایش مستندات تمیز و خوانا تولید می‌کند. طراحی پروژه ماژولار است و لایه‌ی مدل به‌صورت pluggable ساخته شده تا با backendهای مختلف (API های ابری یا مدل‌های لوکال) کار کند.

## قابلیت‌ها

- **دانلود ریپازیتوری** — هر ریپوی عمومی گیت‌هاب را به‌صورت آرشیو zip دریافت می‌کند (بدون نیاز به نصب `git`) و به‌صورت خودکار branch اصلی را تشخیص می‌دهد.
- **تشخیص زبان** — زبان و پکیج‌منیجر پروژه را از روی فایل‌های مانیفست (مثل `Cargo.toml`، `package.json`، `pyproject.toml`) تشخیص می‌دهد.
- **استخراج ساختار** — یک درخت فایل تمیز می‌سازد و موارد اضافی مثل `.git` و `node_modules` را نادیده می‌گیرد.
- **جمع‌آوری فایل‌های کلیدی** — گویاترین فایل‌ها (README، مانیفست‌ها، نقاط ورود) را می‌خواند تا خلاصه‌ای فشرده بسازد که در context مدل جا شود.
- **لایه‌ی هوش مصنوعی قابل‌تعویض** — یک تابع `generate_docs()` مدل را ایزوله می‌کند، پس تعویض بین Gemini، OpenAI، Claude یا یک مدل لوکال مثل Ollama فقط تغییر یک تابع است.

## وضعیت فعلی

هسته‌ی اصلی پروژه (دانلود، تحلیل، خلاصه‌سازی) کامل و کارکننده است. لایه‌ی تولید مستندات با هوش مصنوعی نوشته شده اما به دلیل محدودیت‌های جغرافیایی روی API های ابری، هنوز روی یک مدل زنده تست نشده است. به همین دلیل لایه‌ی مدل عمداً طوری طراحی شده که به‌راحتی قابل تعویض باشد — از جمله با یک مدل لوکال که وابستگی به دسترسی ابری را کاملاً حذف می‌کند.

## نصب و اجرا

```bash
git clone https://github.com/itsMehrnaz/github-doc-bot.git
cd github-doc-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py https://github.com/psf/requests
```

</div>
