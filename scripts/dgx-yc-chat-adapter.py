#!/usr/bin/env python3
"""Expose the configured DGX yc-oam chat service as a minimal Ollama chat API."""

from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import urllib.request


def request_dgx(upstream: str, payload: dict[str, object]) -> str:
    messages = payload.get("messages", [])
    system = str(payload.get("system", "")).strip()
    pieces = [system] if system else []
    for record in messages if isinstance(messages, list) else []:
        if not isinstance(record, dict):
            continue
        role = str(record.get("role", "user")).upper()
        content = str(record.get("content", "")).strip()
        if content:
            pieces.append(f"{role}:\n{content}")
    prompt = "\n\n".join(pieces)
    session_digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:20]
    body = json.dumps(
        {
            "message": prompt,
            "session_id": f"codex-i18n-{session_digest}",
            "mode": "assistant",
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        upstream,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.load(response)
    reply = str(result.get("reply", "")).strip()
    if not reply:
        raise RuntimeError(f"DGX reply was empty: {result}")
    return reply


def handler(upstream: str):
    class AdapterHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            if self.path != "/api/chat":
                self.send_error(404)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length))
                reply = request_dgx(upstream, payload)
                encoded = json.dumps(
                    {
                        "message": {"role": "assistant", "content": reply},
                        "done": True,
                    },
                    ensure_ascii=False,
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
            except Exception as exc:  # noqa: BLE001 - boundary adapter
                encoded = json.dumps({"error": str(exc)}).encode("utf-8")
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

        def log_message(self, format: str, *args: object) -> None:
            print(f"adapter: {format % args}", flush=True)

    return AdapterHandler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=11437)
    parser.add_argument(
        "--upstream",
        default=os.environ.get("DGX_CHAT_ENDPOINT"),
        help="DGX chat URL; defaults to DGX_CHAT_ENDPOINT",
    )
    args = parser.parse_args()
    if not args.upstream:
        parser.error("--upstream or DGX_CHAT_ENDPOINT is required")
    server = ThreadingHTTPServer(
        (args.host, args.port),
        handler(args.upstream),
    )
    print(
        json.dumps(
            {
                "event": "started",
                "listen": f"http://{args.host}:{args.port}",
                "upstream": args.upstream,
            }
        ),
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
