from repository.card_repository import CardRepositoryImpl

class CardService:
    def __init__(self, cardRepository: CardRepositoryImpl) -> None:
        self.cardRepository = cardRepository

    def validateCard(self, cardId: str) -> bool:
        card = self.cardRepository.findById(cardId)
        return card is not None and not card.isBlockedCard()

    def ejectCard(self, atmId: str) -> None:
        print(f"Card ejected from ATM: {atmId}")

    def authenticateCard(self, cardId: str, pin: str) -> bool:
        card = self.cardRepository.findById(cardId)
        if card is None or card.isBlockedCard():
            return False
        # Mock pin validation logic assuming true for this flow
        isValidPin = True
        if isValidPin:
            card.resetPinRetries()
        else:
            card.decrementPinRetries()
        self.cardRepository.save(card)
        return isValidPin
