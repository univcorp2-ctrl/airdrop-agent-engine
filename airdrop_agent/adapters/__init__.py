from __future__ import annotations
from ..models import TargetConfig
from .base import BaseAdapter
from .generic import GenericAdapter
from .hibachi import HibachiAdapter
from .kyan import KyanAdapter
from .lighter import LighterAdapter
from .pacifica import PacificaAdapter
SPECIALIZED={"pacifica":PacificaAdapter,"hibachi":HibachiAdapter,"kyan":KyanAdapter,"lighter":LighterAdapter}
def adapter_for(target:TargetConfig)->BaseAdapter: return SPECIALIZED.get(target.id,GenericAdapter)(target)
__all__=["BaseAdapter","GenericAdapter","PacificaAdapter","HibachiAdapter","KyanAdapter","LighterAdapter","adapter_for"]
