from __future__ import annotations
import os
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RiskLimits:
    max_capital_usd: float=0.0
    max_notional_usd: float=0.0
    max_daily_loss_usd: float=0.0
    max_daily_fees_usd: float=0.0
    max_leverage: float=1.0
    max_open_positions: int=0
    max_api_errors: int=3
    max_data_age_seconds: int=120
    @classmethod
    def from_env(cls)->"RiskLimits":
        return cls(float(os.getenv("MAX_CAPITAL_USD","0")),float(os.getenv("MAX_NOTIONAL_USD","0")),float(os.getenv("MAX_DAILY_LOSS_USD","0")),float(os.getenv("MAX_DAILY_FEES_USD","0")),float(os.getenv("MAX_LEVERAGE","1")),int(os.getenv("MAX_OPEN_POSITIONS","0")),int(os.getenv("MAX_API_ERRORS","3")),int(os.getenv("MAX_DATA_AGE_SECONDS","120")))
def simulated_notional_usd()->float: return max(0.0,float(os.getenv("SIMULATED_NOTIONAL_USD","100")))
