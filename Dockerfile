FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl git ca-certificates grep && \
    rm -rf /var/lib/apt/lists/*

ENV ELAN_HOME=/root/.elan
ENV PATH=/root/.elan/bin:$PATH

RUN curl -sSfL https://elan.lean-lang.org/elan-init.sh | \
    sh -s -- -y --default-toolchain none

WORKDIR /formalization
COPY . .

# 获取固定依赖，构建完整形式化，并保存公理审计结果。
RUN lake exe cache get && \
    lake --rehash build && \
    lake env lean AxiomCheck.lean 2>&1 | tee /formalization/axiom-audit.log && \
    ! grep -RInE '\bsorry\b|\badmit\b|^[[:space:]]*axiom\b' \
      --include='*.lean' --exclude-dir=.lake .

CMD ["cat", "/formalization/axiom-audit.log"]
