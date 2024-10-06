from customtkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import webbrowser
from PIL import Image, ImageTk

def explore():
    # Create a new window for planet names
    planet_window = CTkToplevel(app)
    planet_window.title("Planet Names")
    planet_window.geometry('1280x720')

    # Read the exoplanet data from the CSV file
    try:
        exoplanet_data = pd.read_csv('exo.csv')

        # Assuming the planet names are in a column named 'pl_name'
        planet_names = exoplanet_data['pl_name'].unique()  # Get unique planet names

        # Create a textbox for displaying planet names
        label = CTkLabel(master=planet_window, text="List of all ExoPlanets", font=("Arial", 40), text_color="lightblue")
        label.place(relx=0.1, rely=0.02, anchor="nw")
        textbox = CTkTextbox(master=planet_window, scrollbar_button_color="#FFCC70", font=("Arial", 20), corner_radius=16, border_color="white", border_width=1, width=1100, height=570)
        textbox.place(relx=0.05, rely=0.9, anchor="sw")

        # Insert all planet names into the textbox
        for name in planet_names:
            textbox.insert("end", name + "\n")  # Add each name on a new line

    except FileNotFoundError:
        error_label = CTkLabel(master=planet_window, text="Error: 'exo.csv' file not found!", font=("Arial", 16))
        error_label.pack(pady=20)

def linknasa():
    # Open the NASA website or a specific NASA page
    webbrowser.open("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS") 

def run_test_file():
    os.system('python3 aurora.py')

def run_test_file1():
    os.system('python3 map.py')

