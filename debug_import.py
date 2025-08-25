import importlib
import traceback

print("Testing import of backend.main...")

try:
    m = importlib.import_module("backend.main")
    print("Imported backend.main successfully")
    print("Has app:", hasattr(m, "app"))
    if hasattr(m, "app"):
        print("App object:", m.app)
except Exception:
    print("Error during import:")
    traceback.print_exc()
