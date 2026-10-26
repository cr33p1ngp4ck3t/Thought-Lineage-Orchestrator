class ProviderError(RuntimeError):
    """The model provider could not complete a request."""


class SignatureGenerationError(RuntimeError):
    """A model response could not produce a valid thought signature."""
