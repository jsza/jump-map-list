import {createStore, applyMiddleware, compose} from 'redux'
import thunkMiddleware from 'redux-thunk'
import rootReducer from '../redux/reducer'
import apiMiddleware from '../middleware/api'
import avatarMiddleware from '../middleware/steamAvatar'


export default function configureStore(api, initialState) {
  const store = compose(
    applyMiddleware(
      thunkMiddleware,
      apiMiddleware(api),
      avatarMiddleware()
    )
  )(createStore)(rootReducer, initialState)

  if (module.hot) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept('../redux/reducer', () => {
      const nextRootReducer = require('../redux/reducer')
      store.replaceReducer(nextRootReducer)
    })
  }

  return store
}
