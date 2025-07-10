# How to Update the Master Index

## What is the Master Index?
The master index is a file that keeps track of all the game content areas (like actors, events, world locations, etc.) in the Metro AI RPG project. It helps the system know where to find different types of game data.

## What does the Update Script Do?
The `update_master_index.py` script automatically:
• Scans all game content directories
• Updates the master index with any new or changed files
• Refreshes timestamps and metadata
• Ensures all content areas are properly tracked

## Before You Start
**You'll need:**
• Access to the Metro AI RPG project files
• Python installed on your device
• A terminal or command prompt app

**On smartphone:** Use apps like Termux (Android) or iSH (iOS) for terminal access.

## Step-by-Step Instructions

### Step 1: Find the Script
• Open your terminal/command app
• Navigate to the Metro AI RPG project folder:
  ```
  cd /path/to/metro-ai-rpg
  ```
• The script should be located in the main project directory as `update_master_index.py`

### Step 2: Run the Script
• Type this command and press Enter:
  ```
  python update_master_index.py
  ```
• **On some systems, you might need to use:**
  ```
  python3 update_master_index.py
  ```

### Step 3: Watch for Output
The script will show you:
• ✅ Which areas it's scanning
• 📝 Any updates it makes
• ⚠️ Any problems it finds
• ✨ A success message when complete

**Example output you might see:**
```
Scanning actors directory...
Scanning events directory...
Found 3 new event files
Updated master_index.json
✅ Master index updated successfully!
```

### Step 4: Check What Changed
After the script runs:

**1. Look at the master_index.json file**
• Open `master_index.json` in any text editor
• Check that the `last_modified` timestamp is recent
• Verify all your content areas are listed

**2. Check for any error messages**
• If you see red text or error messages, note them down
• Some common issues and fixes:
  - **"Permission denied"** → Make sure you can write to the project folder
  - **"Python not found"** → Install Python or use `python3` instead
  - **"File not found"** → Make sure you're in the right folder

**3. Verify your content is tracked**
• All your game content directories should appear in the master index
• New files should be reflected in the updated timestamps

## Troubleshooting

### Script Won't Run
• **Check you're in the right folder:** Use `ls` (or `dir` on Windows) to see if `master_index.json` is there
• **Try with python3:** Some systems need `python3` instead of `python`
• **Check file permissions:** Make sure the script file is executable

### No Changes Detected
• This is normal if you haven't added new content recently
• The script still updates timestamps to show it ran successfully

### Error Messages
• **Read the message carefully** - it usually tells you what's wrong
• **Check file paths** - make sure all your content directories exist
• **Try running again** - sometimes temporary issues resolve themselves

## Tips for Smartphone Users

### Make It Easier
• **Bookmark your project folder** in your terminal app
• **Create a shortcut** for the command in your notes app
• **Run this regularly** after adding new game content

### Quick Command Reference
```bash
# Navigate to project
cd /path/to/metro-ai-rpg

# Run the update script  
python update_master_index.py

# Check what's in the current folder
ls

# View the master index file
cat master_index.json
```

## When to Run This Script
**Run the update script:**
• ✨ After adding new actors, events, or locations
• 📝 After modifying existing game content files  
• 🔄 Before starting a game session
• 🛠️ As part of your regular maintenance routine

**You don't need to run it:**
• After only changing system settings
• When just reading or viewing files
• If you haven't made any content changes

## Need Help?
If you run into problems:
1. **Read the error message** - it usually explains the issue
2. **Check this guide again** - make sure you followed all steps
3. **Try the troubleshooting section** above
4. **Ask for help** from other project contributors

Remember: It's safe to run this script multiple times - it only updates what needs updating!