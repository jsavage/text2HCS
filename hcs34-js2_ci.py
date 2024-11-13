import re
import os
import graphviz
import tkinter as tk 
#import subprocess
is_ci = os.getenv('CI') == 'true' # Used to determine whether this code is being run in a CI environment

def parse_hcs(input_text):
    entities = set()
    actions = []
    feedback = []
    nested_entities = {}

    lines = input_text.splitlines()

    for line in lines:
        line = line.strip()

        if ':' in line:
            entities_part, actions_part = line.split(':', 1)
            entities_part = entities_part.strip()
            actions_part = actions_part.strip()

            if '/' in actions_part:
                actions_list, feedback_list = actions_part.split('/', 1)
                actions_list = actions_list.strip().split()
                feedback_list = feedback_list.strip().split()
            else:
                actions_list = actions_part.split()
                feedback_list = []

            entity_list = [e for e in re.split(r'\s+', entities_part) if e != '-']

            if len(entity_list) > 2:
                raise ValueError(f"Expected exactly 2 entities before the colon, but got {entity_list}")

            controlling_entity, target_entity = map(str.strip, entity_list)
            entities.add(controlling_entity)
            entities.add(target_entity)

            for action in actions_list:
                actions.append((controlling_entity, target_entity, action))

            for fb in feedback_list:
                feedback.append((target_entity, controlling_entity, fb))

        elif '[' in line and ']' in line:
            main_entity, nested = re.match(r'(.*?)\[(.*)\]', line).groups()
            main_entity = main_entity.strip()
            nested_entities_list = nested.strip().split()

            entities.add(main_entity)
            nested_entities[main_entity] = nested_entities_list

            for ne in nested_entities_list:
                entities.add(ne)

        else:
            entity_list = [e for e in re.split(r'\s+', line) if e != '-']
            for entity in entity_list:
                entities.add(entity)

    return list(entities), actions, feedback, nested_entities

def xdraw_hcs(entities, actions, feedback, nested_entities, output_file):
    dot = graphviz.Digraph(format='png')

    for entity in entities:
        dot.node(entity, shape='rectangle')

    for parent, children in nested_entities.items():
        with dot.subgraph(name=f'cluster_{parent}') as sub:
            sub.attr(label=parent)
            sub.node(parent, shape='rectangle')
            for child in children:
                sub.node(child, shape='rectangle')

    for (src, tgt, action) in actions:
        dot.edge(src, tgt, label=action)
    for (src, tgt, fb) in feedback:
        dot.edge(src, tgt, label=fb, color='red')

    dot.render(output_file, cleanup=True)

def ydraw_hcs(entities, actions, feedback, nested_entities, output_file):
    dot = graphviz.Digraph(format='png')

    # Add all top-level entities that are not nested entities
    for entity in entities:
        if entity not in nested_entities and not any(entity in sublist for sublist in nested_entities.values()):
            dot.node(entity, shape='rectangle')

    # Handle nested entities
    for parent, children in nested_entities.items():
        with dot.subgraph(name=f'cluster_{parent}') as sub:
            sub.attr(label=parent)
            sub.node(parent, shape='rectangle')
            for child in children:
                sub.node(child, shape='rectangle')

    # Draw actions and feedback
    for (src, tgt, action) in actions:
        dot.edge(src, tgt, label=action)
    for (src, tgt, fb) in feedback:
        dot.edge(src, tgt, label=fb, color='red')

    dot.render(output_file, cleanup=True)



def draw_hcs(entities, actions, feedback, nested_entities, output_file):
    dot = graphviz.Digraph(format='png')

    # Track which entities have already been drawn
    drawn_entities = set()

    # Draw top-level entities that are not nested within any other entity
    for entity in entities:
        if entity not in nested_entities and not any(entity in children for children in nested_entities.values()):
            dot.node(entity, shape='rectangle')
            drawn_entities.add(entity)

    # Draw nested entities within their parent entities
    for parent, children in nested_entities.items():
        if parent not in drawn_entities:
            with dot.subgraph(name=f'cluster_{parent}') as sub:
                sub.attr(label=parent)
                #sub.node(parent, shape='rectangle')
                for child in children:
                    sub.node(child, shape='rectangle')
                    drawn_entities.add(child)
            drawn_entities.add(parent)

    # Draw actions (control) and feedback arrows
    for (src, tgt, action) in actions:
        dot.edge(src, tgt, label=action)

    for (src, tgt, fb) in feedback:
        dot.edge(src, tgt, label=fb, color='red')

    dot.render(output_file, cleanup=True)

