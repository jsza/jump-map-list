import 'babel-core/polyfill'
import React from 'react'
import ReactDOM from 'react-dom'
import {Provider} from 'react-redux'
import APIUtils from './utils/APIUtils'
import configureStore from './store/configureStore'

import LevelsApp from './containers/LevelsApp'

import '../stylus/main.styl'


function main() {
  const api = new APIUtils()
  const store = configureStore(api)
  ReactDOM.render(
    <Provider store={store}>
      <LevelsApp />
    </Provider>,
    document.getElementById('app')
  )
}
main()

