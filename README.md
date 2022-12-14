Authentication Module: The Python authentication Library for DXN
================================================================

VERSION: 1.0.0

First of all, it is recommended to create a python virtual environment to
play around.

### Step 1
For a Python 3 virtual environment type, to create virtual environment with 
the command:
```
python3 -m venv .venv
```
This will create a directory `.venv` along with directories inside it 
containing a copy of the Python interpreter, the standard library, and various supporting files.

### Step 2
To add modules and packages in our Environment, we need to activate it first.
In order to package the whole moduel as a wheel package, we have to install 
wheel module as well.
```
source .venv/bin/activate

pip install wheel
```

## Step 3
To build `dsa_auth` as a wheel package.
```
python3 setup.py bdist_wheel
```

### Step 4
Download buildkit latest release from the [link](https://github.com/moby/buildkit/releases) and install it.

In k3s environment, you need to start `buildkitd` with the parameter 
`--containerd-worker-addr /run/k3s/containerd/containerd.sock`
And then, you can build containerd image as follow:
```
buildctl build --frontend=dockerfile.v0 --local context=. --local dockerfile=. --output type=image,name=lenovonetapp.io/library/dsm-auth:1.0

ctr -n buildkit image export dsm_auth-1.0.tar lenovonetapp.io/library/dsm-auth:1.0
```
By default, the image built by buildctl is in `buildkit` namespace. You can 
use the parameter `--namespace=default` to set the namespace for the image.

### Step 5
Copy the image dsm_auth-1.0.tar to each K3S node and then import them on 
each node.
```
ctr image import dsm_auth-1.0.tar
```

### Step 6
Deploy all the yaml files in the directory `yaml`. There are including the 
following yaml files:
1. ingress.yaml: create a ingress resource, which will leverage Traefik 
   middleware `authentication-middleware` defined in `middleware.yaml` for 
   authentication. After that, the request will forward to web service.
2. middleware.yaml: Generate Traefik middleware, which will forward the 
   request to `dsm_auth` service.
3. cm_dsm_auth.yaml: Define the configuration for dsm_auth service, 
   including database configuration, flask configuration.
4. deploy_dsm_auth.yaml: Deploy `dsm-auth` service for authentication.
5. deploy_web_service.yaml: Deploy `web-service` service.

The user can run the command `kubectl apply -R -f ./yaml` to deploy all the 
resources.

### Step 7
User can use the curl command to verify:
```angular2html
curl http://root:xuanyuan=1@10.128.131.240:32080/hello/  -H "Host:management.magnascale.com"
```


## NOTICE:
In this demo, the user has to run `python3 manager.py` in `dsm_auth` pod to 
inject the authentication user first.
