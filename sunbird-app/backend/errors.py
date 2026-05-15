class SunbirdAPIError(Exception):
    """Raised when Sunbird API/network calls fail or return unexpected data."""


class PipelineError(Exception):
    """Raised when the pipeline cannot complete due to input, dependency, or processing errors."""
