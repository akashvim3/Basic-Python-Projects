from dataclasses import dataclass, field
from typing import List

@dataclass
class Hotel:
    name: str
    roomAvl: int
    location: str
    rating: int
    pricePr: int

    sortParam: str = field(default='name', init=False)

    def __lt__(self, other):
        """Override comparison operator for sorting based on sortParam."""
        return getattr(self, Hotel.sortParam) < getattr(other, Hotel.sortParam)

    @classmethod
    def sortBy(cls, param: str):
        """Sort hotels by any given parameter."""
        cls.sortParam = param

    def __repr__(self):
        return f"Hotel: {self.name}, Rooms Available: {self.roomAvl}, Location: {self.location}, Rating: {self.rating}, Price/Room: {self.pricePr}"


@dataclass
class User:
    uname: str
    uId: int
    cost: int

    def __repr__(self):
        return f"User: {self.uname}, ID: {self.uId}, Booking Cost: {self.cost}"


def PrintHotelData(hotels: List[Hotel]):
    print("\n--- Hotel Data ---")
    for h in hotels:
        print(h)


def SortHotelByName(hotels: List[Hotel]):
    Hotel.sortBy('name')
    hotels.sort()
    print("\n--- Sorted by Name ---")
    PrintHotelData(hotels)


def SortHotelByRating(hotels: List[Hotel]):
    Hotel.sortBy('rating')
    hotels.sort()
    print("\n--- Sorted by Rating ---")
    PrintHotelData(hotels)


def PrintHotelByCity(location: str, hotels: List[Hotel]):
    filtered_hotels = [h for h in hotels if h.location == location]
    print(f"\n--- Hotels in {location} ---")
    PrintHotelData(filtered_hotels)


def SortByRoomAvailable(hotels: List[Hotel]):
    Hotel.sortBy('roomAvl')
    hotels.sort()
    print("\n--- Sorted by Rooms Available ---")
    PrintHotelData(hotels)


def SearchHotelByName(search_name: str, hotels: List[Hotel]):
    filtered_hotels = [h for h in hotels if search_name.lower() in h.name.lower()]
    if filtered_hotels:
        print(f"\n--- Search Results for '{search_name}' ---")
        PrintHotelData(filtered_hotels)
    else:
        print(f"No hotels found for '{search_name}'.")


def FilterHotelsByPrice(min_price: int, max_price: int, hotels: List[Hotel]):
    filtered_hotels = [h for h in hotels if min_price <= h.pricePr <= max_price]
    if filtered_hotels:
        print(f"\n--- Hotels within Price Range {min_price}-{max_price} ---")
        PrintHotelData(filtered_hotels)
    else:
        print(f"No hotels found within the price range {min_price}-{max_price}.")


def PrintUserData(userName, userId, bookingCost, hotels: List[Hotel]):
    users = [User(uname=userName[i], uId=userId[i], cost=bookingCost[i]) for i in range(3)]
    for i in range(len(users)):
        print(f"\n{users[i]} \tBooked Hotel: {hotels[i].name}")


def HotelManagement(userName, userId, hotelName, bookingCost, rooms, locations, ratings, prices):
    hotels = [Hotel(hotelName[i], rooms[i], locations[i], ratings[i], prices[i]) for i in range(3)]

    # Print initial hotel data
    PrintHotelData(hotels)

    # Sort and display hotels by various criteria
    SortHotelByName(hotels)
    SortHotelByRating(hotels)
    PrintHotelByCity("Bangalore", hotels)
    SortByRoomAvailable(hotels)

    # Print user data
    PrintUserData(userName, userId, bookingCost, hotels)

    # Additional features
    SearchHotelByName("H1", hotels)
    FilterHotelsByPrice(100, 200, hotels)


if __name__ == '__main__':
    userName = ["U1", "U2", "U3"]
    userId = [2, 3, 4]
    hotelName = ["H1", "H2", "H3"]
    bookingCost = [1000, 1200, 1100]
    rooms = [4, 5, 6]
    locations = ["Bangalore", "Bangalore", "Mumbai"]
    ratings = [5, 5, 4]
    prices = [100, 200, 100]

    HotelManagement(userName, userId, hotelName, bookingCost, rooms, locations, ratings, prices)
