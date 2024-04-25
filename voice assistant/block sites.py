import os

def block_website(website):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    redirect = "127.0.0.1"
    with open(hosts_path, "a") as file:
        file.write(f"\n{redirect} {website}")

    return (print(f"Сайт {website} был заблокирован"))

def unblock_website(website):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    with open(hosts_path, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(website in line for website in website):
                file.write(line)
        file.truncate()

    return (print(f"Сайт {website} был разблокирован"))
