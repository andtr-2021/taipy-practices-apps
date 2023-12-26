from taipy.gui import Gui


content = "images/cat.jpeg"

page = """

<h1>Cat and Dog Image Displayer</h1>

<p>Everytime you reload the page a random cat or dog image will show up.</p>

<br></br>

<|{content}|image|>

<br></br>

<|New Image|button|on_action=new_button_action|>

"""

def new_button_action(state):
    if state.content == "images/cat.jpeg":
        state.content = "images/dog.jpeg"
    else :
        state.content = "images/cat.jpeg"

Gui(page).run(dark_mode=False)