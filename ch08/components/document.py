from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass 
class Document:
    """파이프라인 내에서 처리되는 문서의 표준 형식"""
    page_content: str  
    metadata: Dict[str, Any] = field(default_factory=dict) 
    score: Optional[float] = None 
