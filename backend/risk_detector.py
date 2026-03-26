import re

RISK_KEYWORDS = [
    "penalty",
    "fine",
    "imprisonment",
    "liable",
    "liability",
    "shall",
    "failure",
    "violation",
    "offence",
    "offense",
    "punishable",
    "cancellation",
    "terminated",
    "termination",
    "suspension",
    "revocation",
    "prohibited",
    "mandatory",
    "must",
    "within",
    "deadline"
]


def highlight_risks(text):
    highlighted_text = text

    for word in RISK_KEYWORDS:
        pattern = re.compile(rf"\b({word})\b", re.IGNORECASE)
        highlighted_text = pattern.sub(
            r"<span style='color:red; font-weight:bold;'>⚠️ \1</span>",
            highlighted_text
        )

    return highlighted_text
