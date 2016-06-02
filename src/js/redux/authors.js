import Immutable from 'immutable'
import {CALL_API, GET, POST} from '../middleware/api'


const LOAD_REQUEST = 'AUTHORS_LOAD_REQUEST'
const LOAD_SUCCESS = 'AUTHORS_LOAD_SUCCESS'
const LOAD_FAILURE = 'AUTHORS_LOAD_FAILURE'

const ADD_REQUEST = 'AUTHORS_ADD_REQUEST'
const ADD_SUCCESS = 'AUTHORS_ADD_SUCCESS'
const ADD_FAILURE = 'AUTHORS_ADD_FAILURE'


const initialState = Immutable.Record(
  { fetching: false
  , fetchingError: null
  , data: null
  , adding: false
  , addingError: null
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
    default:
      return state
  }
}


export function loadAuthors(string) {
  let endpoint
  if (!string || !string.trim().length) {
    endpoint = 'authors/list'
  }
  else {
    endpoint = `authors/list?search=${string}`
  }
  return (
    { [CALL_API]:
      { method: GET
      , started: [LOAD_REQUEST]
      , success: [LOAD_SUCCESS]
      , failure: [LOAD_FAILURE]
      , endpoint: endpoint
      }
    })
}


export function addAuthor(name, url) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [ADD_REQUEST]
      , success: [ADD_SUCCESS]
      , failure: [ADD_FAILURE]
      , endpoint: `authors/add/${name}`
      , data: url
      }
    })
}


export function deleteAuthor(id) {
  return (
    { [CALL_API]:
      { method: POST
      , started: []
      , success: [loadAuthors]
      , failure: []
      , endpoint: `authors/${id}/remove`
      }
    })
}

