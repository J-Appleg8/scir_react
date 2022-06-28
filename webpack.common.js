const path = require('path')

module.exports = {
  entry: {
    colors: './frontend/colors/index.js', // path to our input file
  },
  output: {
    filename: '[name].js',  // output bundle file name
    path: path.resolve(__dirname, 'project/static/frontend'),  // path to our Django static directory
    publicPath: '/static/frontend/',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: { presets: ["@babel/preset-env", "@babel/preset-react"] }
      },
    ]
  },
}