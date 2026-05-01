#!/usr/bin/env bash
# Devcontainer setup — clones dotfiles (if absent), runs install.sh, starts tailscaled.

set -e

# Clone dotfiles if VS Code didn't already (user-level dotfiles.repository setting may have).
if [ ! -d "$HOME/dotfiles" ]; then
    echo "==> Cloning RivasMario/dotfiles to ~/dotfiles..."
    git clone --depth=1 https://github.com/RivasMario/dotfiles.git "$HOME/dotfiles"
fi

# Normalize CRLF that may survive Windows-side clone (defensive).
find "$HOME/dotfiles" -name "*.sh" -exec sed -i 's/\r$//' {} +

# Run dotfiles installer — packages already baked into Dockerfile.
cd "$HOME/dotfiles"
export SKIP_PACKAGES=1
bash install.sh

# Start tailscaled if the feature provided it.
# Use real TUN when /dev/net/tun is available (runArgs), fall back to userspace.
if command -v tailscaled &>/dev/null && ! pgrep -x tailscaled &>/dev/null; then
    if [ -c /dev/net/tun ]; then
        echo "==> Starting tailscaled (kernel TUN)..."
        sudo tailscaled --socks5-server=localhost:1055 &>/dev/null &
    else
        echo "==> Starting tailscaled (userspace networking)..."
        sudo tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &>/dev/null &
    fi
    sleep 1
fi

# Allow vscode user to run tailscale without sudo.
if command -v tailscale &>/dev/null; then
    sudo tailscale set --operator="$USER" 2>/dev/null || true
    echo ""
    echo "==> Tailscale ready. Run: tailscale up --accept-dns=false --accept-routes --exit-node=100.81.194.15"
fi
