from Bank_system.model.card import Card

class CardService:


    def add_card(self):
        c = Card.create()
        return c.number


    def blocked_card(self, num_card):
        Card.delete().where(Card.number == num_card)