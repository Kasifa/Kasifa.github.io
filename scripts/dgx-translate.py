#!/usr/bin/env python3
"""Translate extracted site strings through a local Ollama endpoint with checkpoints."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.request
from pathlib import Path


FORMULA_PATTERNS = (
    re.compile(r"\\\([\s\S]*?\\\)"),
    re.compile(r"\\\[[\s\S]*?\\\]"),
    re.compile(r"https?://[^\s<]+"),
)
PROTECTED_SPLIT_RE = re.compile(
    r"(\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|https?://[^\s<]+)"
)
CHINESE_PATTERN = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
TEX_TEXT_PATTERN = re.compile(r"\\(text|mathrm|operatorname)\{[^{}]*\}")
PUNCTUATION_MAP = str.maketrans("，。；：！？", ",.;:!?")


SYSTEM_PROMPT = """You translate a mathematics research website from Chinese to English.
Write as one individual human researcher. Use first-person singular for the researcher's choices, work, uncertainty, and plans. Use a neutral voice for established mathematics.
Never use first-person plural forms such as "we" or "our".
Use plain, concise academic English. Do not add claims, certainty, novelty, or interpretation.
Keep fragments as fragments and preserve their role in the surrounding sentence. Do not add headings, explanations, or closing punctuation that is absent from the source.
Preserve every TeX expression, URL, identifier, number, and citation exactly. Never translate text inside TeX delimiters.
Use standard Navier-Stokes terminology. In particular: 正式问题说明 = official problem statement; 基础约定 = basic conventions; 无散性 = divergence-free condition; 三波闭合 = triad closure; 临界缩放 = critical scaling; 临界二次量 = critical quadratic quantity; 使用权重 = uses the weight; 临界带权非守恒 = nonconservation of the critical weighted quantity; 无交叉支持共振 = absence of cross-support resonance; 大数据 = large-data regime; 螺旋 = helical; 同号/异号 = same-sign/opposite-sign; 近对角 = near-diagonal; 高频/低频 = high/low frequency; 支持 = support; 局部性 = locality; 强制性 = coercivity; 抵消 = cancellation; 泄漏 = leakage; 薄锥 = narrow cone; 解析半径 = radius of analyticity; 障碍 = obstruction; 奇性 = singularity; 爆破 = blow-up; 弱解 = weak solution; 同行评议 = peer review; 与算子交换 = commutes with the operator.
Do not attach an English possessive to a formula or an NSPH token. For a pattern such as "FORMULA 的无权和", write "the unweighted sum of FORMULA". For "大数据无法吸收", write "the estimate cannot be absorbed in the large-data regime".
Translate every input item and follow the requested output format exactly, with no markdown fences or commentary."""

MANUAL_TRANSLATIONS = {
    ", Clay Mathematics Institute 正式问题说明。": ", the Clay Mathematics Institute's official problem statement.",
    "\\((1,-4,3)\\) 的无权和为零，而 \\(2(1-8+3\\sqrt5)\\ne0\\)。": "The unweighted sum of \\((1,-4,3)\\) is zero, whereas \\(2(1-8+3\\sqrt5)\\ne0\\).",
    "\\(\\dot H^{1/2}\\)：临界但大数据无法吸收": "\\(\\dot H^{1/2}\\): critical, but the estimate cannot be absorbed in the large-data regime",
    "\\(\\mathbb P_k^2=\\mathbb P_k=\\mathbb P_k^\\ast\\)， \\(k\\cdot\\mathbb P_kv=0\\)，且 \\(\\mathbb P\\nabla p=0\\)。 因而 \\(\\mathbb P\\) 是 \\(L^2\\) 中的正交投影，并与 \\(\\Delta\\)、\\(\\Lambda^s\\) 交换。": "\\(\\mathbb P_k^2=\\mathbb P_k=\\mathbb P_k^\\ast\\), \\(k\\cdot\\mathbb P_kv=0\\), and \\(\\mathbb P\\nabla p=0\\). Therefore, \\(\\mathbb P\\) is the orthogonal projection on \\(L^2\\) and commutes with both \\(\\Delta\\) and \\(\\Lambda^s\\).",
    "但临界二次量使用权重 \\(|k|\\)。在上述 \\(T\\) 的单模定义下， 正负模配对后的非线性贡献为": "But the critical quadratic quantity uses the weight \\(|k|\\). Under the single-mode definition of \\(T\\) above, pairing the positive and negative modes gives the nonlinear contribution",
    "适用范围": "Scope",
    "00 · 完成状态": "00 · Completion status",
    "版本 v0.2 · 2026-08-16": "Version v0.2 · 2026-08-16",
    "笔记状态 · 推导已复查": "Note status · derivation checked",
    "Navier–Stokes 个人研究日志": "Navier–Stokes Personal Research Log",
    "它在 \\(0\\le t\\le x\\) 上严格递增，所以固定 \\(x\\) 时最大值在 \\(t=x\\)，即 \\(y=1\\) 取得。 此时": "It is strictly increasing on \\(0\\le t\\le x\\), so for fixed \\(x\\) the maximum occurs at \\(t=x\\), or equivalently \\(y=1\\). In that case,",
    "在整体缩放下 \\(W_s\\) 是二次齐次的。下面固定 \\(P=1\\)，因此 \\(\\mathcal C_s\\) 表示归一化后的临界几何核。": "Under overall scaling, \\(W_s\\) is homogeneous of degree two. I now fix \\(P=1\\), so \\(\\mathcal C_s\\) denotes the normalized critical geometric kernel.",
    "所以 \\(AB(C+D)": "Therefore \\(AB(C+D)",
    "在 \\(\\varepsilon=0.2,n=8\\) 时，接力投影给出 \\(-0.0055113519\\)，完整递推给出 \\(+4.1813664551\\)。有限层数值强烈稳定，但我尚未把 \\(C_n\\) 的极限写成解析闭式， 因而不把 \\(104.5341618\\) 标成已证明常数。": "At \\(\\varepsilon=0.2,n=8\\), the relay projection gives \\(-0.0055113519\\), while the full recurrence gives \\(+4.1813664551\\). The finite-layer values are strongly stable, but I have not obtained a closed analytic form for the limit of \\(C_n\\). I therefore do not present \\(104.5341618\\) as a proved constant.",
    "预定有向接力的闭式则是 \\(D_\\infty=-9\\sqrt6/160\\)。所以完整系数与预定系数的比值恰为 \\[ \\frac{C_\\infty}{D_\\infty}=-\\frac{47797}{63} =-758.68253968\\ldots . \\] R0.12 的“相反符号、约 759 倍”由此变成精确等式。": "The closed form for the prescribed directed relay is \\(D_\\infty=-9\\sqrt6/160\\). Therefore, the ratio of the full coefficient to the prescribed coefficient is exactly \\[ \\frac{C_\\infty}{D_\\infty}=-\\frac{47797}{63} =-758.68253968\\ldots . \\] Thus, the 'opposite sign and about 759 times larger' statement in R0.12 becomes an exact identity.",
    "\\[ \\frac{X_\\infty}{T_\\infty}\\ge45.739348 \\qquad\\text{对任意复振幅成立。} \\]": "\\[ \\frac{X_\\infty}{T_\\infty}\\ge45.739348 \\qquad\\text{for every complex amplitude.} \\]",
    "\\[ T_a=T_b=E_a=E_b=0 \\quad\\text{在整个反对称图 }(a,b)=(0,0)\\text{ 上}. \\]": "\\[ T_a=T_b=E_a=E_b=0 \\quad\\text{throughout the antisymmetric chart }(a,b)=(0,0)\\text{}. \\]",
    "\\[ \\#S_L=\\begin{cases} (L+1)^3,&L\\text{ 为奇数},\\\\ (L+1)^3-1,&L\\text{ 为偶数}. \\end{cases} \\]": "\\[ \\#S_L=\\begin{cases} (L+1)^3,&L\\text{ is odd},\\\\ (L+1)^3-1,&L\\text{ is even}. \\end{cases} \\]",
    "令 \\(R_5\\) 为 R0.18 的第五阶外部/目标能量比，并把四个实极化图坐标写成 \\[ (t_P,t_Q,t_B,t_D)=(p+a,-p+a,q+b,-q+b). \\] R0.18 根盒中的唯一解 \\(z_*=(p_*,q_*,x_*)\\) 使 \\((a,b,p,q,x)=(0,0,z_*)\\) 成为完整五变量驻点。该点的五维 Hessian 正定， 因而它是 \\(R_5\\) 在这个实五变量族中的严格局部极小点。": "Let \\(R_5\\) denote the fifth-order external-to-target energy ratio from R0.18, and write the four real polarization-chart coordinates as \\[ (t_P,t_Q,t_B,t_D)=(p+a,-p+a,q+b,-q+b). \\] The unique solution \\(z_*=(p_*,q_*,x_*)\\) in the R0.18 root box makes \\((a,b,p,q,x)=(0,0,z_*)\\) a stationary point of the full five-variable problem. The five-dimensional Hessian at this point is positive definite, so it is a strict local minimizer of \\(R_5\\) within this real five-variable family.",
    "\\(T\\) 是目标频率能量，\\(E\\) 是模型中其余频率的能量。 R0.18 使用的外部/目标比 \\(R=E/T\\) 与这里的目标比例满足 \\(J=1/(1+R)\\)， 所以 \\(R\\) 的极小点就是 \\(J\\) 的极大点。为处理全部无穷端，我使用射影坐标": "\\(T\\) is the target-frequency energy, and \\(E\\) is the energy in all other model frequencies. The external-to-target ratio \\(R=E/T\\) used in R0.18 and the target share here satisfy \\(J=1/(1+R)\\), so a minimizer of \\(R\\) is a maximizer of \\(J\\). To cover all points at infinity, I use projective coordinates",
}


def raw_protected_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    for pattern in FORMULA_PATTERNS:
        tokens.extend(pattern.findall(text))
    return tokens


def protected_tokens(text: str) -> list[str]:
    return [
        TEX_TEXT_PATTERN.sub(r"\\\1{__I18N_TEXT__}", token)
        for token in raw_protected_tokens(text)
    ]


def mask_protected(item_id: str, text: str) -> tuple[str, dict[str, str]]:
    masked = text
    replacements: dict[str, str] = {}
    for index, token in enumerate(raw_protected_tokens(text)):
        placeholder = f"NSPH{item_id.upper()}X{index}END"
        masked = masked.replace(token, placeholder, 1)
        replacements[placeholder] = token
    return masked, replacements


def preserve_edge_punctuation(source: str, translation: str) -> str:
    leading = re.match(r"^[，。；：！？,.;:!?]+", source)
    if leading:
        expected = leading.group(0).translate(PUNCTUATION_MAP)
        if not translation.startswith(expected):
            translation = expected + (" " if translation and not translation.startswith(" ") else "") + translation

    trailing = re.search(r"[，。；：！？,.;:!?]+$", source)
    if trailing:
        expected = trailing.group(0).translate(PUNCTUATION_MAP)
        if not translation.endswith(expected):
            translation = translation.rstrip("，。；：！？,.;:!?") + expected
    else:
        translation = translation.rstrip("，。；：！？,.;:!?")
    return translation


def singularize_voice(translation: str) -> str:
    replacements = (
        (r"\bOur\b", "My"),
        (r"\bour\b", "my"),
        (r"\bOurs\b", "Mine"),
        (r"\bours\b", "mine"),
        (r"\bOurselves\b", "Myself"),
        (r"\bourselves\b", "myself"),
        (r"\bWe\b", "I"),
        (r"\bwe\b", "I"),
    )
    for pattern, replacement in replacements:
        translation = re.sub(pattern, replacement, translation)
    return translation


def is_valid(source: str, translation: str) -> bool:
    if not translation.strip():
        return False
    if re.search(r"[\u3400-\u9fff\uf900-\ufaff]", translation):
        return False
    if re.search(r"NSPH[A-Z0-9]+END", translation):
        return False
    if (
        "\t" in translation
        or re.search(r"\\t(?:\s|$)", translation)
        or re.search(r"(?:^|\s)s\d{4}\b", translation)
    ):
        return False
    if re.search(r"\b(?:we|our|ours|ourselves)\b", translation, re.I):
        return False
    if CHINESE_PATTERN.search(source) and not re.search(r"[A-Za-z]", translation):
        return False
    if "我" in source and not re.search(r"\b(?:I|my)\b", translation, re.I):
        return False
    if "个人" in source and "personal" not in translation.lower():
        return False
    source_prose = PROTECTED_SPLIT_RE.sub("", source)
    translated_prose = PROTECTED_SPLIT_RE.sub("", translation)
    source_length = len(re.sub(r"\s+", "", source_prose))
    translated_length = len(re.sub(r"\s+", "", translated_prose))
    if source_length >= 24 and translated_length < source_length * 0.55:
        return False
    if translated_length > max(180, source_length * 7):
        return False
    source_has_terminal = bool(re.search(r"[，。；：！？,.;:!?]+$", source))
    if not source_has_terminal and re.search(r"[.;:!?]+$", translation):
        return False
    return protected_tokens(source) == protected_tokens(translation)


def atomic_write(path: Path, data: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(data, encoding="utf-8")
    os.replace(temporary, path)


def load_checkpoint(path: Path) -> dict[str, dict]:
    completed: dict[str, dict] = {}
    if not path.exists():
        return completed
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        completed[item["id"]] = item
    return completed


def request_translation(endpoint: str, model: str, items: list[dict]) -> dict[str, str]:
    replacements: dict[str, dict[str, str]] = {}
    source_by_id = {item["id"]: item["zh"] for item in items}
    compact = []
    for item in items:
        masked, item_replacements = mask_protected(item["id"], item["zh"])
        replacements[item["id"]] = item_replacements
        compact.append({"id": item["id"], "zh": masked})
    prompt = (
        "Translate the following JSON array. Return exactly one line per input item in "
        "the same order. Start each line by copying that item's exact id value, then write "
        "one literal tab character and the English translation. Never output the literal "
        "word ID. For example, an item whose id is s0123 must produce a line beginning "
        "s0123 followed by a tab. Keep each translation on one line. Preserve every token "
        "beginning with NSPH and ending with END exactly, including capitalization and "
        "digits. Translate all Chinese text, including short headings and labels.\n\n"
        + json.dumps(compact, ensure_ascii=False, separators=(",", ":"))
    )
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "options": {"temperature": 0, "num_ctx": 16384, "num_predict": 2500},
    }
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=1800) as response:
        result = json.loads(response.read().decode("utf-8"))
    content = result["message"]["content"].strip()
    content = re.sub(r"^```(?:text|tsv)?\s*|\s*```$", "", content)
    translations: dict[str, str] = {}
    for line in content.splitlines():
        match = re.match(
            r"^(s\d{4})(?:\t|\\t|\s{2,}|\s*[,|:]\s*)(.+)$", line.strip()
        )
        if match:
            item_id = match.group(1)
            translation = re.sub(r"^(?:\\t|\t)\s*", "", match.group(2).strip())
            for placeholder, token in replacements.get(item_id, {}).items():
                translation = translation.replace(placeholder, token)
            translations[item_id] = preserve_edge_punctuation(
                source_by_id[item_id], singularize_voice(translation)
            )
    for item in items:
        manual = MANUAL_TRANSLATIONS.get(item["zh"])
        if manual:
            translations[item["id"]] = manual
    if not translations:
        print(
            json.dumps(
                {"event": "unparsed_response", "content": content[:2000]},
                ensure_ascii=False,
            ),
            flush=True,
        )
    return translations


def request_plain_translation(endpoint: str, model: str, text: str) -> str:
    prompt = (
        "Translate this Chinese mathematics-research fragment into plain academic "
        "English. Return the English fragment only, without a label, quotation marks, "
        f"or commentary. Text: {text.strip()}"
    )
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "options": {"temperature": 0, "num_ctx": 16384, "num_predict": 1000},
    }
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=1800) as response:
        result = json.loads(response.read().decode("utf-8"))
    translation = result["message"]["content"].strip()
    translation = re.sub(r"^```(?:text)?\s*|\s*```$", "", translation).strip()
    translation = re.sub(r"^(?:Translation|English)\s*:\s*", "", translation, flags=re.I)
    translation = translation.strip('"')
    return preserve_edge_punctuation(text.strip(), singularize_voice(translation))


def request_single_translation(endpoint: str, model: str, item: dict) -> str:
    manual = MANUAL_TRANSLATIONS.get(item["zh"])
    if manual:
        return manual

    pieces = [piece for piece in PROTECTED_SPLIT_RE.split(item["zh"]) if piece]
    translated_pieces: list[str] = []
    for piece in pieces:
        if PROTECTED_SPLIT_RE.fullmatch(piece) or not CHINESE_PATTERN.search(piece):
            translated_pieces.append(piece)
            continue
        leading = re.match(r"^\s*", piece).group(0)
        trailing = re.search(r"\s*$", piece).group(0)
        translated_pieces.append(
            leading + request_plain_translation(endpoint, model, piece) + trailing
        )
    return preserve_edge_punctuation(item["zh"], "".join(translated_pieces).strip())


def make_batches(items: list[dict], character_limit: int, item_limit: int) -> list[list[dict]]:
    batches: list[list[dict]] = []
    current: list[dict] = []
    characters = 0
    for item in items:
        length = len(item["zh"])
        if current and (characters + length > character_limit or len(current) >= item_limit):
            batches.append(current)
            current = []
            characters = 0
        current.append(item)
        characters += length
    if current:
        batches.append(current)
    return batches


def translate_batch(endpoint: str, model: str, items: list[dict], depth: int = 0) -> dict[str, str]:
    accepted: dict[str, str] = {}
    pending = items
    for attempt in range(3):
        try:
            pending_count = len(pending)
            translated = request_translation(endpoint, model, pending)
            invalid = [
                item
                for item in pending
                if item["id"] not in translated
                or not is_valid(item["zh"], translated[item["id"]])
            ]
            invalid_ids = {item["id"] for item in invalid}
            accepted.update(
                {
                    item["id"]: translated[item["id"]]
                    for item in pending
                    if item["id"] not in invalid_ids
                }
            )
            if not invalid:
                return accepted
            print(
                f"validation retry depth={depth} attempt={attempt + 1} "
                f"invalid={len(invalid)}/{len(pending)} accepted={len(accepted)}",
                flush=True,
            )
            for item in invalid[:2]:
                print(
                    json.dumps(
                        {
                            "event": "invalid_sample",
                            "id": item["id"],
                            "source": item["zh"][:240],
                            "translation": translated.get(item["id"], "")[:240],
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
            pending = invalid
            if len(invalid) == pending_count:
                print(
                    f"deterministic batch failure at depth={depth}; splitting now",
                    flush=True,
                )
                break
        except Exception as error:  # retry malformed or interrupted model output
            print(
                f"request retry depth={depth} attempt={attempt + 1}: {error}",
                flush=True,
            )
        time.sleep(min(2 ** attempt, 4))

    if len(pending) == 1:
        item = pending[0]
        for attempt in range(3):
            translation = request_single_translation(endpoint, model, item)
            if is_valid(item["zh"], translation):
                return {**accepted, item["id"]: translation}
            print(
                json.dumps(
                    {
                        "event": "single_retry",
                        "attempt": attempt + 1,
                        "id": item["id"],
                        "translation": translation[:240],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
        raise RuntimeError(f"unable to translate {item['id']}")
    midpoint = len(pending) // 2
    left = translate_batch(endpoint, model, pending[:midpoint], depth + 1)
    right = translate_batch(endpoint, model, pending[midpoint:], depth + 1)
    return {**accepted, **left, **right}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--endpoint", default="http://127.0.0.1:11435")
    parser.add_argument("--model", default="codex-qwen-translator")
    parser.add_argument("--characters", type=int, default=4200)
    parser.add_argument("--items", type=int, default=100)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    source_bytes = args.input.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    source = json.loads(source_bytes)
    if args.limit is not None:
        source = source[: args.limit]
    args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    args.result.parent.mkdir(parents=True, exist_ok=True)
    completed = load_checkpoint(args.checkpoint)
    pending = [item for item in source if item["id"] not in completed]
    batches = make_batches(pending, args.characters, args.items)
    started = time.time()

    print(
        json.dumps(
            {
                "event": "start",
                "source_sha256": source_hash,
                "total": len(source),
                "resumed": len(completed),
                "pending": len(pending),
                "batches": len(batches),
                "model": args.model,
            }
        ),
        flush=True,
    )

    for batch_index, batch in enumerate(batches, 1):
        batch_started = time.time()
        translated = translate_batch(args.endpoint, args.model, batch)
        for item in batch:
            record = {
                "id": item["id"],
                "zh": item["zh"],
                "en": translated[item["id"]],
            }
            completed[item["id"]] = record

        ordered = [completed[item["id"]] for item in source if item["id"] in completed]
        atomic_write(
            args.checkpoint,
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in ordered),
        )
        elapsed = time.time() - started
        rate = max(len(ordered), 1) / max(elapsed, 1)
        eta = (len(source) - len(ordered)) / max(rate, 1e-6)
        print(
            json.dumps(
                {
                    "event": "checkpoint",
                    "batch": batch_index,
                    "batches": len(batches),
                    "completed": len(ordered),
                    "total": len(source),
                    "batch_seconds": round(time.time() - batch_started, 1),
                    "eta_seconds": round(eta),
                }
            ),
            flush=True,
        )

    result = [completed[item["id"]] for item in source]
    atomic_write(args.result, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(
        json.dumps(
            {
                "event": "complete",
                "items": len(result),
                "seconds": round(time.time() - started, 1),
                "result": str(args.result),
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
