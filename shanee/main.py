"""Main entry point for Shanee Intelligence."""

import uvicorn

from shanee.api import create_app


def main():
    """Run the application."""
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
