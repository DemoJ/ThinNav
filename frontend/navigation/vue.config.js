const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // 本地的接口
        // target: 'http://10.11.0.10:8888/api', // 线上的接口
        changeOrigin: true,
        pathRewrite: { '^/api': '' }, // 重写路径，将 /api 移除
      },
    },
  },
};