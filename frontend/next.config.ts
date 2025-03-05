/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'fast-chat.s3.us-east-1.amazonaws.com',
      }
    ],
  },
  // ... any other existing configuration
}

module.exports = nextConfig