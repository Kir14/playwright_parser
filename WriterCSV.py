import csv
from Sneaker import Sneaker

class WriterCSV:

    def __init__(self, filename):
        self.filename = filename
        self.csvfile = None
        self.writer = None
        self.fields = [
            "name"
            , "price"
            , "url"
            , "image"
            , "description"
            , "color"
            , "sizes"
        ]

    def open(self):
        """Open the file for writing"""
        self.csvfile = open(self.filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fields)
        self.writer.writeheader()
        self.csvfile.flush()
        return self

    def write_sneaker(self, sneaker):
        """Write Sneaker objects to CSV"""
        if not self.writer:
            raise Exception("File not opened. Call open() first.")

        # Convert object to dict using __dict__
        self.writer.writerow(sneaker.__dict__)

        self.csvfile.flush()
        print(f"Written {sneaker.name} sneakers to {self.filename}")
        return self

    def close(self):
        """Close the file"""
        if self.csvfile and not self.csvfile.closed:
            self.csvfile.close()
            print(f"Closed {self.filename}")
        return self

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()