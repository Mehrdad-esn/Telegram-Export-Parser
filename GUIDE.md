# 🚀 Telegram Export Parser - Complete Guide

## Project Summary

Your Telegram Export Parser has been **completely redesigned and upgraded** with professional-grade features.

## 📂 New Project Structure

```
Telegram Export Parser/
├── app.py                    # Main CLI application (refactored)
├── utils.py                  # Core utilities & helpers
├── stats.py                  # Statistics & analysis
├── filters.py                # Advanced message filtering
├── exporters.py              # Multi-format exporters
├── config.py                 # Configuration management
├── web_ui.py                 # Web interface (Flask)
├── examples.py               # Usage examples & demos
├── telegram_to_text.py       # Original version (backup)
├── test_data.json            # Test dataset
├── requirements.txt          # Dependencies
├── config.json               # Configuration file
├── README.md                 # Documentation
├── GUIDE.md                  # This file
├── templates/
│   └── index.html            # Web UI template
├── telegram_output/          # Output directory
├── examples_output/          # Example outputs
└── .gitignore               # Git ignore rules
```

## ✨ Key Features Implemented

### 🎯 Phase 1: Advanced Filtering ✅

- ✅ Date range filtering (--from-date, --to-date)
- ✅ Sender name filtering
- ✅ Keyword search with regex support
- ✅ Message length filtering
- ✅ Media filtering
- ✅ Chainable filters

### 📊 Phase 2: Statistics & Analysis ✅

- ✅ Message count per sender
- ✅ Word frequency analysis
- ✅ Daily message statistics
- ✅ Average message length
- ✅ Top talkers ranking
- ✅ Professional summary reports

### 📁 Phase 3: Multi-Format Export ✅

- ✅ Text (TXT) - Plain text with formatting
- ✅ CSV - Spreadsheet compatible
- ✅ JSON - Structured data format
- ✅ HTML - Web viewable
- ✅ Markdown - Documentation ready
- ✅ Excel (XLSX) - With formatting

### 🎨 Phase 4: Web UI (Partial) ✅

- ✅ Modern responsive interface
- ✅ Drag-drop file upload
- ✅ Real-time chat preview
- ✅ Format selection
- ✅ Statistics display
- ✅ One-click export

### ⚙️ Phase 5: Configuration & Extensibility ✅

- ✅ Config file support (JSON)
- ✅ Modular architecture
- ✅ Plugin-ready exporters
- ✅ Custom filter framework
- ✅ Environment variable support

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Optional: Create config
python config.py
```

### Command Line Usage

**Interactive mode (choose chat):**

```bash
python app.py -i result.json
```

**Export all chats to CSV:**

```bash
python app.py -i result.json --all-chats --format csv
```

**Show statistics:**

```bash
python app.py -i result.json --stats-only
```

**Export specific chat to HTML:**

```bash
python app.py -i result.json -c "Chat Name" --format html
```

### Web UI (Beta)

```bash
# Install Flask
pip install flask

# Run web server
python web_ui.py

# Open browser
# http://localhost:5000
```

## 💡 Usage Examples

### Example 1: Filter & Export

```python
from filters import MessageFilter
from exporters import CSVExporter

# Load your data
messages = [...]  # Your messages

# Apply filters
msg_filter = MessageFilter(messages)
msg_filter.add_keyword_filter(["سلام"]) \
          .add_date_range("2024-01-01", "2024-12-31")

filtered = msg_filter.apply()

# Export
exporter = CSVExporter(filtered, id_index)
exporter.export(Path("output.csv"))
```

### Example 2: Get Statistics

```python
from stats import MessageStats

stats = MessageStats(messages)
stats.print_summary()

# Access individual stats
top_talkers = stats.get_top_talkers(10)
word_freq = stats.get_word_frequency(20)
daily = stats.get_daily_message_count()
```

### Example 3: Custom Processing

```python
from utils import extract_plain_text, extract_sender_name

for message in messages:
    sender = extract_sender_name(message)
    text = extract_plain_text(message.get("text"))
    print(f"{sender}: {text}")