def zzdraw_hcs(entities, actions, feedback, nested_entities, output_file):
    dot = graphviz.Digraph(format='png')

    # Track which entities have already been drawn
    drawn_entities = set()

    # Draw top-level entities that are not nested within any other entity
    for entity in entities:
        if entity not in nested_entities and not any(entity in children for children in nested_entities.values()):
            dot.node(entity, shape='rectangle')
            drawn_entities.add(entity)

    # Draw nested entities within their parent entities
    for parent, children in nested_entities.items():
        with dot.subgraph(name=f'cluster_{parent}') as sub:
            sub.attr(label=parent, style='dotted')
            sub.node(parent, shape='rectangle')
            for child in children:
                if child not in drawn_entities:  # Ensure not to draw a nested entity more than once
                    sub.node(child, shape='rectangle')
                    drawn_entities.add(child)
            drawn_entities.add(parent)

    # Draw actions (control) and feedback arrows
    for (src, tgt, action) in actions:
        dot.edge(src, tgt, label=action)

    for (src, tgt, fb) in feedback:
        dot.edge(src, tgt, label=fb, color='red')

    dot.render(output_file, cleanup=True)

def zzzdraw_hcs(entities, actions, feedback, nested_entities, output_file):
    dot = graphviz.Digraph(format='png')

    # Draw top-level entities that are not nested within any other entity
    for entity in entities:
        if entity not in nested_entities and not any(entity in children for children in nested_entities.values()):
            dot.node(entity, shape='rectangle')

    # Draw nested entities within their parent entities
    for parent, children in nested_entities.items():
        with dot.subgraph(name=f'cluster_{parent}') as sub:
            sub.attr(label=parent, style='dotted')
            #sub.node(parent, shape='rectangle')  # Parent node
            for child in children:
                sub.node(child, shape='rectangle')  # Child nodes

    # Draw actions (control) and feedback arrows
    for (src, tgt, action) in actions:
        dot.edge(src, tgt, label=action)

    for (src, tgt, fb) in feedback:
        dot.edge(src, tgt, label=fb, color='red')

    dot.render(output_file, cleanup=True)


