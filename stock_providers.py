import yfinance as yf
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional, Dict, List

# ============================================================================
# DATA LAYER - Abstract away the data source
# ============================================================================

class StockDataProvider(ABC):
    """Abstract interface for fetching stock data. Swap implementations freely."""
    
    @abstractmethod
    def get_price(self, ticker: str) -> Optional[float]:
        """Current stock price."""
        pass
    
    @abstractmethod
    def get_quarterly_revenue(self, ticker: str) -> Optional[pd.Series]:
        """Quarterly revenue series (indexed by date, most recent first)."""
        pass
    
    @abstractmethod
    def get_fundamentals(self, ticker: str) -> Dict[str, Optional[float]]:
        """PE ratio, debt/equity, ROE, FCF, etc."""
        pass
    
    @abstractmethod
    def get_valuation_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Enterprise value, market cap, FCF for valuation metrics."""
        pass
    
    @abstractmethod
    def get_roic_components(self, ticker: str) -> Dict[str, Optional[float]]:
        """Operating income, tax rate, debt, equity, cash for ROIC calculation."""
        pass
    
    @abstractmethod
    def get_margin_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Operating income, revenue, FCF, cost of revenue for margin calculations."""
        pass
    
    @abstractmethod
    def get_leverage_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Debt, cash, EBITDA, EBIT, interest expense for leverage metrics."""
        pass
    
    @abstractmethod
    def get_capex_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """CapEx and revenue for intensity calculations."""
        pass
    
    @abstractmethod
    def get_inventory_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Inventory and cost of revenue for turnover calculations."""
        pass
    
    @abstractmethod
    def get_rnd_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """R&D expense and revenue for intensity calculations."""
        pass


