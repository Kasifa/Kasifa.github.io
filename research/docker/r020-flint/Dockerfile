FROM python@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7

LABEL org.opencontainers.image.title="R0.20 exact algebra runtime"
LABEL org.opencontainers.image.description="Pinned Python, SymPy and Python-FLINT runtime for boundary elimination audits"

RUN python -m pip install --no-cache-dir \
    python-flint==0.9.0 \
    sympy==1.14.0

ENV PYTHONUNBUFFERED=1
WORKDIR /work
