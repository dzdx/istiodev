#!/bin/bash


reset(){
    kubectl scale --replicas=1 deploy istio-galley -n istio-system
    kubectl delete ep istio-sidecar-injector -n istio-system
    kubectl apply -f service.yaml
}

debug(){
    kubectl scale --replicas=0 deploy istio-galley -n istio-system
    kubectl apply -f service-debug.yaml
}


case "$1" in
  "reset")
    reset
    ;;
  "debug")
    debug
    ;;
  *)
    echo "reset or debug"
    exit 1
    ;;
esac
