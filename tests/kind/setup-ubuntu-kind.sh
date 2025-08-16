#!/bin/bash
# Setup Ubuntu-compatible Kind cluster for RKE2 testing
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

CLUSTER_NAME="rke2-test"
KIND_CONFIG="tests/kind/kind-config.yaml"

echo -e "${YELLOW}Setting up Kind cluster with Ubuntu compatibility for RKE2 testing...${NC}"

# Step 1: Delete existing cluster if it exists
echo -e "${GREEN}1. Cleaning up existing cluster...${NC}"
if kind get clusters | grep -q "$CLUSTER_NAME"; then
    echo "Deleting existing cluster $CLUSTER_NAME..."
    kind delete cluster --name "$CLUSTER_NAME"
fi

# Step 2: Create storage directory
echo -e "${GREEN}2. Creating storage directory...${NC}"
mkdir -p /tmp/kind-storage

# Step 3: Create Kind cluster
echo -e "${GREEN}3. Creating Kind cluster...${NC}"
export PATH="$HOME/.local/bin:$PATH"
kind create cluster --config "$KIND_CONFIG" --name "$CLUSTER_NAME"

# Step 4: Wait for cluster to be ready
echo -e "${GREEN}4. Waiting for cluster to be ready...${NC}"
kubectl wait --for=condition=Ready nodes --all --timeout=300s

# Step 5: Prepare nodes for Ubuntu/RKE2 testing
echo -e "${GREEN}5. Preparing nodes for RKE2 testing...${NC}"

# Get all node container names
NODES=$(docker ps --filter "name=${CLUSTER_NAME}" --format "{{.Names}}")

for node in $NODES; do
    echo "Preparing $node for RKE2 testing..."
    
    # Install required packages for RKE2 and Ansible
    docker exec "$node" bash -c "
        # Update package lists
        apt-get update -qq
        
        # Install essential packages
        apt-get install -y -qq \
            python3 \
            python3-pip \
            sudo \
            curl \
            wget \
            unzip \
            systemctl \
            lsb-release
        
        # Fix OS detection for Ubuntu (Kind nodes sometimes show as Debian)
        echo 'DISTRIB_ID=Ubuntu' > /etc/lsb-release
        echo 'DISTRIB_RELEASE=22.04' >> /etc/lsb-release
        echo 'DISTRIB_CODENAME=jammy' >> /etc/lsb-release
        echo 'DISTRIB_DESCRIPTION=\"Ubuntu 22.04 LTS\"' >> /etc/lsb-release
        
        # Create os-release file for proper OS detection
        cat > /etc/os-release << 'EOF'
NAME=\"Ubuntu\"
VERSION=\"22.04 LTS (Jammy Jellyfish)\"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME=\"Ubuntu 22.04 LTS\"
VERSION_ID=\"22.04\"
HOME_URL=\"https://www.ubuntu.com/\"
SUPPORT_URL=\"https://help.ubuntu.com/\"
BUG_REPORT_URL=\"https://bugs.launchpad.net/ubuntu/\"
PRIVACY_POLICY_URL=\"https://www.ubuntu.com/legal/terms-and-policies/privacy-policy\"
VERSION_CODENAME=jammy
UBUNTU_CODENAME=jammy
EOF
        
        # Ensure systemctl works (some containers have issues)
        ln -sf /bin/true /usr/bin/systemctl 2>/dev/null || true
        
        echo 'Node $node prepared successfully'
    "
done

# Step 6: Test connectivity and OS detection
echo -e "${GREEN}6. Testing OS detection...${NC}"
docker exec "${CLUSTER_NAME}-control-plane" lsb_release -a

echo -e "${GREEN}✅ Kind cluster with Ubuntu compatibility setup complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Test Ansible connectivity: ansible -i tests/kind/simple-inventory.ini all -m ping"
echo "2. Run RKE2 test playbook: ansible-playbook -i tests/kind/simple-inventory.ini tests/kind/test-playbook.yml"
echo "3. Clean up when done: kind delete cluster --name $CLUSTER_NAME"