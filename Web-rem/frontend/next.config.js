module.exports = {
  experimental: {
    async rewrites() {
      return [
        {
          source: "api/v1/login",
          destination: `http://localhost:8000/login`
        },
        {
          source: "api/v1/logout",
          destination : `http://localhost:8000/logout`
        },
        {
          source: "api/v1/:route*",
          destination: `http://localhost:8000/api/v1/:route*`
        }
      ];
    }
  }
}