def run_tests():
    test_cases = [

        {
            "input": "person microwave",
            "expected_entities": {'person', 'microwave'},
            "expected_actions": [],
            "expected_feedback": [],
            "expected_nested": {}
        },
        {
            "input": "person microwave: open close start stop",
            "expected_entities": {'person', 'microwave'},
            "expected_actions": [
                ('person', 'microwave', 'open'),
                ('person', 'microwave', 'close'),
                ('person', 'microwave', 'start'),
                ('person', 'microwave', 'stop')
            ],
            "expected_feedback": [],
            "expected_nested": {}
        },
        {
            "input": "person microwave: open close start stop / beep",
            "expected_entities": {'person', 'microwave'},
            "expected_actions": [
                ('person', 'microwave', 'open'),
                ('person', 'microwave', 'close'),
                ('person', 'microwave', 'start'),
                ('person', 'microwave', 'stop')
            ],
            "expected_feedback": [
                ('microwave', 'person', 'beep')
            ],
            "expected_nested": {}
        },
        {
            "input": "microwave [ magnetron ]\nmagnetron food: heat",
            "expected_entities": {'microwave', 'magnetron', 'food'},
            "expected_actions": [
                ('magnetron', 'food', 'heat')
            ],
            "expected_feedback": [],
            "expected_nested": {
                'microwave': ['magnetron']
            }
        },
        {
            "input": "person microwave: open close start stop / beep\nmicrowave [ magnetron ]\nmagnetron food: heat",
            "expected_entities": {'person', 'microwave', 'magnetron', 'food'},
            "expected_actions": [
                ('person', 'microwave', 'open'),
                ('person', 'microwave', 'close'),
                ('person', 'microwave', 'start'),
                ('person', 'microwave', 'stop'),
                ('magnetron', 'food', 'heat')
            ],
            "expected_feedback": [
                ('microwave', 'person', 'beep')
            ],
            "expected_nested": {
                'microwave': ['magnetron']
            }
        },
        {
            "input": "person microwave: open close start stop / beep\nmicrowave [ magnetron ]\nmagnetron food: heat\nfood warm-food -: becomes\nperson warm-food: stir / eat",
            "expected_entities": {'person', 'microwave', 'magnetron', 'food', 'warm-food'},
            "expected_actions": [
                ('person', 'microwave', 'open'),
                ('person', 'microwave', 'close'),
                ('person', 'microwave', 'start'),
                ('person', 'microwave', 'stop'),
                ('magnetron', 'food', 'heat'),
                ('food', 'warm-food', 'becomes'),
                ('person', 'warm-food', 'stir')
            ],
            "expected_feedback": [
                ('microwave', 'person', 'beep'),
                ('warm-food', 'person', 'eat')
            ],
            "expected_nested": {
                'microwave': ['magnetron']
            }
        },
        {
            "input": "microwave [ magnetron ]",
            "expected_entities": {'microwave', 'magnetron'},
            "expected_actions": [],
            "expected_feedback": [],
            "expected_nested": {
                'microwave': ['magnetron']
            }
        },
        {
            "input": "microwave [ magnetron ]",
            "expected_entities": {"microwave", "magnetron"},
            "expected_nested": {"microwave": ["magnetron"]},
            "expected_actions": [],
            "expected_feedback": []
        },
        {
            "input": "microwave [ magnetron heater ]",
            "expected_entities": {"microwave", "magnetron", "heater"},
            "expected_nested": {"microwave": ["magnetron", "heater"]},
            "expected_actions": [],
            "expected_feedback": []
        },
        # magnetron was nested in the following 
        {
            "input": "microwave magnetron oven",
            "expected_entities": {"microwave", "magnetron", "oven"},
            "expected_nested": {},
            "expected_actions": [],
            "expected_feedback": []
        },
        {
            "input": "microwave [ magnetron ]\n magnetron food: heat",
            "expected_entities": {"microwave", "magnetron", "food"},
            "expected_nested": {"microwave": ["magnetron"]},
            "expected_actions": [("magnetron", "food", "heat")],
            "expected_feedback": []
        }


    ]

    for i, case in enumerate(test_cases, 1):
        try:
            entities, actions, feedback, nested_entities = parse_hcs(case["input"])
            assert set(entities) == case["expected_entities"], f"Test Case {i} Failed: {entities} != {case['expected_entities']}"
            assert set(actions) == set(case["expected_actions"]), f"Test Case {i} Failed: {actions} != {case['expected_actions']}"
            assert set(feedback) == set(case["expected_feedback"]), f"Test Case {i} Failed: {feedback} != {case['expected_feedback']}"
            assert nested_entities == case["expected_nested"], f"Test Case {i} Failed: {nested_entities} != {case['expected_nested']}"
            print(f"Test Case {i} Passed")
        except AssertionError as e:
            print(str(e))

    print("Testing complete.")

if __name__ == "__main__":
    run_tests()
#    last_case = {
#        "input": "person microwave: open close start stop / beep\nmicrowave [ magnetron ]\nmagnetron food: heat\nfood warm-food -: becomes\nperson warm-food: stir / eat",
#        "output_file": "hcs_diagram"
#    }
#    entities, actions, feedback, nested_entities = parse_hcs(last_case["input"])

#    description = input("Describe the model in the 'depict' style")

#    description = {}
#    description = "person microwave: open close start stop / beep\nmicrowave [ magnetron ]\nmagnetron food: heat\n"

    

from PIL import Image, ImageTk  # Import Pillow modules correctly

# Function to update word count, display the list of words, and count capitalized words
def update_text_info(event=None, default_text=None):
    if default_text:
        text_area.delete("1.0", tk.END)  # Clear the text area
        text_area.insert(tk.END, default_text)  # Insert the default text

    text_content = text_area.get("1.0", tk.END)  # Get all text from the text area
    ##words = text_content.split()

    # Update the word count label
    ##word_count.set(f"Words: {len(words)}")
    
    # Update the word list label
    ##word_list.set(f"Words used: {', '.join(words)}")
    
    # Call the function to count capitalized words and update the label
    ##capitalized_words = count_capitalized_words(words)
    ##capitalized_word_count.set(f"Capitalized Words: {capitalized_words}")
    #print(text_content)

    user_case = {
        "input": text_content,
        "output_file": "user_hcs_diagram"
    }
    
    entities, actions, feedback, nested_entities = parse_hcs(user_case["input"])
    draw_hcs(entities, actions, feedback, nested_entities, user_case["output_file"])
    print('Updating Entities found:', entities)
    print('Actions found:', actions)
    print('Feedback found:', feedback)
    #print('Nested entities found:', nested_entities)
    
    # Load the image using PIL
    img = Image.open("user_hcs_diagram.png")
