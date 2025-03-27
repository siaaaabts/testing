import pandas as pd

# Sample attendance data
attendance_data = {
    'student_id': [101, 101, 101, 101, 101, 102, 102, 102, 102, 103, 103, 103, 103, 103, 104, 104, 104, 104, 104],
    'attendance_date': [
        '2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05',
        '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05',
        '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08', '2024-03-09',
        '2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05'
    ],
    'status': [
        'Absent', 'Absent', 'Absent', 'Absent', 'Present',
        'Absent', 'Absent', 'Absent', 'Present',
        'Absent', 'Absent', 'Absent', 'Absent', 'Absent',
        'Present', 'Present', 'Absent', 'Present', 'Present'
    ]
}

# Sample students data
students_data = {
    'student_id': [101, 102, 103, 104, 105],
    'name': ['ALICE Johnson', 'Bob Smith', 'Charlie Brown', 'David Lee', 'Eva White'],
    'parent_email': [
        'alice_parent@example.com', 
        'bob_parent@example.com', 
        'invalid_email.com', 
        'invalid_email.com', 
        'eva_white@gmail.com'
    ]
}

# Create DataFrames
attendance_df = pd.DataFrame(attendance_data)
students_df = pd.DataFrame(students_data)

# Convert attendance_date to datetime
attendance_df['attendance_date'] = pd.to_datetime(attendance_df['attendance_date'])

# Find students with more than 3 consecutive absences
absent_streaks = []

for student_id, group in attendance_df.groupby('student_id'):
    group = group.sort_values('attendance_date')
    group['streak'] = (group['attendance_date'].diff() != pd.Timedelta(days=1)).cumsum()
    
    for streak_id, streak_group in group.groupby('streak'):
        if (streak_group['status'] == 'Absent').all() and len(streak_group) > 3:
            absence_start_date = streak_group['attendance_date'].min()
            absence_end_date = streak_group['attendance_date'].max()
            total_absent_days = len(streak_group)
            absent_streaks.append((student_id, absence_start_date, absence_end_date, total_absent_days))

# Create DataFrame for results
result_df = pd.DataFrame(absent_streaks, columns=['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days'])

# Join with students data
result_df = result_df.merge(students_df, on='student_id', how='left')

# Validate emails
def validate_email(email):
    if pd.isna(email):
        return False
    if not isinstance(email, str):
        return False
    if email.count('@') != 1 or email.startswith(tuple('0123456789')):
        return False
    local_part, domain = email.split('@')
    if not local_part.replace('_', '').isalnum() or not domain.isalnum():
        return False
    return True

result_df['valid_email'] = result_df['parent_email'].apply(validate_email)

#add msg column
result_df['msg'] = result_df['valid_email'].apply(lambda x: 'Valid parent email' if x else 'none')

#format dates
result_df['absence_start_date'] = result_df['absence_start_date'].dt.strftime('%d-%m-%Y')
result_df['absence_end_date'] = result_df['absence_end_date'].dt.strftime('%d-%m-%Y')

#select final
final_output = result_df[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'parent_email', 'msg']]

#to show putput
print(final_output)
