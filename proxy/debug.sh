#! /bin/sh

export WORKDIR=`pwd`
docker run -it --rm --entrypoint bash --name istio-proxy --network host  \
           -v $WORKDIR:/root/workspace -it \
           --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --security-opt apparmor=unconfined \
           --sig-proxy=true \
           dzdx/istio-debug-proxy:1.2.5
