import unittest

# def discover_and_run(start_dir: str = '.', pattern: str = 'test_*.py'):
#     """Discover and run tests cases, returning the result."""
#     tests = unittest.defaultTestLoader(start_dir, pattern=pattern)
#     # We'll use the standard text runner which prints to stdout
#     runner = unittest.TextTestRunner()
#     result = runner.run(tests) # Returns a TestResult
#     print(result.errors, result.failures) # And more useful properties
#     return result

# discover_and_run()