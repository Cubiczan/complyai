/** @type {import('next').NextConfig} */
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  outputFileTracingRoot: path.join(__dirname),
  webpack: (config) => {
    config.resolve.alias['@'] = __dirname;
    return config;
  },
}

export default nextConfig
