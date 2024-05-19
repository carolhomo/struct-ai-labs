import dataclasses
import enum
import json
from typing import List, Dict


@dataclasses.dataclass
class Book:
    id: int
    name: str
    author: str
    genre: str
    price: int
    available: bool = True


class SORT_TYPE(enum.Enum):
    TOP_UP = 'top_up'
    TOP_DOWN = 'top_down'


@dataclasses.dataclass
class BookCopy:
    book: Book
    location: str


class Library:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'storage'):
            self.storage: Dict[int, List[BookCopy]] = {}

    def add_book(self, book: Book, location: str) -> bool:
        book_copy = BookCopy(book=book, location=location)
        if book.id in self.storage:
            self.storage[book.id].append(book_copy)
        else:
            self.storage[book.id] = [book_copy]
        return True

    def del_book(self, book_id: int) -> bool:
        if book_id in self.storage:
            del self.storage[book_id]
            return True
        return False

    def sort_by_price(self, sort_type: SORT_TYPE) -> List[BookCopy]:
        all_books = [copy for copies in self.storage.values() for copy in copies]
        sorted_books = sorted(
            all_books,
            key=lambda copy: copy.book.price,
            reverse=(sort_type == SORT_TYPE.TOP_DOWN)
        )
        return sorted_books

    def find_book_by_name(self, name: str) -> List[BookCopy]:
        return [copy for copies in self.storage.values() for copy in copies if copy.book.name == name]

    def find_book_by_author(self, author: str) -> List[BookCopy]:
        return [copy for copies in self.storage.values() for copy in copies if copy.book.author == author]

    def find_book_by_genre(self, genre: str) -> List[BookCopy]:
        return [copy for copies in self.storage.values() for copy in copies if copy.book.genre == genre]

    def get_all_books(self) -> List[BookCopy]:
        return [copy for copies in self.storage.values() for copy in copies]

    def analyze_data(self) -> Dict[str, Dict]:
        authors_count = {}
        genres_count = {}

        for copies in self.storage.values():
            for copy in copies:
                book = copy.book
                if book.author in authors_count:
                    authors_count[book.author] += 1
                else:
                    authors_count[book.author] = 1

                if book.genre in genres_count:
                    genres_count[book.genre] += 1
                else:
                    genres_count[book.genre] = 1

        most_popular_author = max(authors_count, key=authors_count.get)
        most_popular_genre = max(genres_count, key=genres_count.get)

        return {
            'most_popular_author': most_popular_author,
            'most_popular_genre': most_popular_genre,
            'authors_count': authors_count,
            'genres_count': genres_count
        }

    def save_to_file(self, filename: str):
        data = {
            book_id: [
                {
                    'book': dataclasses.asdict(copy.book),
                    'location': copy.location
                }
                for copy in copies
            ]
            for book_id, copies in self.storage.items()
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_from_file(self, filename: str):
        with open(filename, 'r') as file:
            data = json.load(file)
        self.storage = {
            int(book_id): [
                BookCopy(
                    book=Book(**copy['book']),
                    location=copy['location']
                )
                for copy in copies
            ]
            for book_id, copies in data.items()
        }

    def check_availability(self, name: str) -> bool:
        for copies in self.storage.values():
            for copy in copies:
                if copy.book.name == name:
                    return copy.book.available
        return False

    def change_availability(self, name: str, available: bool) -> bool:
        updated = False
        for copies in self.storage.values():
            for copy in copies:
                if copy.book.name == name:
                    copy.book.available = available
                    updated = True
        return updated


if __name__ == "__main__":
    library = Library()

    library.add_book(Book(1, "Book One", "Author A", "Fiction", 100), "Shelf A")
    library.add_book(Book(2, "Book Two", "Author B", "Science Fiction", 150), "Shelf B")
    library.add_book(Book(3, "Book Three", "Author A", "Fiction", 200), "Shelf C")
    library.add_book(Book(3, "Book Three", "Author A", "Fiction", 200), "Shelf D")

    library.del_book(1)

    books_by_name = library.find_book_by_name("Book Two")

    sorted_books = library.sort_by_price(SORT_TYPE.TOP_DOWN)

    analysis = library.analyze_data()

    availability = library.check_availability("Book Three")

    library.change_availability("Book Three", False)

    library.save_to_file("library_data.json")
    library.load_from_file("library_data.json")

    print("Books by name:", books_by_name)
    print("Sorted books:", sorted_books)
    print("Analysis:", analysis)
    print("Availability of Book Three:", availability)
