FROM istio/ci:go1.11-bazelisk-clang8-cmake3.8.0
USER root

RUN touch /etc/apt/apt.conf.d/proxy.conf && \
    echo 'Acquire::http::Proxy "http://172.17.0.1:1087";' >> /etc/apt/apt.conf.d/proxy.conf && \
    echo 'Acquire::https::Proxy "http://172.17.0.1:1087";' >> /etc/apt/apt.conf.d/proxy.conf

RUN apt-get update
RUN apt-get install lldb-8 vim
RUN ln -s /home/circleci/.cache/bazel/_bazel_circleci/d9c9f96bb8903e9f03900a33f033e3c6/execroot/__main__/bazel-out/k8-dbg/bin /home/circleci/bin && \
    echo 'settings set target.load-cwd-lldbinit true' > /home/circleci/.lldbinit && \
    chmod 666 /home/circleci/.lldbinit
WORKDIR /home/circleci/workspace
USER circleci