```

## 🔄 Workflow: From Export to Analysis

```
result.json (Telegram Export)
    ↓
[Parse & Load] ← utils.py
    ↓
[List Chats]
    ↓
[Select Chat]
    ↓
[Apply Filters] ← filters.py
    ↓
[Analyze Stats] ← stats.py
    ↓
[Export Format] ← exporters.py
    ├─ TXT
    ├─ CSV
    ├─ JSON
    ├─ HTML
    ├─ MD
    └─ XLSX
```

## 📊 Supported Export Formats

| Format   | Best For        | Size   | Features       |
| -------- | --------------- | ------ | -------------- |
| **TXT**  | Quick preview   | Small  | Human-readable |
| **CSV**  | Excel/Sheets    | Small  | Tabular data   |
| **JSON** | APIs/Processing | Medium | Structured     |
| **HTML** | Web viewing     | Medium | Styled UI      |
| **MD**   | Documentation   | Small  | Git-friendly   |
| **XLSX** | Excel reports   | Medium | Formatting     |

## 🎯 Common Tasks

### Task 1: Export All Messages from a User

```bash
# CLI doesn't have direct filter yet, use Python:
python -c "
from app import *
from filters import MessageFilter
chats = list(iter_chats(Path('result.json')))
for chat in chats:
    msgs = chat.get('messages', [])
    f = MessageFilter(msgs).add_sender_filter(['UserName'])
    print(f'Found {len(f.apply())} messages')
"
```

### Task 2: Generate Monthly Statistics

```python
from stats import MessageStats
from filters import MessageFilter

# Get messages from this month
msg_filter = MessageFilter(messages)
msg_filter.add_date_range("2024-01-01", "2024-01-31")
monthly_msgs = msg_filter.apply()

# Analyze
stats = MessageStats(monthly_msgs)
stats.print_summary()
```

### Task 3: Create an Excel Report

```bash
python app.py -i export.json --all-chats --format xlsx --stats
```

## 🔧 Configuration (config.json)

```json
{
  "output_directory": "telegram_output",
  "default_export_format": "csv",
  "include_stats": true,
  "auto_translate": false,
  "translation_language": "en",
  "max_message_length": 0,
  "theme": "light"
}
```

## 🚀 Next Steps (Future Enhancements)

- [ ] Auto-translation using Google Translate API
- [ ] Sentiment analysis with TextBlob/spaCy
- [ ] Interactive charts & graphs (Plotly)
- [ ] Database storage (SQLite)
- [ ] Real-time monitoring dashboard
- [ ] Duplicate message detection
- [ ] User network analysis
- [ ] Advanced NLP features
- [ ] Mobile app integration
- [ ] Cloud sync support

## 🐛 Troubleshooting

**Q: "ijson not installed"**

```bash
pip install ijson
```

**Q: "Permission denied" when exporting**

- Check folder permissions
- Ensure `telegram_output` directory is writable

**Q: Web UI shows "Cannot GET /api/upload"**

- Make sure Flask is installed: `pip install flask`
- Check templates folder exists
- Restart Flask server

**Q: Slow processing for large files**

- Use ijson for streaming (automatic)
- Process one chat at a time
- Consider filtering before export

## 📈 Performance Tips

- Use `--all-chats` instead of multiple runs
- Filter before export to reduce file size
- Use CSV for large exports (smaller than JSON)
- Enable stats only mode to skip export: `--stats-only`

## 🤝 Contributing

To extend this project:

1. **Add new exporter:**
   - Inherit from `BaseExporter` in exporters.py
   - Implement `export()` method

2. **Add new filter:**
   - Add method to `MessageFilter` class
   - Use chainable API pattern

3. **Add new statistics:**
   - Add method to `MessageStats` class
   - Update `print_summary()` if needed

## 📝 License

MIT License - Feel free to use and modify!

## 📞 Support

For issues:

- Check examples.py for usage patterns
- Review test_data.json for input format
- Enable debug mode: `--debug`

---

**Version:** 2.0.0  
**Last Updated:** 2024-01-16  
**Status:** ✅ Production Ready
