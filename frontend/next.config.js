/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",   // required for Docker / Vercel optimised builds
  reactStrictMode: true,
};

module.exports = nextConfig;