class YFinanceProvider(StockDataProvider):
    """Use yfinance for all stock data - free and reliable."""
    
    def get_price(self, ticker: str) -> Optional[float]:
        try:
            return yf.Ticker(ticker).info.get('currentPrice')
        except:
            return None
    
    def get_quarterly_revenue(self, ticker: str) -> Optional[pd.Series]:
        """
        Fetch revenue data - uses TTM when enough quarterly data, otherwise annual.
        """
        try:
            # Get quarterly data
            quarterly_fin = yf.Ticker(ticker).quarterly_financials
            if quarterly_fin is None or 'Total Revenue' not in quarterly_fin.index:
                return None
            
            quarterly_rev = quarterly_fin.loc['Total Revenue'].dropna()
            
            # Need at least 8 quarters (2 years) to calculate meaningful TTM-based CAGR
            if len(quarterly_rev) < 8:
                # Fall back to annual data
                annual_fin = yf.Ticker(ticker).financials
                if annual_fin is not None and 'Total Revenue' in annual_fin.index:
                    return annual_fin.loc['Total Revenue'].dropna()
                return None
            
            # Calculate rolling TTM (Trailing Twelve Months)
            ttm_values = []
            ttm_dates = []
            
            for i in range(len(quarterly_rev) - 3):
                ttm = quarterly_rev.iloc[i:i+4].sum()
                ttm_values.append(ttm)
                ttm_dates.append(quarterly_rev.index[i])
            
            if not ttm_values:
                return None
            
            return pd.Series(ttm_values, index=ttm_dates)
        except:
            return None
    
    def get_fundamentals(self, ticker: str) -> Dict[str, Optional[float]]:
        """Grab the usual suspects from yfinance.info and cash flow statement"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Calculate TTM FCF from quarterly cash flow statement (more reliable)
            fcf = None
            try:
                cf_q = stock.quarterly_cashflow
                if cf_q is not None and 'Free Cash Flow' in cf_q.index:
                    fcf_series = cf_q.loc['Free Cash Flow'].dropna()
                    if len(fcf_series) >= 4:
                        fcf = fcf_series.iloc[:4].sum()  # TTM
                        
                        # Handle currency conversion for international stocks
                        financial_currency = info.get('financialCurrency', 'USD')
                        quote_currency = info.get('currency', 'USD')
                        
                        # If financials are in different currency, convert using approximate rates
                        # This is a simple approximation - real solution would use live FX rates
                        if financial_currency != 'USD' and quote_currency == 'USD':
                            # Common conversions (approximate rates as of late 2025)
                            conversion_rates = {
                                'TWD': 32,    # Taiwan Dollar
                                'EUR': 0.92,  # Euro
                                'JPY': 150,   # Japanese Yen
                                'KRW': 1300,  # Korean Won
                                'GBP': 0.79,  # British Pound
                            }
                            
                            rate = conversion_rates.get(financial_currency, 1)
                            fcf = fcf / rate
            except:
                pass
            
            return {
                'pe_ratio': info.get('trailingPE'),
                'debt_to_equity': info.get('debtToEquity'),
                'return_on_equity': info.get('returnOnEquity'),
                'free_cashflow': fcf,
            }
        except:
            return {
                'pe_ratio': None,
                'debt_to_equity': None,
                'return_on_equity': None,
                'free_cashflow': None,
            }
    
    def get_valuation_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Fetch enterprise value and FCF for valuation metrics."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get TTM FCF
            fcf = None
            try:
                cf_q = stock.quarterly_cashflow
                if cf_q is not None and 'Free Cash Flow' in cf_q.index:
                    fcf_series = cf_q.loc['Free Cash Flow'].dropna()
                    if len(fcf_series) >= 4:
                        fcf = fcf_series.iloc[:4].sum()
                        
                        # Currency conversion
                        financial_currency = info.get('financialCurrency', 'USD')
                        quote_currency = info.get('currency', 'USD')
                        if financial_currency != 'USD' and quote_currency == 'USD':
                            conversion_rates = {'TWD': 32, 'EUR': 0.92, 'JPY': 150, 'KRW': 1300, 'GBP': 0.79}
                            fcf = fcf / conversion_rates.get(financial_currency, 1)
            except:
                pass
            
            return {
                'enterprise_value': info.get('enterpriseValue'),
                'market_cap': info.get('marketCap'),
                'free_cashflow': fcf,
            }
        except:
            return {'enterprise_value': None, 'market_cap': None, 'free_cashflow': None}
    
    def get_roic_components(self, ticker: str) -> Dict[str, Optional[float]]:
        """Fetch components needed for ROIC calculation."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            balance_sheet = stock.balance_sheet
            income_stmt = stock.financials
            
            # Get most recent values
            operating_income = None
            if income_stmt is not None and 'Operating Income' in income_stmt.index:
                operating_income = income_stmt.loc['Operating Income'].iloc[0]
            
            # Calculate tax rate from income statement
            tax_rate = None
            if income_stmt is not None:
                if 'Tax Provision' in income_stmt.index and 'Pretax Income' in income_stmt.index:
                    tax_provision = income_stmt.loc['Tax Provision'].iloc[0]
                    pretax_income = income_stmt.loc['Pretax Income'].iloc[0]
                    if pretax_income and pretax_income != 0:
                        tax_rate = abs(tax_provision / pretax_income)
            
            # Balance sheet items
            total_debt = info.get('totalDebt')
            total_equity = balance_sheet.loc['Stockholders Equity'].iloc[0] if balance_sheet is not None and 'Stockholders Equity' in balance_sheet.index else None
            cash = info.get('totalCash')
            
            return {
                'operating_income': operating_income,
                'tax_rate': tax_rate if tax_rate else 0.21,  # Default to 21% corporate tax rate
                'total_debt': total_debt,
                'total_equity': total_equity,
                'cash': cash,
            }
        except:
            return {'operating_income': None, 'tax_rate': 0.21, 'total_debt': None, 'total_equity': None, 'cash': None}
    
    def get_margin_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Fetch data for margin calculations."""
        try:
            stock = yf.Ticker(ticker)
            income_stmt = stock.financials
            
            revenue = None
            operating_income = None
            cost_of_revenue = None
            
            if income_stmt is not None:
                if 'Total Revenue' in income_stmt.index:
                    revenue = income_stmt.loc['Total Revenue'].iloc[0]
                if 'Operating Income' in income_stmt.index:
                    operating_income = income_stmt.loc['Operating Income'].iloc[0]
                if 'Cost Of Revenue' in income_stmt.index:
                    cost_of_revenue = income_stmt.loc['Cost Of Revenue'].iloc[0]
            
            # Get TTM FCF
            fcf = None
            try:
                cf_q = stock.quarterly_cashflow
                info = stock.info
                if cf_q is not None and 'Free Cash Flow' in cf_q.index:
                    fcf_series = cf_q.loc['Free Cash Flow'].dropna()
                    if len(fcf_series) >= 4:
                        fcf = fcf_series.iloc[:4].sum()
                        
                        # Currency conversion
                        financial_currency = info.get('financialCurrency', 'USD')
                        quote_currency = info.get('currency', 'USD')
                        if financial_currency != 'USD' and quote_currency == 'USD':
                            conversion_rates = {'TWD': 32, 'EUR': 0.92, 'JPY': 150, 'KRW': 1300, 'GBP': 0.79}
                            fcf = fcf / conversion_rates.get(financial_currency, 1)
            except:
                pass
            
            return {
                'revenue': revenue,
                'operating_income': operating_income,
                'free_cashflow': fcf,
                'cost_of_revenue': cost_of_revenue,
            }
        except:
            return {'revenue': None, 'operating_income': None, 'free_cashflow': None, 'cost_of_revenue': None}
    
    def get_leverage_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Fetch data for leverage metrics."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            income_stmt = stock.financials
            
            # EBITDA from info
            ebitda = info.get('ebitda')
            
            # EBIT from income statement
            ebit = None
            if income_stmt is not None and 'EBIT' in income_stmt.index:
                ebit = income_stmt.loc['EBIT'].iloc[0]
            elif income_stmt is not None and 'Operating Income' in income_stmt.index:
                ebit = income_stmt.loc['Operating Income'].iloc[0]  # EBIT ≈ Operating Income
            
            # Interest expense
            interest_expense = None
            if income_stmt is not None and 'Interest Expense' in income_stmt.index:
                interest_expense = abs(income_stmt.loc['Interest Expense'].iloc[0])
            
            # FCF for alternative leverage metric
            fcf = None
            try:
                cf_q = stock.quarterly_cashflow
                if cf_q is not None and 'Free Cash Flow' in cf_q.index:
                    fcf_series = cf_q.loc['Free Cash Flow'].dropna()
                    if len(fcf_series) >= 4:
                        fcf = fcf_series.iloc[:4].sum()
                        
                        # Currency conversion
                        financial_currency = info.get('financialCurrency', 'USD')
                        quote_currency = info.get('currency', 'USD')
                        if financial_currency != 'USD' and quote_currency == 'USD':
                            conversion_rates = {'TWD': 32, 'EUR': 0.92, 'JPY': 150, 'KRW': 1300, 'GBP': 0.79}
                            fcf = fcf / conversion_rates.get(financial_currency, 1)
            except:
                pass
            
            return {
                'total_debt': info.get('totalDebt'),
                'cash': info.get('totalCash'),
                'ebitda': ebitda,
                'ebit': ebit,
                'interest_expense': interest_expense,
                'free_cashflow': fcf,
            }
        except:
            return {'total_debt': None, 'cash': None, 'ebitda': None, 'ebit': None, 'interest_expense': None, 'free_cashflow': None}
    
    def get_capex_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Fetch CapEx and revenue for intensity calculations."""
        try:
            stock = yf.Ticker(ticker)
            cashflow = stock.cashflow
            income_stmt = stock.financials
            
            capex = None
            if cashflow is not None and 'Capital Expenditure' in cashflow.index:
                capex = cashflow.loc['Capital Expenditure'].iloc[0]
            
            revenue = None
            if income_stmt is not None and 'Total Revenue' in income_stmt.index:
                revenue = income_stmt.loc['Total Revenue'].iloc[0]
            
            return {
                'capital_expenditure': capex,
                'revenue': revenue,
            }
        except:
            return {'capital_expenditure': None, 'revenue': None}
    
    def get_inventory_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Fetch inventory and cost of revenue for turnover calculations."""
        try:
            stock = yf.Ticker(ticker)
            balance_sheet = stock.balance_sheet
            income_stmt = stock.financials
            
            inventory = None
            if balance_sheet is not None and 'Inventory' in balance_sheet.index:
                inventory = balance_sheet.loc['Inventory'].iloc[0]
            
            cost_of_revenue = None
            if income_stmt is not None and 'Cost Of Revenue' in income_stmt.index:
                cost_of_revenue = income_stmt.loc['Cost Of Revenue'].iloc[0]
            
            return {
                'inventory': inventory,
                'cost_of_revenue': cost_of_revenue,
            }
        except:
            return {'inventory': None, 'cost_of_revenue': None}
    
    def get_rnd_data(self, ticker: str) -> Dict[str, Optional[float]]:
        """Fetch R&D expense and revenue for intensity calculations."""
        try:
            stock = yf.Ticker(ticker)
            income_stmt = stock.financials
            
            rnd = None
            if income_stmt is not None and 'Research And Development' in income_stmt.index:
                rnd = income_stmt.loc['Research And Development'].iloc[0]
            
            revenue = None
            if income_stmt is not None and 'Total Revenue' in income_stmt.index:
                revenue = income_stmt.loc['Total Revenue'].iloc[0]
            
            return {
                'research_development': rnd,
                'revenue': revenue,
            }
        except:
            return {'research_development': None, 'revenue': None}