"""
Comprehensive list of semiconductor companies by sub-industry.
"""

industry_categories = {
    # Semiconductor Foundries (contract manufacturing)
    "foundries": [
        "TSM",      # TSMC (Taiwan Semiconductor Manufacturing Company)
        "UMC",      # United Microelectronics Corporation
        # "SSNLF",  # Samsung (OTC, not primary listing)
        # GlobalFoundries is private
    ],
    
    # Fabless Designers (design chips, outsource manufacturing)
    "fabless_designers": [
        "NVDA",     # NVIDIA
        "AMD",      # Advanced Micro Devices
        "QCOM",     # Qualcomm
        "AVGO",     # Broadcom
        "MRVL",     # Marvell Technology
        "MPWR",     # Monolithic Power Systems
        "MCHP",     # Microchip Technology (also has fabs, but primarily fabless)
        "QRVO",     # Qorvo (RF semiconductors)
        "SWKS",     # Skyworks Solutions (RF semiconductors)
        "XLNX",     # Xilinx (acquired by AMD, but may still trade)
        "ARMH",     # ARM Holdings
        "SLAB",     # Silicon Laboratories
        "ALGM",     # Allegro MicroSystems
        "MTSI",     # MACOM Technology Solutions
    ],
    
    # Semiconductor Equipment (tools for chip manufacturing)
    "equipment": [
        "ASML",     # ASML Holding (lithography equipment)
        "LRCX",     # Lam Research (etch/deposition)
        "KLAC",     # KLA Corporation (inspection/metrology)
        "AMAT",     # Applied Materials (deposition/etch/inspection)
        "ENTG",     # Entegris (materials/contamination control)
        "MKSI",     # MKS Instruments
        "ACLS",     # Axcelis Technologies (ion implantation)
        "UCTT",     # Ultra Clean Holdings
        "ICHR",     # Ichor Holdings
        "COHU",     # Cohu (test/handling equipment)
        "FORM",     # FormFactor (probe cards/test)
        "ONTO",     # Onto Innovation (process control)
        "NVMI",     # Nova (metrology)
        "CAMT",     # Camtek (inspection)
    ],
    
    # IDMs - Integrated Device Manufacturers (design + manufacture)
    "idms": [
        "INTC",     # Intel
        "TXN",      # Texas Instruments
        "NXPI",     # NXP Semiconductors
        "STM",      # STMicroelectronics
        "MCHP",     # Microchip Technology (hybrid IDM/fabless)
        "ADI",      # Analog Devices
        "ON",       # ON Semiconductor
        "MU",       # Micron Technology (memory)
        "SSNLF",    # Samsung (memory, foundry - OTC)
        "WDC",      # Western Digital (memory/storage)
        "PSTG",     # Pure Storage (enterprise storage)
        "WOLF",     # Wolfspeed (SiC/GaN power semiconductors)
        "CRUS",     # Cirrus Logic
        "SIMO",     # Silicon Motion Technology
        "DIOD",     # Diodes Incorporated
        "MXL",      # MaxLinear
        "SMTC",     # Semtech
        "RMBS",     # Rambus (memory interface)
    ],
    
    # Memory (specialized IDMs)
    "memory": [
        "MU",       # Micron Technology
        "WDC",      # Western Digital
        "STX",      # Seagate Technology
        "SSNLF",    # Samsung (OTC)
        # SK Hynix (not easily traded in US)
    ],
    
    # All Semiconductors Combined
    "semiconductors": [
        # Foundries
        "TSM", "UMC",
        # Fabless
        "NVDA", "AMD", "QCOM", "AVGO", "MRVL", "MPWR", "MCHP", "QRVO", "SWKS",
        "ARMH", "SLAB", "ALGM", "MTSI",
        # Equipment
        "ASML", "LRCX", "KLAC", "AMAT", "ENTG", "MKSI", "ACLS", "UCTT",
        "ICHR", "COHU", "FORM", "ONTO", "NVMI", "CAMT",
        # IDMs
        "INTC", "TXN", "NXPI", "STM", "ADI", "ON", "MU",
        "WOLF", "CRUS", "SIMO", "DIOD", "MXL", "SMTC", "RMBS",
        # Memory
        "WDC", "STX",
    ],
    
    # ============================
    # CLOUD INFRASTRUCTURE (IaaS)
    # ============================
    "cloud_infrastructure": [
        "AMZN",   # AWS
        "MSFT",   # Azure
        "GOOGL",  # Google Cloud
        "IBM",    # IBM Cloud
        "ORCL",   # Oracle Cloud
    ],

    # ============================
    # CLOUD SaaS (Enterprise SaaS)
    # ============================
    "enterprise_saas": [
        "ADBE",   # Adobe
        "INTU",   # Intuit
        "WDAY",   # Workday
        "NOW",    # ServiceNow
        "TEAM",   # Atlassian
        "HUBS",   # HubSpot
        "CRM",    # Salesforce
    ],

    # ============================
    # VERTICAL SaaS (Industry-specific)
    # ============================
    "vertical_saas": [
        "SHOP",   # Shopify – e-commerce merchants
        "TOST",   # Toast – restaurants
        "VEEV",   # Veeva – life sciences
        "ADSK",   # Autodesk – engineering/design
    ],

    # ============================
    # AD PLATFORM / DIGITAL MEDIA
    # ============================
    "ad_platform": [
        "META",   # Meta Ads + Instagram Ads
        "GOOGL",  # Google Search + YouTube Ads
        "PINS",   # Pinterest Ads
        "SNAP",   # Snapchat Ads
    ],

    # ============================
    # STREAMING / DIGITAL CONTENT
    # ============================
    "streaming": [
        "NFLX",   # Netflix
        "DIS",    # Disney+
        "PARA",   # Paramount+
        "WBD",    # Max / HBO
        "SPOT",   # Spotify
    ],

    # ============================
    # CONSUMER HARDWARE + ECOSYSTEMS
    # ============================
    "hardware_ecosystem": [
        "AAPL",   # iPhone / Mac / Wearables
        "SONY",   # PlayStation ecosystem
        "GOOGL",  # Pixel / Android ecosystem
        "META",   # VR hardware (Quest)
    ],

    # ============================
    # ENTERPRISE AI / DATA ANALYTICS
    # ============================
    "enterprise_ai": [
        "PLTR",   # Palantir
        "SNOW",   # Snowflake AI Cloud
        "DDOG",   # Datadog (Observability + AI)
        "MDB",    # MongoDB (data platform)
        "ZS",     # Zscaler AI Security
    ],

    # ============================
    # CYBERSECURITY
    # ============================
    "cybersecurity": [
        "CRWD",   # CrowdStrike
        "PANW",   # Palo Alto Networks
        "FTNT",   # Fortinet
        "OKTA",   # Identity security
        "S",      # SentinelOne
    ],

    # ============================
    # LEGACY ENTERPRISE TECH
    # ============================
    "legacy_enterprise": [
        "IBM",
        "ORCL",
        "CSCO",
        "HPE",
    ],
}



# Sub-industry mappings for easy access
FOUNDRIES = industry_categories["foundries"]
FABLESS = industry_categories["fabless_designers"]
EQUIPMENT = industry_categories["equipment"]
IDMS = industry_categories["idms"]
MEMORY = industry_categories["memory"]
ALL_SEMIS = industry_categories["semiconductors"]

# Big Tech Business Model Mappings
CLOUD_INFRASTRUCTURE = industry_categories["cloud_infrastructure"]
ENTERPRISE_SAAS = industry_categories["enterprise_saas"]
VERTICAL_SAAS = industry_categories["vertical_saas"]
AD_PLATFORM = industry_categories["ad_platform"]
STREAMING = industry_categories["streaming"]
HARDWARE_ECOSYSTEM = industry_categories["hardware_ecosystem"]
ENTERPRISE_AI = industry_categories["enterprise_ai"]
CYBERSECURITY = industry_categories["cybersecurity"]
LEGACY_ENTERPRISE = industry_categories["legacy_enterprise"]