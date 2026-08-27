FROM gapsystem/gap-docker:latest

USER root
COPY kbfns-proof.patch /tmp/kbfns-proof.patch
RUN cd /home/gap/inst/gap-4.11.1/pkg/kbmag-1.5.9 \
    && patch -p1 < /tmp/kbfns-proof.patch \
    && cd standalone/lib \
    && make CC=cc CFLAGS="-O2 -g -Wall -Wno-char-subscripts" fsalib.a \
    && cd ../src \
    && make CC=cc CFLAGS="-O2 -g -Wall -Wno-char-subscripts" \
       BIN=../../bin/x86_64-pc-linux-gnu-default64-kv7 \
       ../../bin/x86_64-pc-linux-gnu-default64-kv7/kbprog
USER gap
