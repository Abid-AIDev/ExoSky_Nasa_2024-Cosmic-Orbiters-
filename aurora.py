from customtkinter import *
import subprocess
import threading  # To handle the subprocess in a non-blocking way
import time

def btn():
    data = entry.get()  # Get the input from the entry
    if data:
        textbox.insert(END, f"You: {data}\n")  # Show user input
        entry.delete(0, END)  # Clear the entry after getting input
        threading.Thread(target=ollama, args=(data,)).start()  # Call the ollama function in a new thread

def exit():
    app.destroy()

def animate_text(text):
    for char in text:
        textbox.insert(END, char)  # Insert one character at a time
        textbox.see(END)  # Scroll to the end of the textbox
        textbox.update()  # Update the textbox to reflect the new character
        time.sleep(0.05)  # Delay for animation (adjust as necessary)

def ollama(input_data):
    executable_path = '/usr/local/bin/ollama'  # Change this to your executable path

    # Start the subprocess with the executable
    process = subprocess.Popen(
        [executable_path, 'run', 'llama3.1'],  # Modify arguments as needed
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Enables text mode for input/output
        bufsize=1  # Line buffering for real-time output
    )

    # Send input to the executable
    process.stdin.write(input_data + "\n")
    process.stdin.flush()  # Ensure input is sent
    process.stdin.close()  # Close the stdin to indicate end of input

    # Read stdout line by line for real-time updates
    for line in process.stdout:
        # Call the animation function for each line of output
        animate_text(f"{line.strip()}\n")  # Strip newlines and animate the output

    # Wait for the process to complete and close the output
    process.stdout.close()
    process.wait()

# Tkinter setup
app = CTk()
app.title("Aurora")
app.geometry('1200x700')

label = CTkLabel(master=app, text="Aurora AI", font=("Arial", 40), text_color="lightblue")
label.place(relx=0.02, rely=0.05, anchor="nw")

textbox = CTkTextbox(master=app, scrollbar_button_color="#FFCC70", corner_radius=16,
                     border_color="white", border_width=1, width=900, height=570)
textbox.place(relx=0.22, rely=0.87, anchor="sw")

entry = CTkEntry(master=app, placeholder_text="Start typing...", width=700, height=40, text_color="#FFC700")
entry.place(relx=0.24, rely=0.97, anchor="sw")

btn = CTkButton(master=app, text="Enter", corner_radius=12, height=40, width=120, fg_color='#1E88E5', hover_color='#1976D2', command=btn)
btn.place(anchor="sw", relx=0.86, rely=0.97)

btn1 = CTkButton(master=app, text="Exit", corner_radius=12, height=40, width=120, fg_color='#FF7043', hover_color='#F4511E', command=exit)
btn1.place(anchor="sw", relx=0.02, rely=0.97)

app.mainloop()