def analyze_gaia_data():
    # Create a new window for Gaia data analysis
    gaia_window = CTkToplevel(app)
    gaia_window.title("Gaia Data Analysis")
    gaia_window.geometry('800x600')

    # Label explaining what Gaia is
    gaia_info = CTkLabel(master=gaia_window, text="\nGaia is a space observatory launched by the European Space Agency to create a three-dimensional map of our galaxy, the Milky Way, by observing and measuring the positions, distances, and motions of stars with unprecedented precision.\n", 
                          font=("Arial", 19), wraplength=700)
    gaia_info.pack(pady=8)

    # Checkbox for selecting graph types
    graph_types = [
        'Distribution of Planet Mass (Jupiter Mass)',
        'Planet Mass vs Radius',
        'Distribution of Orbital Period (days)',
        'Correlation Heatmap of Stellar Properties',
        'Stellar Mass vs Stellar Radius',
        'Boxplot of Eccentricity Values',
        'Distribution of Stellar Effective Temperature',
        'Scatter Plot of Planet Mass vs Orbital Period',
        'Joint Plot of Mass and Radius',
        'Violin Plot of Stellar Temperature',
        'Pair Plot of Stellar Properties',
        'Bar Plot of Average Planet Mass per Star',
        'Facet Grid of Orbital Period by Planet Count'
    ]

    selected_graphs = []

    def toggle_graph_selection(var, graph_name):
        if var.get():
            selected_graphs.append(graph_name)
        else:
            selected_graphs.remove(graph_name)

    check_vars = []
    for graph in graph_types:
        var = IntVar()
        check_vars.append(var)
        check = CTkCheckBox(master=gaia_window, text=graph, variable=var, command=lambda v=var, g=graph: toggle_graph_selection(v, g))
        check.pack(anchor='w',padx=5,pady=5)

    def generate_graphs():
        # Load your dataset (assuming a CSV or similar file)
        try:
            data = pd.read_csv('gaia.csv')
            sns.set(style="whitegrid")

            # Filter relevant columns based on actual dataset column names
            columns_of_interest = [
                'sy_snum', 'sy_pnum', 'pl_massj', 
                'pl_radj', 'pl_orbper', 'st_mass', 
                'st_rad', 'st_teff', 'pl_orbeccen'
            ]

            # Drop any missing data rows for simplicity
            data_filtered = data[columns_of_interest].dropna()

            # Create a mapping from graph title to plotting function
            graph_functions = {
                'Distribution of Planet Mass (Jupiter Mass)': lambda: sns.histplot(data_filtered['pl_massj'], kde=True, color='skyblue'),
                'Planet Mass vs Radius': lambda: sns.scatterplot(x='pl_massj', y='pl_radj', data=data_filtered),
                'Distribution of Orbital Period (days)': lambda: sns.histplot(data_filtered['pl_orbper'], kde=True, color='coral'),
                'Correlation Heatmap of Stellar Properties': lambda: sns.heatmap(data_filtered[['st_mass', 'st_rad', 'st_teff', 'pl_orbeccen']].corr(), annot=True, cmap='coolwarm'),
                'Stellar Mass vs Stellar Radius': lambda: sns.scatterplot(x='st_mass', y='st_rad', data=data_filtered, hue='pl_orbeccen'),
                'Boxplot of Eccentricity Values': lambda: sns.boxplot(data=data_filtered, x='pl_orbeccen'),
                'Distribution of Stellar Effective Temperature': lambda: sns.histplot(data_filtered['st_teff'], kde=True, color='green'),
                'Scatter Plot of Planet Mass vs Orbital Period': lambda: sns.scatterplot(x='pl_massj', y='pl_orbper', data=data_filtered),
                'Joint Plot of Mass and Radius': lambda: sns.jointplot(x='pl_massj', y='pl_radj', data=data_filtered, kind='scatter', color='orange'),
                'Violin Plot of Stellar Temperature': lambda: sns.violinplot(data=data_filtered, x='st_teff', color='purple'),
                'Pair Plot of Stellar Properties': lambda: sns.pairplot(data_filtered[['st_mass', 'st_rad', 'st_teff', 'pl_orbeccen']], diag_kind='kde'),
                'Bar Plot of Average Planet Mass per Star': lambda: sns.barplot(x='sy_snum', y='pl_massj', data=data_filtered.groupby('sy_snum').mean().reset_index(), palette='viridis'),
                'Facet Grid of Orbital Period by Planet Count': lambda: sns.FacetGrid(data_filtered, col='sy_pnum', col_wrap=4).map(sns.histplot, 'pl_orbper')
            }

            # Generate the selected plots
            for graph_name in selected_graphs:
                plt.figure(figsize=(8, 6))
                graph_functions[graph_name]()
                plt.title(graph_name)
                plt.show()

        except FileNotFoundError:
            label = CTkLabel(master=gaia_window, text="CSV file 'gaia.csv' not found!", font=("Arial", 20), text_color="red")
            label.place(relx=0.5, rely=0.5, anchor="center")


    # Button to generate the selected graphs
    generate_button = CTkButton(master=gaia_window, text="Generate Graphs", font=("Arial", 20), corner_radius=12, height=72, width=190,command=generate_graphs)
    generate_button.place(relx=0.7, rely=0.83)
