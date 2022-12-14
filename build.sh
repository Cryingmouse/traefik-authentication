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

nerdctl build -t lenovonetapp.io/library/dsm_auth:1.0 .

ctr image export dsm_auth-1.0.image lenovonetapp.io/library/dsm_auth:1.0

scp ./dsm_auth-1.0.image root@node-1:/root
ssh node-1 ctr image import ./dsm_auth-1.0.image
ssh node-1 rm /root/dsm_auth-1.0.image

scp ./dsm_auth-1.0.image root@node-2:/root
ssh node-2 ctr image import ./dsm_auth-1.0.image
ssh node-2 rm /root/dsm_auth-1.0.image

scp ./dsm_auth-1.0.image root@node-3:/root
ssh node-3 ctr image import ./dsm_auth-1.0.image
ssh node-3 rm /root/dsm_auth-1.0.image

scp ./dsm_auth-1.0.image root@node-4:/root
ssh node-4 ctr image import ./dsm_auth-1.0.image
ssh node-4 rm /root/dsm_auth-1.0.image

scp ./dsm_auth-1.0.image root@node-5:/root
ssh node-5 ctr image import ./dsm_auth-1.0.image
ssh node-5 rm /root/dsm_auth-1.0.image

scp ./dsm_auth-1.0.image root@node-6:/root
ssh node-6 ctr image import ./dsm_auth-1.0.image
ssh node-6 rm /root/dsm_auth-1.0.image

rm ./dsm_auth-1.0.image
