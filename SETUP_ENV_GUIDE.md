# 🔐 Environment Setup Guide

## Your `.env` File Configuration

### ✅ What I've Done:

1. **Updated `LLM_habits.py`** to use environment variables instead of hardcoded API key
2. **Created `.gitignore`** to prevent `.env` from being committed to git
3. **Added `python-dotenv`** to `requirements.txt`

### ⚠️ Action Required:

Your `.env` file needs to contain the following variable:

```env
OPENROUTER_API_KEY=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
```

### 📝 How to Set It Up:

#### Option 1: Edit the existing .env file
Open your `.env` file and make sure it contains exactly:
```
OPENROUTER_API_KEY=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
```

**Important Format Rules:**
- ✅ No spaces around the `=` sign
- ✅ No quotes around the value
- ✅ Variable name must be exactly `OPENROUTER_API_KEY`
- ❌ Don't add spaces: `OPENROUTER_API_KEY = sk-or...` (wrong)
- ❌ Don't add quotes: `OPENROUTER_API_KEY="sk-or..."` (wrong)

#### Option 2: Use PowerShell to create it
```powershell
Set-Content -Path .env -Value "OPENROUTER_API_KEY=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"
```

### 🧪 Verify It Works:

Run the test script:
```bash
python test_env.py
```

You should see:
```
✅ OPENROUTER_API_KEY is loaded!
   Preview: sk-or-v1-a...2b3
   Length: 68 characters
```

### 📁 File Structure:

```
training/
├── .env                    # Your API key (NOT committed to git)
├── .gitignore              # Prevents .env from being tracked
├── ENV_TEMPLATE.txt        # Template for others
├── LLM_habits.py          # ✅ Updated to use .env
└── requirements.txt        # ✅ Added python-dotenv
```

### 🔒 Security Benefits:

- ✅ API key not in code
- ✅ API key not in git history
- ✅ Easy to share code without exposing credentials
- ✅ Can use different keys for dev/prod

### 🚀 Next Steps:

Once your `.env` file is properly configured:

1. Test it: `python test_env.py`
2. Run your script: `python LLM_habits.py`
3. Delete `test_env.py` and `explain_probability.py` if you want

---

**Note:** The `.env` file is already in your `.gitignore`, so your API key won't be committed to version control! 🔒
