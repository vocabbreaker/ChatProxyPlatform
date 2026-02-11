# Quick User Management Guide

## For Teachers Without Computer Knowledge

### 📋 What You Need
- `users.csv` file (open with Excel or Notepad)
- `sync_all_users.bat` file (double-click to run)

---

## How to Add a New Student

1. Open `users.csv` in Excel
2. Add a new row with these details:

| action | username  | email              | password   | role    | fullName      | credits |
|--------|-----------|-------------------|------------|---------|---------------|---------|
| create | student6  | student6@school.com| Student6!  | student | John Smith    | 1000    |

3. Save the file
4. Double-click `sync_all_users.bat`
5. Wait for "SUCCESS!" message
6. Done! ✅

---

## How to Add a New Teacher

Same as above, but use:
- **role**: `teacher`
- **credits**: `5000` (teachers get more credits)

Example:
| action | username  | email              | password   | role    | fullName      | credits |
|--------|-----------|-------------------|------------|---------|---------------|---------|
| create | teacher4  | teacher4@school.com| Teacher4!  | teacher | Jane Doe      | 5000    |

---

## How to Remove a User

1. Open `users.csv` in Excel
2. Find the user's row
3. Change `create` to `delete` in the action column:

| action | username  | email              | password   | role    | fullName      | credits |
|--------|-----------|-------------------|------------|---------|---------------|---------|
| delete | student6  | student6@school.com| Student6!  | student | John Smith    | 1000    |

4. Save the file
5. Double-click `sync_all_users.bat`
6. Done! ✅

**Note:** This will:
- ✅ Remove the user from the system (they can't login)
- ✅ **Automatically remove all their credits** from accounting

---

## How to Change Credits

1. Open `users.csv` in Excel
2. Find the user's row
3. Change the number in the `credits` column
4. Save the file
5. Double-click `sync_all_users.bat`
6. Done! ✅

---

## ⚠️ Important Rules

1. **Always use `action = create`** for active users
2. **Only use `action = delete`** to remove users
3. **Never delete rows** - just change `create` to `delete`
4. **Passwords must be strong**: At least 8 characters with letters and numbers
5. **Emails must be unique**: No two users can have the same email

---

## 🎯 Quick Examples

### Add 3 students at once:
```
action,username,email,password,role,fullName,credits
create,student6,student6@school.com,Student6!,student,Alice Brown,1000
create,student7,student7@school.com,Student7!,student,Bob Wilson,1000
create,student8,student8@school.com,Student8!,student,Carol Davis,1000
```

### Give a student more credits:
```
action,username,email,password,role,fullName,credits
create,student1,student1@school.com,Student1!,student,Student One,2000
```
(Changed from 1000 to 2000)

---

## 🔧 Troubleshooting

**Problem**: "User already exists"
- **Solution**: The user is already created. If you want to update credits, just change the credits column and run the batch file again.

**Problem**: "Login failed"  
- **Solution**: Make sure Docker containers are running. Check that you see "auth-service" and "accounting-service" in Docker Desktop.

**Problem**: "Email not verified"
- **Solution**: Run `sync_all_users.bat` again - it will verify all users automatically.

---

## 📁 Files You'll Use

| File | What it does | When to use |
|------|--------------|-------------|
| **users.csv** | Contains all user information | Edit this to add/remove users or change credits |
| **sync_all_users.bat** | Applies all changes | Run this after editing users.csv |

---

## ✅ That's It!

Just remember:
1. **Edit CSV** → Add/remove users, change credits
2. **Run BAT** → Double-click sync_all_users.bat
3. **Wait for SUCCESS** → You're done!
