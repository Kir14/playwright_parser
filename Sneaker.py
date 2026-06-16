from dataclasses import dataclass, field
from typing import List

@dataclass
class Sneaker:
    name: str
    price: str
    url: str
    image: str
    description: str
    color: str
    sizes: List[str] = field(default_factory=list)  # ✅ Fixed

    def __str__(self):
        return (
            f"{self.name}: {self.price}\n"
            f"{self.url}\n"
            f"{self.description}\n"
            f"{self.image}\n"
            f"{self.color}\n"
            f"Sizes: {', '.join(self.sizes) if self.sizes else 'No sizes'}"
        )