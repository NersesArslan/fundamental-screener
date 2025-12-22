# experiments/run_business_model.py

from core.stock_screener import StockScreener
from core.stock_scorer import StockScorer
from core.screener_output import format_screener_output

def run_business_model_test(
    *,
    name: str,
    tickers: list[str],
    provider,
    core_metrics: list,
    bm_metrics: list,
    weight_map: dict,
    normalization: str = "minmax",
    verbose: bool = True,
):
    print("\n" + "=" * 70)
    print(f"BUSINESS MODEL TEST — {name}")
    print("=" * 70)

    # 1. Build screener with explicit metrics
    screener = StockScreener(
        provider=provider,
        metrics=core_metrics + bm_metrics
    )

    # 2. Fetch data
    stocks_data = screener.screen_multiple(tickers, verbose=verbose)

    # 3. Display raw metrics
    metric_names = screener.get_metric_names()
    df = format_screener_output(stocks_data, metric_names)
    print("\nRaw Fundamentals:")
    print(df.to_string())

    # 4. Score
    scorer = StockScorer(weight_map, normalization=normalization)
    scores = scorer.calculate_scores(stocks_data)

    # 5. Rank
    ranked = sorted(
        scores.items(),
        key=lambda x: x[1] if x[1] is not None else -1,
        reverse=True,
    )

    print("\nRanking:")
    for rank, (ticker, score) in enumerate(ranked, 1):
        if score is not None:
            print(f"  {rank}. {ticker:6} - Score: {score:.1f}/100")
        else:
            print(f"  {rank}. {ticker:6} - Score: N/A")

    return {
        "raw": stocks_data,
        "scores": scores,
        "ranking": ranked,
    }
