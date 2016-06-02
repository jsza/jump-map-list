import 'babel-core/polyfill'
import React from 'react'
import ReactDOM from 'react-dom'
import {Router, Route, IndexRoute, browserHistory} from 'react-router'
import {Provider} from 'react-redux'
import APIUtils from './utils/APIUtils'
import configureStore from './store/configureStore'
import {SUPERUSER} from './utils/LoginData'

import App from './containers/App'
import LevelsApp from './containers/LevelsApp'
import UsersApp from './containers/UsersApp'
import AuthorsApp from './containers/AuthorsApp'

import '../stylus/index.styl'


function main() {
  const api = new APIUtils()
  const store = configureStore(api)
  ReactDOM.render(
    <Provider store={store}>
      <Router history={browserHistory}>
        <Route component={App} path="/">
          <IndexRoute component={LevelsApp} />
          <Route component={AuthorsApp} path="authors" />
          {SUPERUSER ? <Route component={UsersApp} path="users" /> : null}
        </Route>
      </Router>
    </Provider>,
    document.getElementById('app')
  )
}
main()

