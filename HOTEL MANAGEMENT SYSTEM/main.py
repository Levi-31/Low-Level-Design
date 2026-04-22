


import time
import uuid

from controller.admin_controller import AdminController
from controller.booking_controller import BookingController
from controller.dashboard_controller import DashboardController
from controller.search_controller import SearchController
from controller.transaction_controller import TransactionController
from domain.cancellation_policy import CancellationPolicy
from domain.date_range import DateRange
from domain.hotel import Hotel
from domain.room import Room
from domain.room_type import RoomType
from domain.transaction_status import TransactionStatus
from domain.user import User
from domain.user_role import UserRole
from repository.implementation.booking_repository_implementation import BookingRepositoryImpl
from repository.implementation.cancellation_policy_repository_implementation import CancellationPolicyRepositoryImpl
from repository.implementation.hotel_repository_implementation import HotelRepositoryImpl
from repository.implementation.room_repository_implementation import RoomRepositoryImpl
from repository.implementation.room_type_repository_implementation import RoomTypeRepositoryImpl
from repository.implementation.seasonal_price_repository_implementation import SeasonalPriceRepositoryImpl
from repository.implementation.transaction_repository_implementation import TransactionRepositoryImpl
from repository.implementation.user_repository_implementation import UserRepositoryImpl
from service.booking_service import BookingService
from service.inventory_service import InventoryService
from service.policy_service import PolicyService
from service.pricing_service import PricingService
from service.search_service import SearchService
from service.transaction_service import TransactionService
from service.user_service import UserService


def main():
    print("=== HOTEL MANAGEMENT SYSTEM SIMULATION ===\n")

    # Initialize repositories
    hotel_repository = HotelRepositoryImpl()
    room_type_repository = RoomTypeRepositoryImpl()
    room_repository = RoomRepositoryImpl()
    booking_repository = BookingRepositoryImpl()
    transaction_repository = TransactionRepositoryImpl()
    seasonal_price_repository = SeasonalPriceRepositoryImpl()
    cancellation_policy_repository = CancellationPolicyRepositoryImpl()
    user_repository = UserRepositoryImpl()

    # Initialize services
    pricing_service = PricingService(room_type_repository, seasonal_price_repository)
    inventory_service = InventoryService(booking_repository, hotel_repository, room_type_repository)
    policy_service = PolicyService()
    transaction_service = TransactionService(transaction_repository, booking_repository, inventory_service)
    booking_service = BookingService(
        booking_repository, hotel_repository, room_type_repository, user_repository,
        inventory_service, pricing_service, policy_service, cancellation_policy_repository, transaction_service)
    search_service = SearchService(
        hotel_repository, room_type_repository, room_repository, pricing_service, booking_repository)
    user_service = UserService(booking_repository)

    # Initialize controllers
    search_controller = SearchController(search_service)
    booking_controller = BookingController(booking_service)
    transaction_controller = TransactionController(transaction_service)
    admin_controller = AdminController(
        hotel_repository, room_type_repository, room_repository,
        seasonal_price_repository, cancellation_policy_repository, booking_service)
    dashboard_controller = DashboardController(user_service)

    import pdb;pdb.set_trace()
    # Simulation
    print("1. Creating cancellation policy...\n\n\n")
    flex_policy = CancellationPolicy(
        id=str(uuid.uuid4()), name="FLEX", refund_percent=100, 
        cutoff_hours_before_check_in=24, created_at=int(time.time() * 1000))
    flex_policy = admin_controller.create_or_update_policy(flex_policy)
    print(f"Created policy: {flex_policy}\n\n\n")

    print("\n2. Creating hotel...\n\n")
    hotel = Hotel(
        id=str(uuid.uuid4()), name="Grand Hotel", address="123 Main St",
        city="New York", country="USA", lat=40.7128, lng=-74.0060, rating=4.5, is_active=True,
        default_overbook_percent=10, cancellation_policy_id=flex_policy.id, 
        created_at=int(time.time() * 1000))
    hotel = admin_controller.create_or_update_hotel(hotel)
    print(f"Created hotel: {hotel}")

    print("\n3. Creating room type...\n\n\n")
    deluxe_king = RoomType(
        id=str(uuid.uuid4()), hotel_id=hotel.id, name="Deluxe King",
        capacity=2, bed_type="KING", base_price=10000,
        amenities=["WiFi", "TV", "Mini Bar"], total_rooms=10, is_active=True,
        created_at=int(time.time() * 1000))
    deluxe_king = admin_controller.create_or_update_room_type(deluxe_king)
    print(f"Created room type: {deluxe_king}\n\n\n")

    print("\n4. Creating user...\n\n\n")
    customer = User(
        id=str(uuid.uuid4()), name="Vikky", email="vikky@example.com",
        role=UserRole.CUSTOMER, created_at=int(time.time() * 1000))
    customer = user_repository.save(customer)
    print(f"Created user: {customer}")

    print("\n5. Setting seasonal price...\n\n\n")
    tomorrow = int(time.time() * 1000) + 86400000
    seasonal_price = admin_controller.set_seasonal_price(
        hotel.id, deluxe_king.id, tomorrow, 15000)
    print(f"Set seasonal price: {seasonal_price}")

    print("\n6. Checking availability...")
    date_range = DateRange(tomorrow, tomorrow + 2 * 86400000)
    available_room_types = search_controller.get_availability(hotel.id, date_range)
    print(f"Found {len(available_room_types)} available room type(s):")
    for rta in available_room_types:
        print(f"  - {rta.room_type_name} (Capacity: {rta.capacity}, Bed: {rta.bed_type}, Price: {rta.total_price})")

    print("\n7. Creating booking...")
    booking = None
    if not available_room_types:
        print("No available room types for booking")
    else:
        selected_rta = available_room_types[0]
        booking = booking_controller.create_booking(
            customer.id, hotel.id, selected_rta.room_type_id, date_range,
            selected_rta.total_price)
        print(f"Created booking: {booking}")

    if booking:
        print("\n8. Initiating transaction...")
        transaction = transaction_controller.initiate_transaction(booking.id)
        print(f"Transaction initiated: {transaction}")

        print("\n9. Simulating payment success callback...")
        transaction_controller.handle_transaction_callback(transaction.provider_ref, TransactionStatus.COMPLETED)
        print("Payment completed, booking confirmed")

        print("\n10. Admin checking in guest...")
        room = Room(
            id=str(uuid.uuid4()), hotel_id=hotel.id, room_type_id=booking.room_type_id,
            room_number="101", is_active=True, created_at=int(time.time() * 1000))
        room = room_repository.save(room)
        checked_in_booking = admin_controller.check_in(booking.id, room.id, int(time.time() * 1000))
        print(f"Guest checked in: {checked_in_booking}")

        print("\n11. Admin checking out guest (early check-out)...")
        checked_out_booking = admin_controller.check_out(booking.id, int(time.time() * 1000) + 86400000)
        print(f"Guest checked out: {checked_out_booking}")

    print("\n12. Viewing user dashboard...")
    user_bookings = dashboard_controller.list_user_bookings(customer.id)
    print(f"User bookings: {len(user_bookings)} booking(s)")

    print("\n=== SIMULATION COMPLETED ===")

if __name__ == "__main__":
    main()
