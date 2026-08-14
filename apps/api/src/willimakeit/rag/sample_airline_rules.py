from datetime import date

from willimakeit.schemas.rag_pipeline import AirlineRuleChunk

WIZZ_RULES = [
    AirlineRuleChunk(
        airline_code="W6",
        section="Carry-on bag",
        content=(
            "Every Wizz Air passenger is allowed to bring one carry-on bag "
            "on board for free. The bag may weigh up to 10 kg and must be "
            "40 x 30 x 20 cm. Wheels are allowed but not mandatory. "
            "The bag must fit under the seat in front of the passenger. "
            "It can be a laptop bag, woman's purse, or small backpack."
        ),
        effective_date=date(2026, 8, 14),
    ),
    AirlineRuleChunk(
        airline_code="W6",
        section="Trolley bag",
        content=(
            "A Wizz Air trolley bag may weigh up to 10 kg and must be "
            "55 x 40 x 23 cm. A trolley bag is available for purchase "
            "with WIZZ Priority and must fit in the overhead compartment. "
            "With WIZZ Priority, passengers can bring a total of two "
            "pieces of baggage on board: the free carry-on bag and the trolley bag."
        ),
        effective_date=date(2026, 8, 14),
    ),
    AirlineRuleChunk(
        airline_code="W6",
        section="Checked-in bag",
        content=(
            "Wizz Air checked baggage is available in 10 kg, 20 kg, "
            "26 kg, or 32 kg options. The maximum dimensions are "
            "149 x 119 x 171 cm. Up to 6 checked bags can be purchased "
            "per passenger. Checked baggage is purchased separately."
        ),
        effective_date=date(2026, 8, 14),
    ),
    AirlineRuleChunk(
        airline_code="W6",
        section="Baggage purchase",
        content=(
            "Wizz Air baggage can be added by choosing a bundle such as "
            "WIZZ GO or WIZZ PLUS during booking, adding baggage when "
            "making a reservation, adding baggage after booking through "
            "the WIZZ Account or Call Centre, or purchasing baggage at "
            "the airport. Additional fees apply when baggage is purchased "
            "at the airport."
        ),
        effective_date=date(2026, 8, 14),
    ),
    AirlineRuleChunk(
        airline_code="W6",
        section="General baggage rules",
        content=(
            "Wizz Air baggage is divided into cabin baggage and checked-in "
            "baggage. Cabin baggage includes the free carry-on bag and "
            "trolley bag. All baggage options have size and weight limits, "
            "and exceeding these limits incurs additional fees. The passenger "
            "is responsible for checking the list of restricted items for "
            "both onboard and checked baggage before packing."
        ),
        effective_date=date(2026, 8, 14),
    ),
]


RYANAIR_RULES = [
    AirlineRuleChunk(
        airline_code="FR",
        section="Personal bag",
        content=(
            "All Ryanair fares include one small personal bag free of charge. "
            "The bag must be 40 x 30 x 20 cm and fit under the seat in front "
            "of the passenger. Examples include a handbag or laptop bag."
        ),
        effective_date=date(2026, 8, 14),
    ),
    AirlineRuleChunk(
        airline_code="FR",
        section="Priority and cabin baggage",
        content=(
            "Ryanair Priority & 2 Cabin Bags allows passengers to bring a "
            "small personal bag measuring 40 x 30 x 20 cm plus a 10 kg cabin "
            "bag measuring 55 x 40 x 20 cm. The larger bag is stored in the "
            "overhead locker. Priority also allows passengers to board using "
            "the Priority Boarding queue at the gate."
        ),
        effective_date=date(2026, 8, 14),
    ),
    AirlineRuleChunk(
        airline_code="FR",
        section="Checked baggage",
        content=(
            "Ryanair offers 10 kg, 20 kg, and 23 kg checked baggage options. "
            "A 10 kg Check-in Bag must be dropped at the airport check-in desk "
            "before security and is placed in the aircraft hold. Passengers "
            "can purchase up to 3 checked bags of 20 kg. Passengers can "
            "purchase up to 1 checked bag of 23 kg."
        ),
        effective_date=date(2026, 8, 14),
    ),
    AirlineRuleChunk(
        airline_code="FR",
        section="Infant baggage",
        content=(
            "Ryanair allows passengers travelling with an infant to carry "
            "2 items of baby equipment free of charge per child. There is "
            "no cabin bag allowance for an infant aged 8 days to 23 months "
            "inclusive. A baby bag of up to 5 kg is allowed for babies "
            "travelling on an adult's lap. The baby bag must be no larger "
            "than 45 x 35 x 20 cm."
        ),
        effective_date=date(2026, 8, 14),
    ),
    AirlineRuleChunk(
        airline_code="FR",
        section="Additional baggage options",
        content=(
            "Ryanair offers additional baggage options for passengers who "
            "need more allowance than the standard personal bag included "
            "with every fare. Options include Priority & 2 Cabin Bags and "
            "10 kg, 20 kg, or 23 kg checked bags."
        ),
        effective_date=date(2026, 8, 14),
    ),
]


AIRLINE_RULES = WIZZ_RULES + RYANAIR_RULES
