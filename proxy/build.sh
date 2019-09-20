#! /bin/sh
export DOCKER0=172.17.0.1
export WORKDIR=`pwd`
docker run -it  --name build-istio-proxy --rm -e http_proxy="http://$DOCKER0:1087" -e https_proxy="http://$DOCKER0:1087" \
            -e BAZEL_BUILD_ARGS="-c dbg" -e BAZEL_TARGETS="//src/envoy:envoy"\
            -v /home/dzdx/Documents/istio-proxy:/home/circleci/istio-proxy \
            -v /home/dzdx/Documents/istio-envoy:/home/circleci/istio-envoy \
            -v $WORKDIR/cache/bazel:/home/circleci/.cache/bazel \
            -v $WORKDIR/cache/bazelist:/home/circleci/.cache/bazelist \
            istio-proxy-debug bash -c "cd /home/circleci/istio-proxy && make build"
