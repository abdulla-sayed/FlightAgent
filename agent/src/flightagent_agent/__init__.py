# Why do we need such files?:
# It's because python needs to know about the packages and modules we have, e.g., import flightagent_mcp means
# Find a Python package/module called flightagent_mcp, The __init__.py file historically tells Python: "This directory is a Python package."
# Modern Python has namespace packages that can sometimes work without it,
# but for a conventional application/package structure, explicitly having __init__.py is still a sensible and common choice.
# thus, these files are our "python packages" and we use the src/ layout because:
# One major benefit is that it helps prevent accidentally importing your package directly from the project directory during development when it hasn't actually been installed.
