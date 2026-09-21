"""Module 22: Logging"""
import logging

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("my_agent")

logger.debug("Debug: detailed internal state")
logger.info("Info: normal operation event")
logger.warning("Warning: something unexpected but recoverable")
logger.error("Error: operation failed")
logger.critical("Critical: system cannot continue")

# Connection to AI Agents: agent runtimes use structured logging
# instead of print() so logs can be filtered, routed, and stored.
print("Logging lesson complete — check output above.")
