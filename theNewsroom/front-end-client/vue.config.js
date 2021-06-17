module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/vuetify'
    : '/',
  "transpileDependencies": [
    "vuetify"
  ],
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:3001"
      },
      "^/graphql": {
        target: "http://localhost:5000",
        changeOrigin: true,
        secure: false, 
        pathRewrite: {'^/graphql': '/graphql'},
        logLevel: 'debug'
      }
    }
  }
}