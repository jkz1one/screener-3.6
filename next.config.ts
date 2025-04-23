import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/autowatchlist",
        destination: "http://localhost:8008/autowatchlist",
      },
    ];
  },
};

export default nextConfig;
