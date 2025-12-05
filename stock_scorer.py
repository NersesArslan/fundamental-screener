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
            'price': False,  # Debatable, but generally lower price = better value
            'pe_ratio': False,  # Lower P/E = better value
            'debt_to_equity': False,  # Lower debt = better
            'revenue_cagr_3year': True,  # Higher growth = better
            'returnonequity': True,  # Higher ROE = better
            'free_cashflow': True,  # Higher FCF = better
            'fcf_yield': True,  # Higher yield = better
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
        # Filter out None values
        valid_values = [v for v in values if v is not None]
        
        if len(valid_values) == 0:
            return [None] * len(values)
        
        min_val = min(valid_values)
        max_val = max(valid_values)
        
        # Avoid division by zero
        if max_val == min_val:
            return [50.0 if v is not None else None for v in values]
        
        normalized = []
        for v in values:
            if v is None:
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
        valid_values = [v for v in values if v is not None]
        
        if len(valid_values) < 2:
            return [50.0 if v is not None else None for v in values]
        
        mean = sum(valid_values) / len(valid_values)
        variance = sum((v - mean) ** 2 for v in valid_values) / len(valid_values)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return [50.0 if v is not None else None for v in values]
        
        normalized = []
        for v in values:
            if v is None:
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
        if not stocks_data:
            return {}
        
        tickers = list(stocks_data.keys())
        scores = {ticker: 0.0 for ticker in tickers}
        
        # For each metric in weights, normalize and apply weight
        for metric_key, weight in self.weights.items():
            if weight == 0:
                continue
            
            # Extract values for this metric across all stocks
            values = [stocks_data[ticker].get(metric_key) for ticker in tickers]
            
            # Fill missing values with median if requested
            if fill_missing_with_median:
                valid_values = [v for v in values if v is not None]
                if valid_values:
                    median = sorted(valid_values)[len(valid_values) // 2]
                    values = [v if v is not None else median for v in values]
            
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
                    
                if normalized[i] is not None:
                    scores[ticker] += normalized[i] * weight
                else:
                    # If metric is missing, set score to None (incomplete data)
                    scores[ticker] = None
        
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
