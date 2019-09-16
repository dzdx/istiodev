#!/bin/bash


reset(){
    kubectl delete ep istio-pilot -n istio-system
    kubectl apply -f service.yaml
}

debug(){
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
