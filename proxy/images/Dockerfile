FROM istio/ci:go1.11-bazelisk-clang8-cmake3.8.0
USER root

RUN touch /etc/apt/apt.conf.d/proxy.conf && \
    echo 'Acquire::http::Proxy "http://172.17.0.1:1087";' >> /etc/apt/apt.conf.d/proxy.conf && \
    echo 'Acquire::https::Proxy "http://172.17.0.1:1087";' >> /etc/apt/apt.conf.d/proxy.conf

RUN apt-get update
RUN apt-get install lldb-8 vim
RUN ln -s /home/circleci/istio-proxy/bazel-out/k8-dbg/bin /home/circleci/bin && \
    echo 'settings set target.load-cwd-lldbinit true' > /home/circleci/.lldbinit && \
    chmod 666 /home/circleci/.lldbinit
ADD certs /etc/certs
WORKDIR /home/circleci/workspace
USER circleci
