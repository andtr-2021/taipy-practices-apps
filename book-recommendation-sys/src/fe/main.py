from taipy.gui import Gui, navigate, notify
import pandas as pd
import json

books_data_file = "../../data/data4display/goodreads-books.csv"
books_df = pd.read_csv(books_data_file)

user_data_file = "../../data/data4display/user_collection.json"

root_md="<|menu|label=Menu|lov={[('collection', 'collection'), ('books_list', 'books_list')]}|on_action=on_menu|>"
find_filters = ["Title", "isbn", "isbn13"]

class Book:
    def __init__(self, id, book_id, isbn, isbn13):
        self.id, self.book_id, self.isbn, self.isbn13 = (id, book_id, isbn, isbn13)

# Check if the JSON file exists and create it if it doesn't
try:
    with open(user_data_file, "x") as file:
        json.dump([], file)
except FileExistsError:
    pass

# Function to load spendings from JSON file
def load_user_datas():
    with open(user_data_file, "r") as file:
        return [Book(**data) for data in json.load(file)]

find_filter = find_filters[0]
value = ""
status = ""

user_datas = load_user_datas()
user_data_df = books_df[books_df["isbn"].isin([data.isbn for data in user_datas])]

collection_md="""
## Find a book
Search by <|{find_filter}|selector|lov={find_filters}|dropdown|>
Input <|{value}|input|>

<|{status}|>

<|Confirm|button|on_action=on_confirm_button_action|>

## Your collection
<|{user_data_df}|table|filter|>
"""

def on_confirm_button_action(state):
    # Filtering the dataframe based on the input value and the filter selected by the user
    search_df = books_df[books_df[state.find_filter] == state.value]

    if search_df.empty:
        state.status = "No book found with {} = {}".format(state.find_filter, state.value)

    else:
        book_data = search_df.iloc[0].to_dict()
        if any(data.isbn == book_data['isbn'] for data in state.user_datas):
            state.status = "Book already in collection"

        else:
            new_book = Book(len(state.user_datas), book_data["Book Id"], book_data["isbn"], book_data["isbn13"])
            state.user_datas.append(new_book)

            with open(user_data_file, "w") as file:
                json.dump([vars(data) for data in state.user_datas], file)

            state.user_data_df = books_df[books_df["isbn"].isin([data.isbn for data in state.user_datas])]
            state.status = "Added book '{}' to collection".format(book_data['Title'])

    return state.status


books_list_md = """
# Books
<|{books_df}|table|filter|>
"""

def on_menu(state, action, info):
    page = info["args"][0]
    navigate(state, to=page)

pages = {
    "/": root_md,
    "collection": collection_md,
    "books_list": books_list_md,
}

Gui(pages=pages).run()