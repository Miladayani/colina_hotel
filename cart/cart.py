from django.contrib import messages

from rooms.models import Room


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request

        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, room, quantity=1, replace_current_quantity=False,
            arrival_date=None, departure_date=None,
            adults=0, children=0, infants=0, totally_price=0, nights=None):

        room_id = str(room.id)

        if room_id not in self.cart:
            self.cart[room_id] = {
                'quantity': 0,
                'arrival_date': arrival_date,
                'departure_date': departure_date,
                'adults': adults,
                'children': children,
                'infants': infants,
                'totally_price': totally_price,
                'nights': nights,
            }

        if replace_current_quantity:
            self.cart[room_id]['quantity'] = quantity
        else:
            self.cart[room_id]['quantity'] += quantity

        self.cart[room_id]['arrival_date'] = arrival_date or self.cart[room_id]['arrival_date']
        self.cart[room_id]['departure_date'] = departure_date or self.cart[room_id]['departure_date']
        self.cart[room_id]['adults'] = adults or self.cart[room_id]['adults']
        self.cart[room_id]['children'] = children or self.cart[room_id]['children']
        self.cart[room_id]['infants'] = infants or self.cart[room_id]['infants']
        self.cart[room_id]['nights'] = nights or self.cart[room_id]['nights']
        self.cart[room_id]['totally_price'] = totally_price or self.cart[room_id]['totally_price']

        self.save()

    def remove(self, room):
        """
        Remove a room from the cart
        """
        room_id = str(room.id)

        if room_id in self.cart:
            del self.cart[room_id]

        messages.success(self.request, 'Room successfully removed from Cart')

        self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        room_ids = self.cart.keys()
        rooms = Room.objects.filter(id__in=room_ids)

        cart = self.cart.copy()

        for room in rooms:
            cart[str(room.id)]['room_obj'] = room

        for item in cart.values():
            item['total_price'] = item['room_obj'].price_per_night * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    # def get_total(self):
    #     room_ids = self.cart.keys()
    #
    #     return sum(item['totally_price'] for item in self.cart.values())

    def is_empty(self):
        if self.cart:
            return False
        return True