def graph():
    # Create a new window for graph selection
    graph_window = CTkToplevel(app)
    graph_window.title("Graph Selection")
    graph_window.geometry('600x500')

    label = CTkLabel(master=graph_window, text="Select a program for graphing", font=("Arial", 20))
    label.place(relx=0.5, rely=0.1, anchor="center")
    
    # ComboBox for x-axis program selection
    programs = ["No.of stars", "No. of Planets", "Discovery Year", "Orbital Period", 'Stellar effective Temparature',
                'Stellar radius', 'Stellar surface gravity', 'distance', 'Gaia Magnitude', 'releasedate']
    label1 = CTkLabel(master=graph_window, text="Choose X-axis:", font=("Arial", 15))
    label1.place(relx=0.5, rely=0.2, anchor="center")
    combo_box_x = CTkComboBox(master=graph_window, values=programs, width=200, height=30)
    combo_box_x.place(relx=0.5, rely=0.3, anchor="center")

    # ComboBox for y-axis program selection
    label2 = CTkLabel(master=graph_window, text="Choose y-axis:", font=("Arial", 15))
    label2.place(relx=0.5, rely=0.4, anchor="center")
    combo_box_y = CTkComboBox(master=graph_window, values=programs, width=200, height=30)
    combo_box_y.place(relx=0.5, rely=0.5, anchor="center")

    # ComboBox for chart type selection
    label2 = CTkLabel(master=graph_window, text="Choose graph type:", font=("Arial", 15))
    label2.place(relx=0.5, rely=0.6, anchor="center")
    chart_types = ["Scatter Plot", "Line Plot", "Histogram", "Box Plot"]
    combo_chart = CTkComboBox(master=graph_window, values=chart_types, width=200, height=30)
    combo_chart.place(relx=0.5, rely=0.7, anchor="center")

    # ComboBox for planet selection
    try:
        exo = pd.read_csv('exo.csv')  # Load the CSV file
        planets = exo['pl_name'].unique()  # Get unique planet names from the CSV
    except FileNotFoundError:
        print("CSV file not found!")
        planets = []

    # Function to handle the selected program and generate the graph
    def on_program_select():
        selected_x = combo_box_x.get()
        selected_y = combo_box_y.get()
        selected_chart = combo_chart.get()
        selected_planet = entry.get()

        if selected_x and selected_y and selected_chart and selected_planet:
            try:
                exo = pd.read_csv('exo.csv')

                if selected_x in exo.columns and selected_y in exo.columns:
                    x_data = exo[selected_x]
                    y_data = exo[selected_y]

                    plt.figure(figsize=(8, 6))

                    # Plot the graph based on the selected chart type
                    if selected_chart == "Scatter Plot":
                        sns.scatterplot(x=x_data, y=y_data, color='blue', label="Data Points")
                    elif selected_chart == "Line Plot":
                        sns.lineplot(x=x_data, y=y_data, color='green', label="Data Points")
                    elif selected_chart == "Histogram":
                        sns.histplot(x=x_data, y=y_data, bins=20, kde=True, color='purple', label="Data Points")
                    elif selected_chart == "Box Plot":
                        sns.boxplot(x=x_data, y=y_data, palette="coolwarm")

                    # Highlight the selected planet's data point
                    planet_row = exo[exo['pl_name'] == selected_planet]  # Find row with selected planet
                    if not planet_row.empty:
                        planet_x = planet_row[selected_x].values[0]
                        planet_y = planet_row[selected_y].values[0]
                        plt.scatter(planet_x, planet_y, color='red', s=100, label=f"Planet: {selected_planet}")

                    # Add title, labels, and legend
                    plt.title(f'{selected_x} vs {selected_y} ({selected_chart})')
                    plt.xlabel(selected_x)
                    plt.ylabel(selected_y)
                    plt.legend()
                    plt.grid(True)

                    # Show the plot
                    plt.show()

                else:
                    print("Selected data not found in the CSV.")
            except FileNotFoundError:
                print("CSV file not found!")

    # Button to confirm selection and generate graph
    btn = CTkButton(master=graph_window, text="Generate Graph", corner_radius=12, height=52, width=160,
                    fg_color='#1E88E5', hover_color='#1976D2', command=on_program_select)
    btn.place(relx=0.5, rely=0.85, anchor="center")

