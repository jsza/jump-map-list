import {combineReducers} from 'redux'

import levels from './levels'
import users from './users'
import avatars from './avatars'
import media from './media'
import authors from './authors'


export default combineReducers(
  { levels
  , users
  , avatars
  , media
  , authors
  })
