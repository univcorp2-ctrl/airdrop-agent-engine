ALLOWED_AUTOMATED_TASKS=frozenset({"program_status","terms_status","api_status","points_status","market_data","dry_run"})
PROHIBITED_SCHEDULED_TASKS=frozenset({"live_trading","deposit","withdrawal","bridge","contract_approval"})
def scheduler_policy()->dict[str,object]: return {"allowed":sorted(ALLOWED_AUTOMATED_TASKS),"prohibited":sorted(PROHIBITED_SCHEDULED_TASKS),"live_scheduler_enabled":False}