def btn_callback():
    data = entry.get()  # Get the input from the entry
    toplevel = CTkToplevel(app)  # Create a new toplevel window
    toplevel.title("ExoSky - Planet Information")
    toplevel.geometry('1200x700')

    try:
        # Read the CSV file
        exo = pd.read_csv('exo.csv', delimiter=',')  # Using comma delimiter
        
        planet_name = data
        # Search for the planet name in the dataset
        result = exo[exo['pl_name'] == planet_name]
        
        if not result.empty:
            planet_info = result.iloc[0]  # Get the first row as a Series

            # Display the planet name
            label = CTkLabel(master=toplevel, text=f"Planet: {planet_name}", font=("Arial", 40), text_color="lightblue")
            label.place(relx=0.5, rely=0.1, anchor="center")
            
            # Extract individual fields and display them
            hostname = planet_info['hostname']
            no_of_stars = planet_info['No.of stars']
            no_of_planets = planet_info['No.of Planets']
            no_of_moons = planet_info['No.of Moons']
            discovery_year = planet_info['Discovery year']
            discovery_facility = planet_info['Discovery facility']
            discovery_instrument = planet_info['Discovery Instrument']
            orbital_period = planet_info['Orbital Period']
            stellar_temp = planet_info['Stellar effective Temparature']
            stellar_radius = planet_info['Stellar radius']
            stellar_mass = planet_info['Stellar mass']
            stellar_gravity = planet_info['Stellar surface gravity']
            distance = planet_info['distance']
            gaia_magnitude = planet_info['Gaia Magnitude']
            release_date = planet_info['releasedate']

            label1 = CTkLabel(master=toplevel, text=f"Hostname: {hostname}", font=("Arial",20), text_color="lightblue")
            label1.place(relx=0.15, rely=0.2, anchor="w")

            label2 = CTkLabel(master=toplevel, text=f"No. of Stars: {no_of_stars}", font=("Arial", 20), text_color="lightblue")
            label2.place(relx=0.15, rely=0.3, anchor="w")

            label3 = CTkLabel(master=toplevel, text=f"No. of Planets: {no_of_planets}", font=("Arial", 20), text_color="lightblue")
            label3.place(relx=0.15, rely=0.4, anchor="w")

            label4 = CTkLabel(master=toplevel, text=f"Discovery Year: {discovery_year}", font=("Arial", 20), text_color="lightblue")
            label4.place(relx=0.15, rely=0.5, anchor="w")

            label5 = CTkLabel(master=toplevel, text=f"Discovery Facility: {discovery_facility}", font=("Arial", 20), text_color="lightblue")
            label5.place(relx=0.15, rely=0.6, anchor="w")
            
            label6 = CTkLabel(master=toplevel, text=f"Discovery Instrument: {discovery_instrument}", font=("Arial", 20), text_color="lightblue")
            label6.place(relx=0.15, rely=0.7, anchor="w")

            label7 = CTkLabel(master=toplevel, text=f"Orbital Period: {orbital_period}", font=("Arial", 20), text_color="lightblue")
            label7.place(relx=0.15, rely=0.8, anchor="w")

            label8 = CTkLabel(master=toplevel, text=f"Stellar Temperature: {stellar_temp} K", font=("Arial", 20), text_color="lightblue")
            label8.place(relx=0.65, rely=0.2, anchor="w")

            label9 = CTkLabel(master=toplevel, text=f"Stellar Radius: {stellar_radius} Solar Radii", font=("Arial", 20), text_color="lightblue")
            label9.place(relx=0.65, rely=0.3, anchor="w")

            label10 = CTkLabel(master=toplevel, text=f"Stellar Mass: {stellar_mass} Solar Masses", font=("Arial", 20), text_color="lightblue")
            label10.place(relx=0.65, rely=0.4, anchor="w")

            label11 = CTkLabel(master=toplevel, text=f"Stellar Gravity: {stellar_gravity} m/s²", font=("Arial", 20), text_color="lightblue")
            label11.place(relx=0.65, rely=0.5, anchor="w")

            label12 = CTkLabel(master=toplevel, text=f"Distance: {distance} light-years",font=("Arial", 20), text_color="lightblue")
            label12.place(relx=0.65, rely=0.6, anchor="w")

            label13 = CTkLabel(master=toplevel, text=f"Gaia Magnitude: {gaia_magnitude}", font=("Arial", 20), text_color="lightblue")
            label13.place(relx=0.65, rely=0.7, anchor="w")

            label14 = CTkLabel(master=toplevel, text=f"Release Date: {release_date}" ,font=("Arial", 20), text_color="lightblue")
            label14.place(relx=0.65, rely=0.8, anchor="w")

            btn = CTkButton(master=toplevel, text="Generate Graph", corner_radius=12, height=52, width=160, fg_color='#1E88E5', hover_color='#1976D2',command=graph)
            btn.place(anchor="sw", relx=0.46, rely=0.97)

            btn = CTkButton(master=toplevel, text="Learn more", corner_radius=12, height=52, width=160, fg_color='#1E88E5', hover_color='#1976D2',command=linknasa)
            btn.place(anchor="sw", relx=0.86, rely=0.97)


        else:
            # If the planet doesn't exist, show a message
            label = CTkLabel(master=toplevel, text=f"Sorry, planet '{planet_name}' not found.", font=("Arial", 40), text_color="red")
            label.place(relx=0.5, rely=0.3, anchor="center")

    except FileNotFoundError:
        # Handle the case where the CSV file is not found
        label = CTkLabel(master=toplevel, text="CSV file not found!", font=("Arial", 40), text_color="red")
        label.place(relx=0.5, rely=0.3, anchor="center")

