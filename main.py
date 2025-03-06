import re
import json
import datetime

USERS_DATA = "users.json"
PROJECTS_DATA = "projects.json"

def load_data(filename):
    file = open(filename)
    return json.load(file)
    

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def validate_egyptian_phone(phone):
    return re.match(r"^01[0-2,5]{1}[0-9]{8}$", phone)

def register():
    print("\n============ User Registration ===============")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Email: ")
    password = input("Password: ")
    confirm_password = input("Confirm password: ")
    phone = input("Mobile Phone: ")
    
    if password != confirm_password:
        print("Passwords do not match!")
        return
    
    if not validate_egyptian_phone(phone):
        print("Invalid phone number!")
        return
    
    users = load_data(USERS_DATA)
    for user in users:
        if user['email'] == email:
            print("Email already registered!")
            return
    
    users.append({"first_name": first_name, "last_name": last_name, "email": email, "password": password, "phone": phone})
    save_data(USERS_DATA, users)
    print("Successfully registered!")

def login():
    print("\n======== User Login ========")
    email = input("Email: ")
    password = input("Password: ")
    
    users = load_data(USERS_DATA)
    for user in users:
        if user['email'] == email and user['password'] == password:
            print(f"Welcome, {user['first_name']}!")
            return user
    print("Invalid email or password!")
    return None

def create_project(user):
    print("\n======== Create Project =========")
    title = input("Project title: ")
    details = input("Details: ")
    total_target = input("Total target: ")
    start_date = input("Start date: ")
    end_date = input("End date: ")
    
    try:
        datetime.datetime.strptime(start_date, "%Y-%m-%d")
        datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format!")
        return
    
    projects = load_data(PROJECTS_DATA)
    projects.append({"owner": user['email'], "title": title, "details": details, "target": total_target, "start_date": start_date, "end_date": end_date})
    save_data(PROJECTS_DATA, projects)
    print("Project created successfully.")

def view_projects():
    print("\n======== All Projects ========")
    projects = load_data(PROJECTS_DATA)
    for idx, project in enumerate(projects, 1):
        print(f"[{idx}] {project['title']} - {project['details']} (Target: {project['target']} EGP, Start: {project['start_date']}, End: {project['end_date']})")

def edit_project(user):
    projects = load_data(PROJECTS_DATA)
    user_projects = [p for p in projects if p['owner'] == user['email']]
    
    if not user_projects:
        print("You have no projects to edit.")
        return
    
    view_projects()
    idx = int(input("Enter project number to edit: ")) - 1
    if idx < 0 or idx >= len(user_projects):
        print("Invalid selection!")
        return
    
    project = user_projects[idx]
    project['title'] = input(f"New title ({project['title']}): ") or project['title']
    project['details'] = input(f"New details ({project['details']}): ") or project['details']
    project['target'] = input(f"New target ({project['target']} EGP): ") or project['target']
    save_data(PROJECTS_DATA, projects)
    print("Project updated successfully!")

def delete_project(user):
    projects = load_data(PROJECTS_DATA)
    user_projects = [p for p in projects if p['owner'] == user['email']]
    
    if not user_projects:
        print("You have no projects to delete.")
        return
    
    view_projects()
    idx = int(input("Enter project number to delete: ")) - 1
    if idx < 0 or idx >= len(user_projects):
        print("Invalid selection!")
        return
    
    projects.remove(user_projects[idx])
    save_data(PROJECTS_DATA, projects)
    print("Project deleted successfully!")

def search_project_by_date():
    date = input("Enter project start date to search: ")
    projects = load_data(PROJECTS_DATA)
    found = [p for p in projects if p['start_date'] == date]
    
    if found:
        for project in found:
            print(f"{project['title']} - {project['details']} (Target: {project['target']} EGP)")
    else:
        print("No projects found on this date.")

def main():
    while True:
        print("\nCrowd funding console app")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                while True:
                    print("\n1. Create project")
                    print("2. View projects")
                    print("3. Edit my project")
                    print("4. Delete my project")
                    print("5. Search project by Date")
                    print("6. Logout")
                    option = input("Enter choice: ")
                    if option == "1":
                        create_project(user)
                    elif option == "2":
                        view_projects()
                    elif option == "3":
                        edit_project(user)
                    elif option == "4":
                        delete_project(user)
                    elif option == "5":
                        search_project_by_date()
                    elif option == "6":
                        break
        elif choice == "3":
            print("Loged out.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
