const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // 代理到后端服务器地址
        changeOrigin: true,
        pathRewrite: { '^/api': '' }, // 重写路径，将 /api 移除
      },
    },
  },
};