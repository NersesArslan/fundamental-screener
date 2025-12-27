from typing import Dict, List, Optional
import pandas as pd

# ============================================================================
# SCORING SYSTEM - Normalize metrics and calculate weighted scores
# ============================================================================

class StockScorer:
    """
    Normalizes metrics and calculates weighted composite scores.
    
    Usage:
        weights = {'pe_ratio': 0.2, 'returnonequity': 0.3, ...}
        scorer = StockScorer(weights)
        scores = scorer.calculate_scores(stocks_data)
    """
    
    def __init__(self, weights: Dict[str, float], normalization: str = 'minmax'):
        """
        Args:
            weights: Dict mapping metric_key to weight (should sum to 1.0)
            normalization: 'minmax' (0-100 scale) or 'zscore' (standard deviations)
        """
        self.weights = weights
        self.normalization = normalization
        
        # Define which metrics are "higher is better"
        # Lower is better metrics will be inverted during scoring
        self.higher_is_better = {
            # Core metrics
            'ev_to_fcf': False,  # Lower is better - cheaper valuation
            'revenue_cagr': True,  # Higher is better - faster growth
            'operating_margin': True,  # Higher is better - more efficient operations
            'fcf_margin': True,  # Higher is better - better cash generation
            'net_debt_to_ebitda': False,  # Lower is better - less leveraged
            'interest_coverage': True,  # Higher is better - safer debt servicing
            
            # Industry-specific metrics (semis)
            'capex_intensity': False,  # Lower is better - more capital efficient
            'inventory_turnover': True,  # Higher is better - better working capital management
            'gross_margin': True,  # Higher is better - pricing power
            
            # Industry-specific metrics (tech)
            'rnd_intensity': True,  # Higher is better - more innovation investment (context-dependent)
            'net_debt_to_fcf': False,  # Lower is better - less debt burden
            
            # Shared business model metrics
            'revenue_per_employee': True,  # Higher is better - more efficient per person
            'rule_of_40': True,  # Higher is better - growth + profitability
        }
        
        # Validate weights sum to ~1.0
        weight_sum = sum(weights.values())
        if not (0.99 <= weight_sum <= 1.01):
            print(f"⚠️  Warning: Weights sum to {weight_sum:.3f}, not 1.0")
    
    def normalize_minmax(self, values: List[float], higher_is_better: bool) -> List[float]:
        """
        Normalize to 0-100 scale using min-max scaling.
        
        Args:
            values: List of metric values for all stocks
            higher_is_better: If False, inverts the scale (lower values get higher scores)
        """
        import math
        
        # Filter out None and NaN values
        valid_values = [v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
        
        if len(valid_values) == 0:
            return [None] * len(values)
        
        min_val = min(valid_values)
        max_val = max(valid_values)
        
        # Avoid division by zero
        if max_val == min_val:
            return [50.0 if v is not None and not (isinstance(v, float) and math.isnan(v)) else None for v in values]
        
        normalized = []
        for v in values:
            if v is None or (isinstance(v, float) and math.isnan(v)):
                normalized.append(None)
            else:
                # Scale to 0-100
                score = ((v - min_val) / (max_val - min_val)) * 100
                
                # Invert if lower is better
                if not higher_is_better:
                    score = 100 - score
                
                normalized.append(score)
        
        return normalized
    
    def normalize_zscore(self, values: List[float], higher_is_better: bool) -> List[float]:
        """
        Normalize using z-scores (standard deviations from mean).
        Then scale to 0-100 range for consistency.
        """
        import math
        
        # Filter out None and NaN values
        valid_values = [v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
        
        if len(valid_values) < 2:
            return [50.0 if v is not None and not (isinstance(v, float) and math.isnan(v)) else None for v in values]
        
        mean = sum(valid_values) / len(valid_values)
        variance = sum((v - mean) ** 2 for v in valid_values) / len(valid_values)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return [50.0 if v is not None and not (isinstance(v, float) and math.isnan(v)) else None for v in values]
        
        normalized = []
        for v in values:
            if v is None or (isinstance(v, float) and math.isnan(v)):
                normalized.append(None)
            else:
                # Calculate z-score
                z = (v - mean) / std_dev
                
                # Invert if lower is better
                if not higher_is_better:
                    z = -z
                
                # Scale to 0-100 (z-scores typically range -3 to +3)
                # Map -3 → 0, 0 → 50, +3 → 100
                score = 50 + (z * 16.67)  # 50/3 ≈ 16.67
                score = max(0, min(100, score))  # Clamp to 0-100
                
                normalized.append(score)
        
        return normalized
    
    def calculate_scores(self, stocks_data: Dict[str, Dict], fill_missing_with_median: bool = True) -> Dict[str, Optional[float]]:
        """
        Calculate weighted composite scores for all stocks.
        
        Args:
            stocks_data: Dict of {ticker: {metric_key: value}}
            fill_missing_with_median: If True, replaces None values with peer group median
        
        Returns:
            Dict of {ticker: total_score} (0-100 scale)
        """
        import math
        
        if not stocks_data:
            return {}
        
        tickers = list(stocks_data.keys())
        scores = {ticker: 0.0 for ticker in tickers}
        
        # Track actual weights used per stock (for N/A metric redistribution)
        actual_weights = {ticker: 0.0 for ticker in tickers}
        
        # For each metric in weights, normalize and apply weight
        for metric_key, weight in self.weights.items():
            if weight == 0:
                continue
            
            # Extract values for this metric across all stocks
            values = [stocks_data[ticker].get(metric_key) for ticker in tickers]
            
            # Separate NaN (N/A - Case 1) from None (Missing - Case 2)
            # For median calculation, exclude both NaN and None
            valid_values = [v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
            # If the metric has no valid values across the peer group, skip it entirely
            if len(valid_values) == 0:
                continue

            if fill_missing_with_median and valid_values:
                median = sorted(valid_values)[len(valid_values) // 2]
                # Only impute None values (Case 2), leave NaN as-is (Case 1)
                values = [v if v is not None and not (isinstance(v, float) and math.isnan(v)) else (median if v is None else v) for v in values]
            
            # Determine direction
            higher_better = self.higher_is_better.get(metric_key, True)
            
            # Normalize
            if self.normalization == 'zscore':
                normalized = self.normalize_zscore(values, higher_better)
            else:
                normalized = self.normalize_minmax(values, higher_better)
            
            # Apply weight to each stock's score
            for i, ticker in enumerate(tickers):
                # Skip if this stock's score is already None (failed earlier metric)
                if scores[ticker] is None:
                    continue
                
                # Check if this metric is N/A (NaN) for this stock
                value = values[i]
                if isinstance(value, float) and math.isnan(value):
                    # Case 1: N/A - skip this metric, don't add its weight
                    continue
                    
                if normalized[i] is not None:
                    scores[ticker] += normalized[i] * weight
                    actual_weights[ticker] += weight
                else:
                    # If metric is missing after imputation, set score to None (incomplete data)
                    scores[ticker] = None
        
        # Redistribute N/A metric weights proportionally
        # Since normalized scores are 0-100 and we multiply by weight (0-1),
        # we need to normalize by actual_weights to maintain 0-100 scale
        for ticker in tickers:
            if scores[ticker] is not None and actual_weights[ticker] > 0:
                # Redistribute: scale up the score proportionally to account for skipped metrics
                scores[ticker] = scores[ticker] / actual_weights[ticker]
        
        return scores
    
    def get_detailed_scores(self, stocks_data: Dict[str, Dict]) -> pd.DataFrame:
        """
        Return a detailed breakdown showing normalized scores for each metric.
        Useful for understanding why a stock got its score.
        
        Returns:
            DataFrame with columns for each metric's normalized score + total
        """
        if not stocks_data:
            return pd.DataFrame()
        
        tickers = list(stocks_data.keys())
        detailed = {ticker: {} for ticker in tickers}
        
        # Calculate normalized score for each metric
        for metric_key, weight in self.weights.items():
            values = [stocks_data[ticker].get(metric_key) for ticker in tickers]
            higher_better = self.higher_is_better.get(metric_key, True)
            
            if self.normalization == 'zscore':
                normalized = self.normalize_zscore(values, higher_better)
            else:
                normalized = self.normalize_minmax(values, higher_better)
            
            for i, ticker in enumerate(tickers):
                detailed[ticker][f"{metric_key}_score"] = normalized[i]
        
        # Add total scores
        total_scores = self.calculate_scores(stocks_data)
        for ticker in tickers:
            detailed[ticker]['total_score'] = total_scores[ticker]
        
        df = pd.DataFrame(detailed).T
        df.index.name = 'Ticker'
        return df
