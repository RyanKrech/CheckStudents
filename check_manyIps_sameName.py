import csv
import sys
from datetime import datetime, time

# Function to check user logins with multiple IPs and filter by time range
def check_user_with_multiple_ips(file_path, start_time_str, end_time_str):
    user_ips = {}
    user_login_times = {}  # Stores first and last login times per user and date
    total_rows = 0
    successfully_parsed_rows = 0
    rows_with_missing_data = []  # Track rows with missing data

    try:
        # Convert time range strings into time objects
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

            # Iterate through the rows
            for row in reader:
                if len(row) < 9:  # Ensure the row has enough columns
                    continue

                total_rows += 1
                timestamp_str = row[0]  # The timestamp is in the first column
                user = row[1]  # The user's full name is in the second column
                ip = row[8]  # The IP address is in the ninth column

                # Parse timestamp with day/month/year, hour:minute:second format
                try:
                    timestamp = datetime.strptime(timestamp_str, "%d/%m/%y, %H:%M:%S") if timestamp_str else None
                    login_date = timestamp.date() if timestamp else None  # Get only the date (day/month/year)
                    login_time = timestamp.time() if timestamp else None  # Get the time (hour:minute:second)
                except ValueError:
                    timestamp = None
                    login_date = None
                    login_time = None
                    print(f"Skipping row (invalid timestamp format): {row}")

                # Filter rows based on time range
                if ip and user and login_date and login_time:  # Ensure IP, User, and login_date are present
                    if start_time <= login_time <= end_time:  # Check if the login time is within the given range
                        successfully_parsed_rows += 1
                        if user not in user_ips:
                            user_ips[user] = {}
                            user_login_times[user] = {}

                        if login_date not in user_ips[user]:
                            user_ips[user][login_date] = set()
                            user_login_times[user][login_date] = {"first_login": timestamp, "last_login": timestamp}

                        user_ips[user][login_date].add(ip)

                        # Update first and last login times
                        if timestamp and (not user_login_times[user][login_date]["first_login"] or timestamp < user_login_times[user][login_date]["first_login"]):
                            user_login_times[user][login_date]["first_login"] = timestamp
                        if timestamp and (not user_login_times[user][login_date]["last_login"] or timestamp > user_login_times[user][login_date]["last_login"]):
                            user_login_times[user][login_date]["last_login"] = timestamp
                    else:
                        # Skip this row if the login time is not in the given range
                        continue
                else:
                    rows_with_missing_data.append(row)  # Track rows with missing data

        print(f"Total rows in the file: {total_rows}")
        print(f"Successfully parsed rows: {successfully_parsed_rows}")

        if total_rows != successfully_parsed_rows:
            print("Warning: Not all rows were parsed successfully.")

        if rows_with_missing_data:
            print(f"Rows with missing data: {len(rows_with_missing_data)}")
            for missing_data_row in rows_with_missing_data:
                print(f"Missing data in row: {missing_data_row}")

        # Identify users with multiple IP addresses on the same day
        user_with_multiple_ips_on_same_day = {
            user: {date: ips for date, ips in dates.items() if len(ips) > 1}
            for user, dates in user_ips.items()
        }

        # Filter out users who don't have multiple IPs on the same day
        user_with_multiple_ips_on_same_day = {
            user: dates for user, dates in user_with_multiple_ips_on_same_day.items() if dates
        }

        return user_with_multiple_ips_on_same_day, user_login_times

    except Exception as e:
        print(f"Error reading the file: {e}")
        return {}, {}

# Main function to execute the script
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python process_logins.py <file_path> <start_time> <end_time>")
        sys.exit(1)

    file_path = sys.argv[1]
    start_time_str = sys.argv[2]
    end_time_str = sys.argv[3]

    # Get users with multiple IP addresses on the same day filtered by time range
    user_with_multiple_ips_on_same_day, user_login_times = check_user_with_multiple_ips(file_path, start_time_str, end_time_str)

    # Write the output to a CSV file
    output_file = "output_users_with_multiple_ips_and_logins_same_day_filtered.csv"

    with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(["User Full Name", "Login Date", "IP Addresses", "First Login Time", "Last Login Time"])  # Write the header

        # Write users with multiple IPs on the same day along with first and last login times
        if user_with_multiple_ips_on_same_day:
            for user, dates in user_with_multiple_ips_on_same_day.items():
                for login_date, ips in dates.items():
                    first_login = user_login_times[user][login_date]["first_login"].strftime("%Y-%m-%d %H:%M:%S") if user_login_times[user][login_date]["first_login"] else "N/A"
                    last_login = user_login_times[user][login_date]["last_login"].strftime("%Y-%m-%d %H:%M:%S") if user_login_times[user][login_date]["last_login"] else "N/A"
                    writer.writerow([user, login_date.strftime("%d/%m/%y"), ', '.join(ips), first_login, last_login])  # Write the user with associated IPs, login date, and login times

    print(f"Output has been written to {output_file}")