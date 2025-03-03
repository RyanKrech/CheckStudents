import csv
import sys

file1 = sys.argv[1]  

def check_ip_with_multiple_users(file_path):
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
            
        # Identify IPs that have multiple users
        ip_with_multiple_users = {ip: users for ip, users in ip_users.items() if len(users) > 1}

        return ip_with_multiple_users
    
    except Exception as e:
        print(f"Error reading the file: {e}")
        return {}

ip_with_multiple_users = check_ip_with_multiple_users(file1)

# Write the output to a CSV file
output_file = "output_ips_with_multiple_users.csv"

with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerow(["IP Address", "Users"])  # Write the header

    if ip_with_multiple_users:
        for ip, users in ip_with_multiple_users.items():
            writer.writerow([ip, ', '.join(users)])  # Write the IP with associated users

print(f"Output has been written to {output_file}")
