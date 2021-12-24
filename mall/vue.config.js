// 跨域配置
module.exports = {
  devServer: {
    proxy: { // 设置代理到服务接口,解决跨域问题
      '/api': {
        target: 'http://127.0.0.1:5000/', // 代理的目标地址
        changeOrigin: true,
        pathRewrite: {
          '^api': ''
        }
      }
    }
  },
  // 防止eslint报错
  lintOnSave: false
}
