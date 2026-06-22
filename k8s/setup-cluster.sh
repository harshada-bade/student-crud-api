#!/bin/bash

set -e

echo "Starting 3-node Minikube cluster..."
minikube start --nodes 3 --driver=docker

echo "Waiting for nodes to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=120s

echo "Labeling nodes..."
kubectl label nodes minikube type=application --overwrite
kubectl label nodes minikube-m02 type=database --overwrite
kubectl label nodes minikube-m03 type=dependent_services --overwrite

echo "Cluster setup complete! Current nodes and labels:"
kubectl get nodes --show-labels