def exit_callback():
    app.destroy()

# Main Tkinter setup
app = CTk()
app.title("ExoSky")
app.geometry('1280x720')

bg_image_path = "/Users/abid/Desktop/Abid/NASA/bg.jpg"  # Update with your image path
background_image = Image.open(bg_image_path)
background_image = background_image.resize((1280, 720), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(background_image)
canvas = CTkCanvas(app, width=1280, height=720)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)


# Load the image (make sure the path is correct)
image_path = 'exo.png'  # Replace with your image file path
image = Image.open(image_path)

# Resize the image (optional)
image = image.resize((300, 100))  # Resize to fit the desired place in your GUI

# Convert the image for use with tkinter
img_tk = ImageTk.PhotoImage(image)

# Create a label to display the image and place it
label_image = CTkLabel(master=app, image=img_tk, text="")
label_image.image = img_tk  # Keep a reference to the image to prevent garbage collection
label_image.place(relx=0.5, rely=0.16, anchor="center") 


label1 = CTkLabel(master=app, text="“Connect with the Stars Beyond!”", font=("Arial", 20), text_color="white")
label1.place(relx=0.39, rely=0.25, anchor="nw")

entry = CTkEntry(master=app, placeholder_text="Start typing...", width=700, height=50, text_color="#FFC700")
entry.place(relx=0.22, rely=0.47, anchor="sw")

btn = CTkButton(master=app, text="Search", corner_radius=12, height=52, width=130, fg_color='#1E88E5', hover_color='#1976D2', command=btn_callback)
btn.place(anchor="sw", relx=0.775, rely=0.47)

btn1 = CTkButton(master=app, text="Exit", corner_radius=12, height=40, width=120, fg_color='#FF7043', hover_color='#F4511E', command=exit_callback)
btn1.place(anchor="sw", relx=0.02, rely=0.1)

btn2 = CTkButton(master=app, text="Gaia",font=("Arial", 30), corner_radius=12, height=70, width=200, fg_color='#1E88E5', hover_color='#1976D2', command=analyze_gaia_data)
btn2.place(anchor="sw", relx=0.23, rely=0.64)

btn3 = CTkButton(master=app, text="Aurora", corner_radius=12,font=("Arial", 30), height=70, width=200, fg_color='#FF7043', hover_color='#F4511E', command=run_test_file)
btn3.place(anchor="sw", relx=0.42, rely=0.64)

btn4 = CTkButton(master=app, text="3D Map", corner_radius=12,font=("Arial", 30), height=70, width=200, fg_color='#03C04A', hover_color='#03AC13', command=run_test_file1)
btn4.place(anchor="sw", relx=0.62, rely=0.64)

btn5 = CTkButton(master=app, text="Explore", corner_radius=12, height=40, width=120, fg_color='#1E88E5', hover_color='#1976D2', command=explore)
btn5.place(anchor="sw", relx=0.87, rely=0.1)


label2 = CTkLabel(master=app, text="@Cosmic_Orbiters", font=("Arial", 10), text_color="lightblue")
label2.place(relx=0.9, rely=0.95, anchor="nw")

app.mainloop()