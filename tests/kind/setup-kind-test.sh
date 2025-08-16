#!/bin/bash
# Setup script for Kind-based testing of RKE2 Ansible collection
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CLUSTER_NAME="rke2-test"
KIND_CONFIG="tests/kind/kind-config.yaml"
TEST_INVENTORY="tests/kind/test-inventory.ini"
SSH_KEY="~/.ssh/kind-test-key"

echo -e "${YELLOW}Setting up Kind cluster for RKE2 testing...${NC}"

# Step 1: Create storage directory for testing
echo -e "${GREEN}1. Creating storage directory...${NC}"
sudo mkdir -p /tmp/kind-storage
sudo chmod 777 /tmp/kind-storage

# Step 2: Generate SSH key if it doesn't exist
echo -e "${GREEN}2. Setting up SSH key...${NC}"
if [ ! -f ~/.ssh/kind-test-key ]; then
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/kind-test-key -N "" -C "kind-test-key"
    echo "SSH key generated at ~/.ssh/kind-test-key"
else
    echo "SSH key already exists"
fi

# Step 3: Create Kind cluster
echo -e "${GREEN}3. Creating Kind cluster...${NC}"
if kind get clusters | grep -q "$CLUSTER_NAME"; then
    echo "Cluster $CLUSTER_NAME already exists. Deleting and recreating..."
    kind delete cluster --name "$CLUSTER_NAME"
fi

kind create cluster --config "$KIND_CONFIG" --name "$CLUSTER_NAME"

# Step 4: Wait for cluster to be ready
echo -e "${GREEN}4. Waiting for cluster to be ready...${NC}"
kubectl wait --for=condition=Ready nodes --all --timeout=300s

# Step 5: Set up Docker access to Kind nodes
echo -e "${GREEN}5. Setting up SSH access to Kind nodes...${NC}"

# Get Kind node container names
CONTROL_PLANE=$(docker ps --filter "name=${CLUSTER_NAME}-control-plane" --format "{{.Names}}")
WORKER1=$(docker ps --filter "name=${CLUSTER_NAME}-worker" --format "{{.Names}}" | head -1)
WORKER2=$(docker ps --filter "name=${CLUSTER_NAME}-worker" --format "{{.Names}}" | tail -1)

echo "Control plane: $CONTROL_PLANE"
echo "Worker 1: $WORKER1"
echo "Worker 2: $WORKER2"

# Copy SSH public key to nodes
for node in $CONTROL_PLANE $WORKER1 $WORKER2; do
    echo "Setting up SSH access for $node"
    
    # Install SSH server in Kind node
    docker exec "$node" bash -c "
        apt-get update -qq && 
        apt-get install -y -qq openssh-server &&
        mkdir -p /root/.ssh &&
        chmod 700 /root/.ssh &&
        systemctl enable ssh &&
        systemctl start ssh
    "
    
    # Copy SSH public key
    docker cp ~/.ssh/kind-test-key.pub "$node:/root/.ssh/authorized_keys"
    docker exec "$node" chmod 600 /root/.ssh/authorized_keys
    
    # Set up port forwarding for SSH access
    case $node in
        *control-plane*)
            docker exec "$node" bash -c "sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config && systemctl restart ssh"
            ;;
        *worker*)
            if [ "$node" = "$WORKER1" ]; then
                docker exec "$node" bash -c "sed -i 's/#Port 22/Port 2223/' /etc/ssh/sshd_config && systemctl restart ssh"
            else
                docker exec "$node" bash -c "sed -i 's/#Port 22/Port 2224/' /etc/ssh/sshd_config && systemctl restart ssh"
            fi
            ;;
    esac
done

# Step 6: Test connectivity
echo -e "${GREEN}6. Testing connectivity...${NC}"
kubectl get nodes -o wide

echo -e "${GREEN}✅ Kind cluster setup complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Test Ansible connectivity: ansible -i $TEST_INVENTORY all -m ping"
echo "2. Run your RKE2 playbooks against the Kind cluster"
echo "3. Clean up when done: kind delete cluster --name $CLUSTER_NAME"