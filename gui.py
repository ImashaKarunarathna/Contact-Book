import tkinter as tk
from tkinter import messagebox
import json

# Contact Book class to manage the contacts
class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("400x500")  # Set the window size
        self.root.config(bg="#FFC0CB")  # Light pink background color

        # Initialize contacts dictionary
        self.contacts = {}
        self.load_contacts()  # Load contacts from file

        # Title Label
        self.title_label = tk.Label(root, text="Contact Book", font=("Arial", 48, "bold","italic"), bg="#FFC0CB", pady=10, fg="#FF69B4")
        self.title_label.pack()

        # Frame to hold the entry fields and labels
        self.frame = tk.Frame(root, bg="#FFC0CB")
        self.frame.pack(pady=10)

        # GUI Elements
        self.name_label = tk.Label(self.frame, text="Name:", font=("Arial", 12), bg="#FF69B4", fg="black")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(self.frame, font=("Arial", 12), width=25)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.phone_label = tk.Label(self.frame, text="Phone Number:", font=("Arial", 12), bg="#FF69B4", fg="black")
        self.phone_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.phone_entry = tk.Entry(self.frame, font=("Arial", 12), width=25)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        self.email_label = tk.Label(self.frame, text="Email:", font=("Arial", 12), bg="#FF69B4", fg="black")
        self.email_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), width=25)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        self.address_label = tk.Label(self.frame, text="Address:", font=("Arial", 12), bg="#FF69B4", fg="black")
        self.address_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.address_entry = tk.Entry(self.frame, font=("Arial", 12), width=25)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons Frame
        self.button_frame = tk.Frame(root, bg="#FFC0CB")
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Contact", command=self.add_contact, font=("Arial", 12), bg="#FF69B4", fg="black")
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.view_button = tk.Button(self.button_frame, text="View Contacts", command=self.view_contacts, font=("Arial", 12), bg="#FF69B4", fg="black")
        self.view_button.grid(row=0, column=1, padx=5, pady=5)

        self.search_label = tk.Label(root, text="Search by Name or Phone", font=("Arial", 12), bg="#FFC0CB", fg="black")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(root, font=("Arial", 12), width=25)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(root, text="Search", command=self.search_contact, font=("Arial", 12), bg="#FF69B4", fg="black")
        self.search_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Contact", command=self.update_contact, font=("Arial", 12), bg="#FF69B4", fg="black")
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact, font=("Arial", 12), bg="#FF69B4", fg="black")
        self.delete_button.pack(pady=5)

        # Listbox to display contacts
        self.contact_listbox = tk.Listbox(root, font=("Arial", 12 ," bold"), width=40, height=10, bg="#FFC0CB", fg="#FF69B4")
        self.contact_listbox.pack(pady=10)
        self.update_contact_listbox()

    # Function to add a new contact
    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            self.contacts[name] = {'Phone': phone, 'Email': email, 'Address': address}
            self.save_contacts()  # Save the updated contacts
            self.update_contact_listbox()
            messagebox.showinfo("Success", "Contact added successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Name and Phone Number are required!")

    # Function to view all contacts
    def view_contacts(self):
        self.update_contact_listbox()

    # Function to search for a contact
    def search_contact(self):
        search_term = self.search_entry.get()
        self.contact_listbox.delete(0, tk.END)
        found_contacts = [f"{name}: {details['Phone']}" for name, details in self.contacts.items()
                          if search_term.lower() in name.lower() or search_term in details['Phone']]

        if found_contacts:
            for contact in found_contacts:
                self.contact_listbox.insert(tk.END, contact)
        else:
            messagebox.showinfo("Search Results", "No contacts found.")

    # Function to update a contact
    def update_contact(self):
        name = self.name_entry.get()
        if name in self.contacts:
            self.contacts[name]['Phone'] = self.phone_entry.get()
            self.contacts[name]['Email'] = self.email_entry.get()
            self.contacts[name]['Address'] = self.address_entry.get()
            self.save_contacts()  # Save the updated contacts
            self.update_contact_listbox()
            messagebox.showinfo("Success", "Contact updated successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Contact not found.")

    # Function to delete a contact
    def delete_contact(self):
        name = self.name_entry.get()
        if name in self.contacts:
            del self.contacts[name]
            self.save_contacts()  # Save the updated contacts
            self.update_contact_listbox()
            messagebox.showinfo("Success", "Contact deleted successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Contact not found.")

    # Function to clear the entry fields
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    # Function to update the contact listbox
    def update_contact_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        for name, details in self.contacts.items():
            self.contact_listbox.insert(tk.END, f"{name}: {details['Phone']}")

    # Function to save contacts to a file
    def save_contacts(self):
        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file)

    # Function to load contacts from a file
    def load_contacts(self):
        try:
            with open("contacts.json", "r") as file:
                self.contacts = json.load(file)
        except FileNotFoundError:
            self.contacts = {}

# Create the main window and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
