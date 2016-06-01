import 'babel-core/polyfill'
import React from 'react'
import ReactDOM from 'react-dom'
import {Provider} from 'react-redux'
import APIUtils from './utils/APIUtils'
import configureStore from './store/configureStore'

import App from './containers/App'

import '../stylus/index.styl'


function main() {
  const api = new APIUtils()
  const store = configureStore(api)
  ReactDOM.render(
    <Provider store={store}>
      <App />
    </Provider>,
    document.getElementById('app')
  )
}
main()

