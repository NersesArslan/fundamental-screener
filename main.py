# main.py

from core.stock_providers import YFinanceProvider
from experiments.run_business_model import run_business_model_test
from metrics.core_metrics import get_core_metrics
from universes. semiconductors import ALL_SEMICONDUCTORS
# ============================================================================
# CONFIGURATION: Change this to test different business models
# ============================================================================
ACTIVE_MODEL = "streaming"  # Options: "cybersecurity", "ad_platform", 
                                 # "cloud_infrastructure", "enterprise_saas",
                                 # "enterprise_ai", "hardware_ecosystem",
                                 # "legacy_enterprise", "streaming"
# ============================================================================

# Business model configurations
BUSINESS_MODELS = {
    "cybersecurity": {
        "universe": "universes.cybersecurity",
        "universe_var": "CYBERSECURITY",
        "metrics": "metrics.business_models.cybersecurity",
        "metrics_func": "get_cybersecurity_metrics",
        "weights": "industry.business_model_weights.cybersecurity",
        "weights_var": "CYBERSECURITY_WEIGHT_MAP",
    },
    "ad_platform": {
        "universe": "universes.ad_platform",
        "universe_var": "AD_PLATFORM",
        "metrics": "metrics.business_models.ad_platform",
        "metrics_func": "get_ad_platform_metrics",
        "weights": "industry.business_model_weights.ad_platform",
        "weights_var": "AD_PLATFORM_WEIGHT_MAP",
    },
    "cloud_infrastructure": {
        "universe": "universes.cloud_infrastructure",
        "universe_var": "CLOUD_INFRASTRUCTURE",
        "metrics": "metrics.business_models.cloud_infrastructure",
        "metrics_func": "get_cloud_infrastructure_metrics",
        "weights": "industry.business_model_weights.cloud_infrastructure",
        "weights_var": "CLOUD_INFRASTRUCTURE_WEIGHT_MAP",
    },
    "enterprise_saas": {
        "universe": "universes.enterprise_saas",
        "universe_var": "ENTERPRISE_SAAS",
        "metrics": "metrics.business_models.enterprise_saas",
        "metrics_func": "get_saas_metrics",
        "weights": "industry.business_model_weights.enterprise_saas",
        "weights_var": "ENTERPRISE_SAAS_WEIGHT_MAP",
    },
    "enterprise_ai": {
        "universe": "universes.enterprise_ai",
        "universe_var": "ENTERPRISE_AI",
        "metrics": "metrics.business_models.enterprise_ai",
        "metrics_func": "get_enterprise_ai_metrics",
        "weights": "industry.business_model_weights.enterprise_ai",
        "weights_var": "ENTERPRISE_AI_WEIGHT_MAP",
    },
    "hardware_ecosystem": {
        "universe": "universes.hardware_ecosystem",
        "universe_var": "HARDWARE_ECOSYSTEM",
        "metrics": "metrics.business_models.hardware_ecosystem",
        "metrics_func": "get_hardware_ecosystem_metrics",
        "weights": "industry.business_model_weights.hardware_ecosystem",
        "weights_var": "HARDWARE_ECOSYSTEM_WEIGHT_MAP",
    },
    "legacy_enterprise": {
        "universe": "universes.legacy_enterprise",
        "universe_var": "LEGACY_ENTERPRISE",
        "metrics": "metrics.business_models.legacy_enterprise",
        "metrics_func": "get_legacy_enterprise_metrics",
        "weights": "industry.business_model_weights.legacy_enterprise",
        "weights_var": "LEGACY_ENTERPRISE_WEIGHT_MAP",
    },
    "streaming": {
        "universe": "universes.streaming",
        "universe_var": "STREAMING",
        "metrics": "metrics.business_models.streaming",
        "metrics_func": "get_streaming_metrics",
        "weights":"industry.business_model_weights.streaming",
        "weights_var": "STREAMING_WEIGHT_MAP"
    },
}


def load_business_model_components(model_name):
    """Dynamically load the components for a given business model."""
    if model_name not in BUSINESS_MODELS:
        raise ValueError(
            f"Unknown business model: {model_name}. "
            f"Available options: {', '.join(BUSINESS_MODELS.keys())}"
        )
    
    config = BUSINESS_MODELS[model_name]
    
    # Import universe
    universe_module = __import__(config["universe"], fromlist=[config["universe_var"]])
    tickers = getattr(universe_module, config["universe_var"])
    
    # Import metrics function
    metrics_module = __import__(config["metrics"], fromlist=[config["metrics_func"]])
    metrics_func = getattr(metrics_module, config["metrics_func"])
    
    # Import weights if available
    weight_map = None
    if config["weights"] and config["weights_var"]:
        try:
            weights_module = __import__(config["weights"], fromlist=[config["weights_var"]])
            weight_map = getattr(weights_module, config["weights_var"])
        except (ImportError, AttributeError):
            print(f"Warning: Weight map not found for {model_name}, using default weights")
    
    return tickers, metrics_func, weight_map


def main():
    provider = YFinanceProvider()
    
    # Load the active business model configuration
    tickers, metrics_func, weight_map = load_business_model_components(ACTIVE_MODEL)
    
    # Format the name for display
    display_name = ACTIVE_MODEL.replace("_", " ").title()
    
    run_business_model_test(
        name=display_name,
        tickers=tickers,
        provider=provider,
        core_metrics=get_core_metrics(),
        bm_metrics=metrics_func(),
        weight_map=weight_map,
        normalization="minmax",
        verbose=True,
    )


if __name__ == "__main__":
    main()

