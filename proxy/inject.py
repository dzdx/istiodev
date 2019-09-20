import argparse
import subprocess
from io import StringIO
import yaml
import re


parser = argparse.ArgumentParser(description='inject debug proxy sidecar')
parser.add_argument('-f', required=True, dest='file', help='deployment file path')
args = parser.parse_args()


def main():
    proc = subprocess.Popen(["istioctl", "kube-inject", "-f", args.file], stdout=subprocess.PIPE)
    try:
        outs, errs = proc.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    if errs:
        print(errs)
        return
    outs = outs.decode('utf-8')
    res_yamls = []
    for out in re.split(r'-{3,}', outs):
        if not out.strip():
            continue
        buf = StringIO(out)
        res = yaml.load(buf)
        if res['kind'] == 'Deployment':
            res['spec']['template']['metadata']['annotations']['sidecar.istio.io/inject'] = 'false'
            containers = res['spec']['template']['spec']['containers']
            for container in containers:
                if container['name'] == 'istio-proxy':
                    container['securityContext']['capabilities'] = {
                        'add': ['NET_ADMIN', 'SYS_PTRACE']
                    }
                    container['image'] = 'dzdx/istio-debug-proxy:1.2.5'
                    del container['readinessProbe']
        buf = StringIO()
        yaml.dump(res, buf)
        res_yamls.append(buf.getvalue())
    print('---\n'.join(res_yamls))
if __name__ == '__main__':
    main()
