# 🌐 URL Checker

> 🚀 A powerful terminal-based application for validating multiple URLs concurrently with a user-friendly interface and Excel export functionality.

```ascii
##   ##  ######    ##                ######   ######   ####     ######   ######  ######
##   ##  ##   ##   ##                # ## #   ##      ##  ##    # ## #   ##      ##   ##
##   ##  ##   ##   ##                  ##     ##      ##          ##     ##      ##   ##
##   ##  ##  ###   ##                  ##     #####    #####      ##     #####   ##  ###
##   ##  #####     ##                  ##     ##           ##     ##     ##      #####
##   ##  ## ###    ##   #              ##     ##      ##   ##     ##     ##      ## ###
 #####   ##  ###   ######              ##     ######   #####      ##     ######  ##  ###
```

## ✨ Features

⚡ **Concurrent Processing**: Multiple URLs checked simultaneously  
🖥️ **Interactive UI**: Beautiful terminal interface  
📊 **Excel Export**: Save results in organized spreadsheets  
🔄 **Real-time Updates**: Live status monitoring  
📜 **Scrollable Results**: Easy navigation through long lists  
🎨 **Color Coding**: ✅ Green for valid, ❌ Red for invalid URLs  
🔄 **Quick Reload**: Refresh and recheck without restarting

## 📋 Prerequisites

```bash
🔧 pip install requests openpyxl
```

## 🚀 Setup

1️⃣ Create a `urls.txt` file in the script directory  
2️⃣ Add URLs (one per line):

```text
🔗 https://example.com
🔗 https://google.com
🔗 https://github.com
```

## 🎮 Usage

### Start the Application

```bash
▶️ python url_checker.py
```

### 🎯 Controls

```
⌨️  's' → Start Test
⌨️  'q' → Quit & Save
⌨️  'r' → Reload URLs
⌨️  ↑/↓ → Scroll Results
```

## 📊 Output Format

Excel file contains:
| Column | Description |
|--------|-------------|
| 🔗 URL | Web address |
| ✅ Status | Valid/Invalid |

## 🔧 Technical Details

- ⏱️ 5-second timeout per URL
- 📝 200 status code = valid
- 💾 .xlsx output format
- 📐 Terminal size: 100x25 minimum

## ⚠️ Error Handling

The app handles:

- 📄 Missing urls.txt
- 🌐 Network issues
- ❌ Invalid URLs
- 📱 Small terminals

## 🤝 Contributing

```
👥 Issues welcome!
🛠️ Pull requests appreciated
💡 Enhancement ideas encouraged
```

## 📜 License

```
⚖️ MIT License
```

## 🔍 Status Indicators

```
✅ Valid URL
❌ Invalid URL
⏳ Processing
🔄 Reloading
```

---

💫 **Happy URL Checking!** 💫

> 💡 **Pro Tip**: Keep your urls.txt file organized and regularly updated for best results!
