import React from 'react'
import {SUPERUSER} from '../utils/LoginData'

import LevelsApp from './LevelsApp'
import UsersApp from './UsersApp'


export default class App extends React.Component {
  render() {
    return (
      <div>
        <a href="/logout" className="pull-right">Sign out</a>
        <LevelsApp />
        {SUPERUSER
        ? <UsersApp />
        : null}
      </div>
    )
  }
}
