import pandas as pd
from pynput import mouse
import os
from playsound import playsound

file_name = input("Enter the file name (without extension): ") + '.csv'

if os.path.exists(file_name):
    data = pd.read_csv(file_name).to_dict(orient='records')
else:
    data = []

print("The program is running. Click anywhere on the screen to save the mouse coordinates.")

def on_click(x, y, button, pressed):

    # Play sound when clicked
    playsound('./AutoAuto/salva_gui_csv/accets/sound.mp4')

    if pressed:
        element_name = input("Enter the name of the element to be saved: ")

        # Stores coordinates and name in a dictionary
        coord = {"Name": element_name, "X": x, "Y": y}
        
        # Add dictionary to list
        data.append(coord)
        

        print(f'Saved coordinates: {coord}')
        
        # Saves data to a dataframe and exports to CSV
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)

        # Ends the execution of the mouse listener (pynput)
        on_click = False
        return on_click

# Start the mouse listener (pynput)
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
