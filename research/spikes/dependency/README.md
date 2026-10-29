# Dependency compatibility spike

This is a research probe, not connector implementation. It verifies that the exact runtime and package graph can be installed and imported together.

```sh
export PATH="$PWD/.node24/bin:$PATH"
curl -fSLo node-v24.22.1-linux-x64.tar.xz https://nodejs.org/dist/v24.22.1/node-v24.22.1-linux-x64.tar.xz
echo "6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6  node-v24.22.1-linux-x64.tar.xz" | sha256sum -c -
mkdir -p .node24
tar -xJf node-v24.22.1-linux-x64.tar.xz -C .node24 --strip-components=1
node --version
npm --version
cd research/spikes/dependency
npm ci --ignore-scripts --no-audit --no-fund
./node_modules/.bin/tsc -p tsconfig.json
npm audit --omit=dev
```

Expected: Node `v24.22.1`, npm `11.19.1`, a matching checksum, exit 0 from TypeScript, and no Critical production audit finding. The final lockfile includes the mutation tools and the archived output records the clean verification.
