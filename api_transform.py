from text_analysis_utils import text_transform, calculate, handle_summary

def apply_transform(text, transform):
    args = [False] * 4
    idx = {"uppercase": 0, "lowercase": 1, "capitalize": 2}.get(transform, 3)
    args[idx] = transform
    return text_transform(text, *args)

def run_actions(text, transform, statistic, frequent = 5):
    out = {}
    if transform:
        text = apply_transform(text, transform)
        out["transformed"] = text
    if statistic == "stats":
        out["result"] = calculate(text, frequent)
    elif statistic == "summary":
        out["summary"] = handle_summary(text)
    return out