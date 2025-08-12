import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class ProcessMonitor:
    """Monitor and log process stages"""
    
    def __init__(self, process_id: str = None):
        self.process_id = process_id or self._generate_process_id()
        self.start_time = datetime.now()
    
    def _generate_process_id(self) -> str:
        """Generate unique process ID"""
        return f"proc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def log_stage(self, stage: str, status: str, details: Dict[str, Any] = None):
        """Log a process stage"""
        log_entry = {
            'process_id': self.process_id,
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'status': status,
            'details': details or {}
        }
        
        logger.info(f"Process {self.process_id} - {stage}: {status}")
        if details:
            logger.debug(f"Details: {json.dumps(details, indent=2)}")
        
        # TODO: Also write to PostgreSQL for tracking
        return log_entry