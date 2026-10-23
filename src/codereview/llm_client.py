"""Ollama LLM client wrapper."""

from __future__ import annotations

try:
    import ollama
except ImportError:
    ollama = None

try:
    from rich.console import Console
    console = Console()
except ImportError:
    class DummyConsole:
        def print(self, *args, **kwargs):
            import re
            import sys
            text = " ".join(str(a) for a in args)
            clean_text = re.sub(r"\[/?[\w\s=#]+\]", "", text)
            try:
                print(clean_text)
            except UnicodeEncodeError:
                safe_text = clean_text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8")
                print(safe_text)
    console = DummyConsole()

DEFAULT_MODEL = "codellama"


class LLMClient:
    """Client for communicating with Ollama LLM."""

    def __init__(self, model: str = DEFAULT_MODEL, host: str | None = None):
        """Initialize the LLM client.

        Args:
            model: Ollama model name to use.
            host: Ollama server host URL. None uses the default localhost.
        """
        self.model = model
        if host:
            self.client = ollama.Client(host=host)
        else:
            self.client = ollama.Client()

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        stream: bool = True,
    ) -> str:
        """Send a chat message and get a response.

        Args:
            system_prompt: System prompt setting the AI's behavior.
            user_prompt: User's message/query.
            stream: Whether to stream the response.

        Returns:
            The AI's response text.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if stream:
            return self._chat_stream(messages)
        else:
            return self._chat_sync(messages)

    def _chat_sync(self, messages: list[dict]) -> str:
        """Send a synchronous chat request."""
        try:
            response = self.client.chat(model=self.model, messages=messages)
            return response["message"]["content"]
        except ollama.ResponseError as e:
            console.print(f"[red]❌ Ollama error: {e}[/red]")
            raise
        except Exception as e:
            console.print(
                f"[red]❌ Failed to connect to Ollama. "
                f"Is it running? (ollama serve)[/red]"
            )
            raise ConnectionError(
                "Cannot connect to Ollama. Make sure it's running with 'ollama serve'."
            ) from e

    def _chat_stream(self, messages: list[dict]) -> str:
        """Send a streaming chat request with live output."""
        try:
            stream = self.client.chat(
                model=self.model, messages=messages, stream=True
            )
            full_response = []
            for chunk in stream:
                content = chunk["message"]["content"]
                full_response.append(content)
                console.print(content, end="")
            console.print()  # Final newline
            return "".join(full_response)
        except ollama.ResponseError as e:
            console.print(f"[red]❌ Ollama error: {e}[/red]")
            raise
        except Exception as e:
            console.print(
                f"[red]❌ Failed to connect to Ollama. "
                f"Is it running? (ollama serve)[/red]"
            )
            raise ConnectionError(
                "Cannot connect to Ollama. Make sure it's running with 'ollama serve'."
            ) from e

    def check_connection(self) -> bool:
        """Check if Ollama is running and the model is available.

        Returns:
            True if connection is successful and model is available.
        """
        try:
            models_response = self.client.list()
            available = [m["model"] for m in models_response.get("models", [])]
            # Check with and without :latest tag
            model_names = []
            for m in available:
                model_names.append(m)
                if ":" in m:
                    model_names.append(m.split(":")[0])

            if self.model not in model_names and f"{self.model}:latest" not in model_names:
                console.print(
                    f"[yellow]⚠️  Model '{self.model}' not found. "
                    f"Available models: {', '.join(available)}[/yellow]"
                )
                console.print(
                    f"[yellow]   Run: ollama pull {self.model}[/yellow]"
                )
                return False
            return True
        except Exception:
            console.print(
                "[red]❌ Cannot connect to Ollama. "
                "Make sure it's running with 'ollama serve'.[/red]"
            )
            return False
