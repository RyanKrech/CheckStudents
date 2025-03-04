import csv
import sys

def check_ip_with_multiple_users(file_path, exclude_file):
    ip_users = {}
    total_rows = 0 
    successfully_parsed_rows = 0  

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            required_columns = ["IP address", "User full name"]
            if not all(col in reader.fieldnames for col in required_columns):
                print("Error: CSV file is missing required columns.")
                return {}

            for row in reader:
                if not row:
                    continue
                
                total_rows += 1
                ip = row.get("IP address")
                user = row.get("User full name")
                
                if ip and user:
                    successfully_parsed_rows += 1
                    if ip not in ip_users:
                        ip_users[ip] = set()
                    ip_users[ip].add(user)
                else:
                    print(f"Skipping row (missing IP or user): {row}")

        print(f"Total rows in the file: {total_rows}")
        print(f"Successfully parsed rows: {successfully_parsed_rows}")
        
        if total_rows != successfully_parsed_rows:
            print("Warning: Not all rows were parsed successfully.")
        else:
            print("All rows were parsed successfully.")
            
        # Read IPs from the second file
        exclude_ips = set()
        try:
            with open(exclude_file, mode='r', newline='', encoding='utf-8') as ex_file:
                reader = csv.reader(ex_file)
                exclude_ips = {row[0] for row in reader if row}
        except Exception as e:
            print(f"Error reading the exclude file: {e}")
            return {}
        
        # Identify IPs that are NOT in the second file
        ip_not_in_second_file = {ip: users for ip, users in ip_users.items() if ip not in exclude_ips}

        return ip_not_in_second_file
    
    except Exception as e:
        print(f"Error reading the file: {e}")
        return {}

if len(sys.argv) < 3:
    print("Usage: python script.py <file1.csv> <file2.csv>")
    sys.exit(1)

file1 = sys.argv[1]  # First CSV file containing IPs and usernames
file2 = sys.argv[2]  # Second CSV file containing only IPs to exclude

ip_not_in_second_file = check_ip_with_multiple_users(file1, file2)

# Write the output to a CSV file
output_file = "output_ips_not_in_second_file.csv"

with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerow(["IP Address", "Users"])  # Write the header

    if ip_not_in_second_file:
        for ip, users in ip_not_in_second_file.items():
            writer.writerow([ip, ', '.join(users)])  # Write the IP with associated users

print(f"Output has been written to {output_file}")
