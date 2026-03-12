import re
from typing import List, Tuple

import phonenumbers
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline


class PIICleaner:
    def __init__(self, model_name: str = "Babelscape/wikineural-multilingual-ner") -> None:
        self.ner_pipeline = pipeline(
            "ner",
            model=AutoModelForTokenClassification.from_pretrained(model_name),
            tokenizer=AutoTokenizer.from_pretrained(model_name),
            aggregation_strategy="max",
        )

    def anonymize_phone_numbers(self, text: str, replacement: str = "[PHONE-NUMBER]") -> str:
        matches = phonenumbers.PhoneNumberMatcher(text, None)
        spans = [(match.start, match.end) for match in matches]

        for start, end in sorted(spans, reverse=True):
            text = text[:start] + replacement + text[end:]

        return text

    def clean_addresses(self, text: str) -> str:
        ip_regex = r"\b(?:\d{1,3}\.){3}\d{1,3}\b(?!:\d+)"
        url_regex = r"(?:[a-zA-Z]+:\/\/[^\s]+|www\.[^\s]+)"

        text = re.sub(ip_regex, "[IP_ADDRESS]", text)
        text = re.sub(url_regex, "[URL]", text)

        return text

    def clean_emails(self, text: str) -> str:
        email_pattern = r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"
        return re.sub(email_pattern, "[EMAIL-ADDRESS]", text)

    def clean_names_with_ner(self, text: str) -> str:
        lines = text.splitlines()
        cleaned_lines = []

        for line in lines:
            if not line.strip():
                cleaned_lines.append(line)
                continue

            ner_results = self.ner_pipeline(line)

            spans = [
                (entity["start"], entity["end"])
                for entity in ner_results
                if entity.get("entity_group") == "PER"
            ]

            if not spans:
                cleaned_lines.append(line)
                continue

            spans = sorted(spans, key=lambda x: x[0])

            merged_spans = []
            for start, end in spans:
                if not merged_spans or start > merged_spans[-1][1]:
                    merged_spans.append([start, end])
                else:
                    merged_spans[-1][1] = max(merged_spans[-1][1], end)

            result = []
            last_idx = 0
            for start, end in merged_spans:
                result.append(line[last_idx:start])
                result.append("[NAME]")
                last_idx = end
            result.append(line[last_idx:])

            cleaned_lines.append("".join(result))

        return "\n".join(cleaned_lines)

    def clean_pii(self, input_text: str) -> str:
        if input_text is None:
            return ""

        text = str(input_text)

        if not text.strip():
            return text

        text = self.anonymize_phone_numbers(text, replacement="[PHONE-NUMBER]")
        text = self.clean_addresses(text)
        text = self.clean_emails(text)
        text = self.clean_names_with_ner(text)

        return text