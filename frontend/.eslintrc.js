module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: 'babel-eslint'
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended'
  ],
  plugins: [
  ],
  // add your custom rules here
  rules: {
    'no-console': 'off',
    'vue/order-in-components': 'off',
    'vue/name-property-casing': 'off',
    'vue/component-name-in-template-casing': 'off',
    'vue/html-self-closing': 'off',
    'semi': 'off',
    'comma-dangle': 'off',
  },
}
