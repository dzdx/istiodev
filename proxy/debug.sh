#! /bin/sh

export WORKDIR=`pwd`
docker run -it --rm --name istio-proxy --network host  \
           -v /home/dzdx/Documents/istio-proxy:/home/circleci/istio-proxy \
           -v /home/dzdx/Documents/istio-envoy:/home/circleci/istio-envoy \
           -v $WORKDIR/cache:/home/circleci/.cache \
           -v $WORKDIR:/home/circleci/workspace -it \
           --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --security-opt apparmor=unconfined \
           --sig-proxy=true \
           istio-proxy-debug bash
