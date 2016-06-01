import Immutable from 'immutable'
import {CALL_API, GET, POST} from '../middleware/api'


const LOAD_REQUEST = 'USERS_LOAD_REQUEST'
const LOAD_SUCCESS = 'USERS_LOAD_SUCCESS'
const LOAD_FAILURE = 'USERS_LOAD_FAILURE'

const ADD_REQUEST = 'USERS_ADD_REQUEST'
const ADD_SUCCESS = 'USERS_ADD_SUCCESS'
const ADD_FAILURE = 'USERS_ADD_FAILURE'

const DELETE_REQUEST = 'USERS_DELETE_REQUEST'
const DELETE_SUCCESS = 'USERS_DELETE_SUCCESS'
const DELETE_FAILURE = 'USERS_DELETE_FAILURE'


const initialState = Immutable.Record(
  { fetching: false
  , fetchingError: null
  , data: null
  , adding: false
  , addingError: null
  , deleting: false
  , deletingError: null
  })


export default function reducer(state=new initialState(), action) {
  switch (action.type) {
    case LOAD_REQUEST:
      return state.merge(new initialState())
    case LOAD_SUCCESS:
      let data = Immutable.OrderedMap()
      action.data.forEach((item) => {
        data = data.set(item.id, Immutable.fromJS(item))
      })
      return state.merge(
        { fetching: false
        , data: data
        })
    case LOAD_FAILURE:
      return state.merge(
        { fetching: false
        , fetchingError: action.error
        })
    case ADD_REQUEST:
      return state.merge(
        { adding: true
        , addingError: null
        })
    case ADD_SUCCESS:
      return state.set('adding', false).setIn(['data', action.data.id],
        Immutable.fromJS(action.data))
    case ADD_FAILURE:
      return state.merge(
        { adding: false
        , addingError: action.error
        })
    case DELETE_REQUEST:
      return state.merge(
        { deleting: true
        , deletingError: null
        })
    case DELETE_SUCCESS:
      return state.set('deleting', false).removeIn(['data', action.id])
    case DELETE_FAILURE:
      return state.merge(
        { deleting: false
        , deletingError: action.error
        })
    default:
      return state
  }
}


function fetch() {
  return (
    { [CALL_API]:
      { method: GET
      , started: [LOAD_REQUEST]
      , success: [LOAD_SUCCESS]
      , failure: [LOAD_FAILURE]
      , endpoint: 'users/list'
      }
    })
}


export function loadUsers() {
  return (dispatch, getState) => {
    const fetching = getState().levels.fetching
    if (fetching) {
      return null
    }
    return dispatch(fetch())
  }
}


export function addUser(steamID, superuser) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [ADD_REQUEST]
      , success: [ADD_SUCCESS]
      , failure: [ADD_FAILURE]
      , endpoint: `users/add/${steamID}?superuser=${superuser}`
      }
    })
}


export function deleteUser(id) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [DELETE_REQUEST]
      , success: [DELETE_SUCCESS]
      , failure: [DELETE_FAILURE]
      , endpoint: `users/${id}/delete`
      }
    , id
    })
}
