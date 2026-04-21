from typing import Dict, Optional
from domain.card import Card

class CardRepositoryImpl:
    def __init__(self) -> None:
        self.cardStore: Dict[str, Card] = {}

    def save(self, card: Card) -> Card:
        self.cardStore[card.getId()] = card
        return card

    def findById(self, cardId: str) -> Optional[Card]:
        return self.cardStore.get(cardId)

    def updatePinRetries(self, cardId: str, retriesLeft: int) -> None:
        card = self.findById(cardId)
        if card is not None:
            card.setPinRetriesLeft(retriesLeft)

    def blockCard(self, cardId: str) -> None:
        card = self.findById(cardId)
        if card is not None:
            card.setBlocked(True)
