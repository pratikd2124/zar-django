from collections import defaultdict
from datetime import datetime, timedelta, timezone
import os
import ast

LOG_DIR = '/home/ubuntu/zar-django/logs/user_activity'  # Update with your log folder path

def parse_log_file(filepath):
    activity_data = []
    
    with open(filepath, 'r') as file:
        for line in file:
            try:
                log_info = ast.literal_eval(line.strip())  # Parse the log line safely
                timestamp = datetime.fromisoformat(log_info['time_visited'])
                user_id = log_info['user']
                page_visited = log_info['path']
                activity_data.append({'user': user_id, 'page_visited': page_visited, 'timestamp': timestamp})
            except Exception as e:
                print(f"Error parsing line in file {filepath}: {line.strip()} - {e}")
                continue
    return activity_data

def get_all_user_activity_logs():
    all_logs = []
    for filename in os.listdir(LOG_DIR):
        filepath = os.path.join(LOG_DIR, filename)
        if os.path.isfile(filepath):
            all_logs.extend(parse_log_file(filepath))
    return all_logs

def analyze_user_activity_from_logs():
    logs = get_all_user_activity_logs()

    now = datetime.now(timezone.utc)  # Use UTC timezone
    
    # Monthly active users for the past 90 days
    monthly_active_users_list = defaultdict(set)  # Use a set to ensure unique users
    for log in logs:
        timestamp = log['timestamp']
        if timestamp >= now - timedelta(days=90):
            month = timestamp.strftime('%Y-%m')
            monthly_active_users_list[month].add(log['user'])  # Add unique user to the set for the month

    # Last week's active users
    last_week_active_users_list = defaultdict(set)  # Use a set to ensure unique users
    one_week_ago = now - timedelta(days=7)
    for log in logs:
        timestamp = log['timestamp']
        if timestamp >= one_week_ago:
            day = timestamp.strftime('%A')
            last_week_active_users_list[day].add(log['user'])  # Add unique user to the set for the day

    # Category-wise visited users
    category_wise_visited_users_count = defaultdict(set)  # Use a set to ensure unique users per category
    for log in logs:
        category = log['page_visited']  # Assuming page_visited corresponds to a category
        category_wise_visited_users_count[category].add(log['user'])  # Add unique user to the set for the category

    # Convert sets to their lengths (count of unique users)
    monthly_active_users_count = {month: len(users) for month, users in monthly_active_users_list.items()}
    last_week_active_users_count = {day: len(users) for day, users in last_week_active_users_list.items()}
    category_wise_users_count = {category: len(users) for category, users in category_wise_visited_users_count.items()}

    return (
        monthly_active_users_count,  # Monthly active users data
        last_week_active_users_count,  # Weekly active users data
        category_wise_users_count  # Category-wise unique user visits
    )
