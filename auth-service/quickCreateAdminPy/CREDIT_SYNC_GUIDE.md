# Simple Credit Management Guide

Quick and easy credit management using CSV file.

## How It Works

1. Edit `users.csv` and add/update the `credits` column
2. Run `sync_credits.bat`
3. Script reads the CSV and sets each user's credits to the specified amount

## CSV Format

```csv
action,username,email,password,role,fullName,credits
create,teacher1,teacher1@school.com,Teacher@2026,teacher,John Smith,5000
create,student1,student1@school.com,Student@2026,student,Alice,1000
```

### Credits Column:
- **Set the exact amount** you want each user to have
- Run `sync_credits.bat` anytime to update credits
- Users not found will be skipped with a warning

## Quick Start

### 1. Edit Credits
```batch
notepad users.csv
```

Add credits for each user:
- Teachers: 5000 credits
- Students: 1000 credits

### 2. Sync Credits
```batch
sync_credits.bat
```

This will set all users to their specified credit amounts.

## Examples

### Give Teachers More Credits
```csv
teacher1,teacher1@school.com,...,5000
teacher2,teacher2@school.com,...,8000
```

### Reset Student Credits
```csv
student1,student1@school.com,...,1000
student2,student2@school.com,...,1000
```

### Mixed Amounts
```csv
teacher1,teacher1@school.com,...,10000
student1,student1@school.com,...,500
student2,student2@school.com,...,2000
```

## Features

✅ **Simple** - Just edit CSV and run bat file
✅ **Idempotent** - Safe to run multiple times
✅ **Fast** - Sets all credits in one run
✅ **Safe** - Only updates credits, doesn't delete users
✅ **Visible** - Shows success/error for each user

## What It Does

1. Reads `users.csv` file
2. Logs in as admin
3. For each user with credits:
   - Finds user by email
   - Sets credits to the CSV amount
   - Shows success/error message

## Troubleshooting

### "User not found"
- User hasn't been created yet
- Run `manage_users_admin.bat` first to create users

### "Failed to set credits"
- Accounting service may not be running
- Check: `cd ..\..\accounting-service && start.bat`

### "CSV file not found"
- Make sure you're in the `quickCreateAdminPy` folder
- Check if `users.csv` exists

## Tips

💡 **Bulk Updates**: Edit all credit amounts in CSV, run once
💡 **Regular Sync**: Run weekly/monthly to reset credits
💡 **Different Amounts**: Each user can have different credits
💡 **Quick Reset**: Change CSV values and re-run anytime
