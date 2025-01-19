const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  devServer: {
    allowedHosts: "all",
  },
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "Song of the Week";
      return args;
    });
  },
  configureWebpack: {
    optimization: {
      minimize: true, // Ensure minimization is enabled
      minimizer: [
        new (require("terser-webpack-plugin"))({
          terserOptions: {
            compress: {
              drop_console: false, // Keep console logs for debugging
              drop_debugger: false, // Keep debugger statements
            },
            mangle: false, // Prevent variable and function name mangling
          },
        }),
      ],
    },
  },
});
