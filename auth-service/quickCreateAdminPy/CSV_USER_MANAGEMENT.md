# CSV User Management Guide

This folder contains scripts to manage users (create/delete) via CSV file with admin privileges.

## Quick Start

1. **Edit the CSV file:**
   ```batch
   notepad users.csv
   ```
   (Or copy from `users_template.csv` to start)

2. **Run the management script as Administrator:**
   - Right-click `manage_users_admin.bat`
   - Select "Run as administrator"

## CSV Format

```csv
action,username,email,password,role,fullName
create,teacher1,teacher1@school.com,Teacher@123,teacher,John Smith
delete,olduser,olduser@school.com,,,
```

### Fields:

- **action** (Required): `create` or `delete`
- **username** (Required): Unique username (3-50 characters)
- **email** (Required): Valid email address
- **password** (Required for create): Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
- **role** (Optional): `admin`, `supervisor`, `teacher`, `student`, `enduser` (default: enduser)
- **fullName** (Optional): User's full name

## Available Roles

- **admin** - Full system access
- **supervisor** - Limited administrative capabilities
- **teacher** - Teacher/instructor access
- **student** - Student access
- **enduser** - Basic user access (default)

## Examples

### Create Multiple Teachers
```csv
action,username,email,password,role,fullName
create,teacher1,teacher1@school.com,Teacher@123,teacher,John Smith
create,teacher2,teacher2@school.com,Teacher@456,teacher,Jane Doe
```

### Create Multiple Students
```csv
action,username,email,password,role,fullName
create,student1,student1@school.com,Student@123,student,Alice Johnson
create,student2,student2@school.com,Student@456,student,Bob Wilson
create,student3,student3@school.com,Student@789,student,Carol Martinez
```

### Delete Users
```csv
action,username,email,password,role,fullName
delete,olduser1,olduser1@school.com,,,
delete,olduser2,olduser2@school.com,,,
```

### Mixed Operations
```csv
action,username,email,password,role,fullName
create,newteacher,newteacher@school.com,Teacher@2026,teacher,New Teacher
create,newstudent,newstudent@school.com,Student@2026,student,New Student
delete,olduser,olduser@school.com,,,
```

## Logs

All operations are logged to `user_management.log` with timestamps.

Example log entry:
```
[2026-02-10 14:30:15] [SUCCESS] ✓ Created user: teacher1 (teacher1@school.com) - Role: teacher - ID: 698abc123...
[2026-02-10 14:30:16] [SUCCESS] ✓ Deleted user: olduser (olduser@school.com)
```

## Troubleshooting

### "This script requires Administrator privileges"
- Right-click the .bat file and select "Run as administrator"

### "CSV file not found"
- The script will create `users.csv` from the template
- Edit it with your user data and run again

### "Admin login failed"
- Ensure auth-service is running: `cd .. && start.bat`
- Verify admin account exists: `list_users.bat`

### "Failed to create user"
- Check password requirements (min 8 chars, uppercase, lowercase, number, special char)
- Ensure username and email are unique
- Check logs for detailed error messages

## Files

- **users_template.csv** - Template with examples
- **users.csv** - Your actual user data (edit this)
- **manage_users_csv.py** - Python script that processes the CSV
- **manage_users_admin.bat** - Batch script requiring admin rights
- **user_management.log** - Operation log file
- **CSV_USER_MANAGEMENT.md** - This guide

## Security Notes

⚠️ **Important:**
- Store `users.csv` securely (contains passwords)
- Change default passwords after first login
- Use strong passwords in production
- Consider deleting CSV file after user creation
- Review logs for any failed operations
