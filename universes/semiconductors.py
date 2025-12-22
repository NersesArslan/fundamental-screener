FOUNDRIES = [
    "TSM",
    "UMC",
]

FABLESS = [
    "NVDA", "AMD", "QCOM", "AVGO", "MRVL", "MPWR",
    "MCHP", "QRVO", "SWKS", "ARM", "SLAB", "ALGM",
    "MTSI", "CRUS", "SIMO", "MXL", "RMBS",
]

EQUIPMENT = [
    "ASML", "LRCX", "KLAC", "AMAT", "ENTG", "MKSI",
    "ACLS", "UCTT", "ICHR", "COHU", "FORM", "ONTO",
    "NVMI", "CAMT",
]

IDMS = [
    "INTC", "TXN", "NXPI", "STM", "ADI", "ON",
    "MU", "WOLF",
]

MEMORY = [
    "MU", "WDC", "STX",
]

ALL_SEMICONDUCTORS = sorted(
    set(
        FOUNDRIES
        + FABLESS
        + EQUIPMENT
        + IDMS
        + MEMORY
    )
)

SEMICONDUCTORS = {
    "foundries": FOUNDRIES,
    "fabless": FABLESS,
    "equipment": EQUIPMENT,
    "idms": IDMS,
    "memory": MEMORY,
    "all": ALL_SEMICONDUCTORS,
}
