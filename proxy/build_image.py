import tempfile
import shutil
import os
import sys
import docker
import contextlib
import json
import logging

logger = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
logger.addHandler(out_hdlr)
logger.setLevel(logging.INFO)


client = docker.APIClient()

ISTIO_PROXY_DIR = '/home/dzdx/Documents/istio-proxy'
ISTIO_ENVOY_DIR = '/home/dzdx/Documents/istio-envoy'

@contextlib.contextmanager
def chdir(path):
    try:
        old = os.getcwd()
        os.chdir(path)
        yield
    finally:
        os.chdir(old)

def copy_file(src, dst):
    dirname = os.path.dirname(dst)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    shutil.copy(src, dst, follow_symlinks=False)


try:
    tmp_dir = tempfile.mkdtemp(prefix="build_istio_proxy")
    print(tmp_dir)
    executable = 'cache/bazel/_bazel_circleci/d9c9f96bb8903e9f03900a33f033e3c6/execroot/__main__/bazel-out/k8-dbg/bin/src/envoy/envoy'
    logger.info("copying envoy binary")
    copy_file(executable, os.path.join(tmp_dir, 'bin/envoy'))
    logger.info("copying Dockerfile")
    copy_file('Dockerfile.debug', os.path.join(tmp_dir, 'Dockerfile'))
    logger.info("copying lldbinit")
    copy_file('.lldbinit', os.path.join(tmp_dir, 'lldbinit'))
    logger.info("copying istio-proxy")
    shutil.copytree(ISTIO_PROXY_DIR, os.path.join(tmp_dir, "istio-proxy"),symlinks=True, ignore=shutil.ignore_patterns('^.git'))
    logger.info("copying istio-envoy")
    shutil.copytree(ISTIO_ENVOY_DIR, os.path.join(tmp_dir, "istio-envoy"), symlinks=True, ignore=shutil.ignore_patterns('^.git'))
    logger.info("copying cache source")
    for root, subdirs, files in os.walk('cache', followlinks=False):
        for f in files:
            name, ext = os.path.splitext(f)
            if ext in ('.h', '.cc', '.c', '.cpp') or os.path.islink(os.path.join(root, f)):
                f_path = os.path.join(root, f)
                copy_file(f_path, os.path.join(tmp_dir, f_path))

    IMAGE_NAME = 'dzdx/istio-debug-proxy:1.2.5'

    logger.info("start building")
    with open('Dockerfile.debug', 'rb') as f:
        for line in client.build(tag=IMAGE_NAME, path=tmp_dir):
            l = json.loads(line)
            if 'stream' in l:
                logger.info(l['stream'])
            elif 'error' in l:
                logger.error(l['error'])
finally:
    shutil.rmtree(tmp_dir)

