import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from anonymizer.pii_cleaner import PIICleaner

cleaner = PIICleaner()

comment = """

"""

cleaned = cleaner.clean_pii(comment)

print("----- ORIGINAL -----")
print(comment)

print("\n----- ANONYMIZED -----")
print(cleaned)