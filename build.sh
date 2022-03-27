#!/bin/bash

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv

  source .venv/bin/activate

  pip install wheel
else
  source .venv/bin/activate
fi

if [[ "$1" == "full" || ! -d "./dist" ]]; then
  python3 setup.py bdist_wheel
fi

buildctl build --frontend=dockerfile.v0 --local context=. --local dockerfile=. --output type=image,name=lenovonetapp.io/library/dsm-auth:1.0

ctr -n buildkit image export dsm-auth-1.0.tar lenovonetapp.io/library/dsm-auth:1.0
ctr image import ./dsm-auth-1.0.tar

scp ./dsm-auth-1.0.tar root@10.128.136.174:/root
ssh 10.128.136.174 ctr image import ./dsm-auth-1.0.tar

scp ./dsm-auth-1.0.tar root@10.128.136.175:/root
ssh 10.128.136.175 ctr image import ./dsm-auth-1.0.tar