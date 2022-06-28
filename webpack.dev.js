const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    hot: true,
    proxy: {
      '!/static/frontend/**': {
        target: 'http://localhost:8000', // points to django dev server
        changeOrigin: true,
      }
    }
  }
})