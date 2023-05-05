#!/bin/bash

# Test if pipeline version is set
if [ -z ${PIPELINE_VERSION} ]; then 
    export PIPELINE_VERSION=1.8.4 
fi

echo "[1] Kubeflow pipeline version to be used: " $PIPELINE_VERSION

# Test if minio key id is set
if [ -z ${MINIO_KEY_ID} ]; then 
    export MINIO_KEY_ID=minio
fi

# Test if minio secret key is set
if [ -z ${MINIO_SECRET_KEY} ]; then 
    export MINIO_SECRET_KEY=minio123 
fi

echo "[2] Dowloading Kubectl"
if ! which kubectl; then
    curl -LOs https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl  > /dev/null
    chmod +x kubectl
    sudo mv ./kubectl /usr/local/bin/
fi

echo "[3] Dowloading K3s"
if ! which k3s; then
    curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--write-kubeconfig-mode 600 --disable traefik" sh -s
fi

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
sudo chmod 600 /etc/rancher/k3s/k3s.yaml
sudo chown $USER /etc/rancher/k3s/k3s.yaml


echo "[6] Install needed kubecflow CRDs"
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"

echo "[7] Wait for all CRDs to be ready"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io

echo "[8] Install Kubeflow pipelines"
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"