#    img = img.resize((int(root.winfo_width() * 0.65), int(root.winfo_height())), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
    img = ImageTk.PhotoImage(img)

    # Display the image in a label
    img_label.config(image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    
    # Set the status message in the main window
    task_label.set("Image displayed in the main window.")


# Function to count the number of capitalized words
##def count_capitalized_words(words):
##    return sum(1 for word in words if word.istitle())

# Function to display an image in the main window
def Y():
    # Load the image using PIL
    img = Image.open("user_hcs_diagram.png")
    img = img.resize((int(root.winfo_width() * 0.65), int(root.winfo_height())), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
    img = ImageTk.PhotoImage(img)

    # Display the image in a label
    img_label.config(image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    
    # Set the status message in the main window
    task_label.set("Image displayed in the main window.")

# Function to exit the tkinter window and carry on after root.mainloop()
def exit_program():
    root.quit()  # Exits the main loop and closes the window


def do_tk():
    # Setting up the main application window
    root = tk.Tk()
    root.title("Word Counter with Image Display")

    # Configure grid layout
    root.grid_columnconfigure(0, weight=1)  # Column 0 for text input and controls (35%)
    root.grid_columnconfigure(1, weight=2)  # Column 1 for image display (65%)

    # Creating a Text widget for multi-line text input
    text_area = tk.Text(root, wrap="word", height=15, width=30)
    text_area.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")
 
    # Label to display the status of the tasks
    task_label = tk.StringVar()
    task_label.set("No task running.")

    task_status_label = tk.Label(root, textvariable=task_label, font=("Helvetica", 14))
    task_status_label.grid(row=3, column=1, sticky="nw", padx=10)

    # Button to start the function Y
    start_button = tk.Button(root, text="Refresh Diagram", command=Y, font=("Helvetica", 14))
    start_button.grid(row=4, column=0, sticky="nw", padx=10, pady=5)

    # Button to exit the tkinter window
    exit_button = tk.Button(root, text="Exit", command=exit_program, font=("Helvetica", 14))
    exit_button.grid(row=5, column=0, sticky="nw", padx=10, pady=5)

    # Label to display the image
    img_label = tk.Label(root)
    img_label.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

    # Initialize the text area with default text and update the information
    default_text = "person microwave: open close start stop / beep\nmicrowave [ magnetron ]\nmagnetron food: heat\nfood warm-food -: becomes\nperson warm-food: stir / eat"
    default_text = "microwave [ magnetron ]"
    default_text = "Microwave-oven[Door Timer Controller Turntable Light Magnetron Food]\n"\
    "Person Door: open,close\n" \
    "Door Controller: Door_status\n"\
    "Controller Light: On,Off\n" \
    "Controller Turntable: On,Off\n"\
    "Controller Magnetron: On,Off\n" \
    "Person Timer : Set Start,Stop / Time,Beep\n"\
    "Controller Magnetron\n"\
    "Timer Controller:Cook\n"\
    "Turntable Food:Turns\n"\
    "Light Food:Iluminates\n"\
    "Magnetron Food:Heats\n"\
    "Person Food: /Audible_&_Visible_Feedback"
    update_text_info(default_text=default_text)

    # Link the <KeyRelease> event to the text info update function
    text_area.bind("<KeyRelease>", update_text_info)

    # Run the main application loop
    root.mainloop()

    # Code to execute after the tkinter window is closed
    print("Tkinter window closed, continuing execution...")

if not is_ci:
    # Code to create and display Tkinter windows
    # Eg root = tk.Tk()
    # Your window setup and logic here
    # e.g., root.mainloop()

    do_tk()

else:
    print("Running in CI mode - Tkinter GUI is disabled.")
