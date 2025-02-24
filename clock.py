from tkinter import *
from tkinter import messagebox
import time
import winsound  # For sound on Windows

# Initialize the main window
root = Tk()
root.title("Timer")
root.geometry("400x600")
root.configure(bg="#000")
root.resizable(False, False)

# Heading
heading = Label(root, text="Timer", font="arial 30 bold", bg="#000", fg="#ea3548")
heading.pack(pady=16)

# Label for displaying current time
Label(root, font=("arial", 15, "bold"), text="Current Time", bg="papaya whip").place(x=65, y=70)


# Function to display the current time
def clock():
    clock_time = time.strftime('%H:%M:%S %p')
    current_time.config(text=clock_time)
    current_time.after(1000, clock)


current_time = Label(root, font=("arial", 15, "bold"), text="", fg="#000", bg="#fff")
current_time.place(x=190, y=70)
clock()


# Entry fields for hours, minutes, and seconds
hrs = StringVar()
mins = StringVar()
secs = StringVar()

Entry(root, textvariable=hrs, width=2, font="arial 50", bg="#000", fg="#fff", bd=0).place(x=30, y=155)
hrs.set("00")

Entry(root, textvariable=mins, width=2, font="arial 50", bg="#000", fg="#fff", bd=0).place(x=150, y=155)
mins.set("00")

Entry(root, textvariable=secs, width=2, font="arial 50", bg="#000", fg="#fff", bd=0).place(x=270, y=155)
secs.set("00")

# Labels for hours, minutes, and seconds
Label(root, text="hours", font="arial 12", bg="#000", fg="#fff").place(x=105, y=200)
Label(root, text="min", font="arial 12", bg="#000", fg="#fff").place(x=225, y=200)
Label(root, text="sec", font="arial 12", bg="#000", fg="#fff").place(x=345, y=200)

# Global variable to control timer state
timer_running = False
paused = False
remaining_time = 0
timer_id = None  # To store the after() timer event


# Call function when time is up


# Function to move focus automatically after 2 digits are entered


# Function to handle what happens when the timer finishes
def validate_inputs():
    # Check if all inputs are numeric
    if not (hrs.get().isdigit() and mins.get().isdigit() and secs.get().isdigit()):
        messagebox.showerror("Invalid Input", "Please enter only numeric values.")
        return False

    # Validate the range of the numeric inputs
    try:
        hours = int(hrs.get())
        minutes = int(mins.get())
        seconds = int(secs.get())

        if hours == 0 and minutes == 0 and seconds == 0:
            messagebox.showerror("Invalid Input", "Please enter a time greater than zero.")
            return False
        # Check if hours are within the valid range (0-23)
        if not (0 <= hours <= 23):
            messagebox.showerror("Invalid Input", "Please enter a valid hour (0-23).")
            return False

        # Check if minutes are within the valid range (0-59)
        if not (0 <= minutes <= 59):
            messagebox.showerror("Invalid Input", "Please enter a valid minute (0-59).")
            return False

        # Check if seconds are within the valid range (0-59)
        if not (0 <= seconds <= 59):
            messagebox.showerror("Invalid Input", "Please enter a valid second (0-59).")
            return False

        return True  # If all checks pass, return True
    except ValueError:
        # If the conversion to int fails
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")
        return False


# Timer logic

def Timer():
    global remaining_time, timer_running, paused
    if not validate_inputs():
        return

    if timer_running:
        return  # Prevent multiple timers from running

    # Convert input time into total seconds
    times = int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(secs.get())
    remaining_time = times
    timer_running = True
    paused = False
    countdown(remaining_time)


def play_sound():
    frequency = 1000  # Set Frequency To 1000 Hertz
    duration = 1000   # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)


def countdown(times):
    global remaining_time, timer_running, paused, timer_id
    if times > 0 and not paused:
        minute, second = divmod(times, 60)
        hour = 0
        if minute >= 60:
            hour, minute = divmod(minute, 60)

        # Update the time values in the input fields
        secs.set(f"{second:02}")
        mins.set(f"{minute:02}")
        hrs.set(f"{hour:02}")

        remaining_time = times
        timer_id = root.after(1000, countdown, times - 1)  # Update every second
    else:
        if times == 0:
            play_sound()  # Play sound when time is up
            messagebox.showinfo("Time's up!", "The countdown has finished!")
            # Reset the timer state
            timer_running = False
            paused = False
            # Optionally set fields to 00:00:00
            secs.set("00")
            mins.set("00")
            hrs.set("00")


# Timer control functions
def pause_timer():
    global paused
    paused = True


def resume_timer():
    global paused
    paused = False
    countdown(remaining_time)


def stop_timer():
    global timer_running, paused, timer_id
    if timer_id:
        root.after_cancel(timer_id)  # Cancel the running after() event
    timer_running = False
    paused = False
    hrs.set("00")
    mins.set("00")
    secs.set("00")



# Preset functions for brushing, face care, and cooking eggs
def brush():
    hrs.set("00")
    mins.set("02")
    secs.set("00")


def face():
    hrs.set("00")
    mins.set("15")
    secs.set("00")


def eggs():
    hrs.set("00")
    mins.set("10")
    secs.set("00")


# Create a Canvas for the circular buttons at the bottom
canvas = Canvas(root, width=400, height=100, bg="#000", highlightthickness=0)
canvas.pack(side=BOTTOM, pady=20)  # Pack at the bottom with padding


# Create circular buttons with the Canvas widget
def create_circular_button(canvas, x, y, label, command):
    circle = canvas.create_oval(x - 35, y - 35, x + 35, y + 35, fill="#ea3548")
    button = Button(root, text=label, width=5, height=2, bg="#ea3548", bd=0, fg="#fff", command=command)
    canvas.create_window(x, y, window=button)


# Place buttons in a horizontal circular line at the bottom
create_circular_button(canvas, 60, 50, "Start", Timer)
create_circular_button(canvas, 140, 50, "Pause", pause_timer)
create_circular_button(canvas, 220, 50, "Resume", resume_timer)
create_circular_button(canvas, 300, 50, "Stop", stop_timer)

# Preset image buttons for quick selection
Image1 = PhotoImage(file="brush.png")
button1 = Button(root, image=Image1, bg="#000", bd=0, command=brush)
button1.place(x=7, y=300)

Image2 = PhotoImage(file="face.png")
button2 = Button(root, image=Image2, bg="#000", bd=0, command=face)
button2.place(x=137, y=300)

Image3 = PhotoImage(file="eggs.png")
button3 = Button(root, image=Image3, bg="#000", bd=0, command=eggs)
button3.place(x=267, y=300)

# Run the main loop
root.mainloop()
