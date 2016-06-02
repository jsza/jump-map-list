import Immutable from 'immutable'
import {CALL_API, GET, POST} from '../middleware/api'


const LOAD_REQUEST = 'LEVELS_LOAD_REQUEST'
const LOAD_SUCCESS = 'LEVELS_LOAD_SUCCESS'
const LOAD_FAILURE = 'LEVELS_LOAD_FAILURE'

const ADD_REQUEST = 'LEVELS_ADD_REQUEST'
const ADD_SUCCESS = 'LEVELS_ADD_SUCCESS'
const ADD_FAILURE = 'LEVELS_ADD_FAILURE'

const UPDATE_REQUEST = 'LEVELS_UPDATE_REQUEST'
const UPDATE_SUCCESS = 'LEVELS_UPDATE_SUCCESS'
const UPDATE_FAILURE = 'LEVELS_UPDATE_FAILURE'

const DELETE_REQUEST = 'LEVELS_DELETE_REQUEST'
const DELETE_SUCCESS = 'LEVELS_DELETE_SUCCESS'
const DELETE_FAILURE = 'LEVELS_DELETE_FAILURE'

const DISMISS_LAST_DELETE = 'LEVELS_DISMISS_LAST_DELETE'

const LOAD_AUTHORS_REQUEST = 'LEVELS_LOAD_AUTHORS_REQUEST'
const LOAD_AUTHORS_SUCCESS = 'LEVELS_LOAD_AUTHORS_SUCCESS'
const LOAD_AUTHORS_FAILURE = 'LEVELS_LOAD_AUTHORS_FAILURE'

const ADD_AUTHOR_REQUEST = 'LEVELS_ADD_AUTHOR_REQUEST'
const ADD_AUTHOR_SUCCESS = 'LEVELS_ADD_AUTHOR_SUCCESS'
const ADD_AUTHOR_FAILURE = 'LEVELS_ADD_AUTHOR_FAILURE'

const REMOVE_AUTHOR_REQUEST = 'LEVELS_REMOVE_AUTHOR_REQUEST'
const REMOVE_AUTHOR_SUCCESS = 'LEVELS_REMOVE_AUTHOR_SUCCESS'
const REMOVE_AUTHOR_FAILURE = 'LEVELS_REMOVE_AUTHOR_FAILURE'


const AuthorState = Immutable.Record(
  { fetching: false
  , error: null
  , data: null
  })


const LastDelete = Immutable.Record(
  { id: null
  , name: null
  , soldier_tier: null
  , demoman_tier: null
  })


const initialState = Immutable.Record(
  { fetching: false
  , fetchingError: null
  , data: null
  , adding: false
  , addingError: null
  , updating: false
  , updatingError: null
  , deleting: false
  , deletingError: null
  , lastDelete: null
  , authors: new AuthorState()
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
    case UPDATE_REQUEST:
      return state.merge(
        { updating: true
        , updatingError: null
        })
    case UPDATE_SUCCESS:
      const playerClass = action.playerClass.toString()
      return state.set('updating', false).setIn(
        ['data', action.id, 'class_tiers', playerClass, 'tier'], action.tier)
    case UPDATE_FAILURE:
      return state.merge(
        { updating: false
        , updatingError: action.error
        })
    case DELETE_REQUEST:
      return state.merge(
        { deleting: true
        , deletingError: null
        })
    case DELETE_SUCCESS:
      let result = state
      const old = state.getIn(['data', action.id])
      if (old) {
        result = result.set('lastDelete', new LastDelete(
          { id: old.id
          , name: old.name
          , soldier_tier: old.soldier_tier
          , demoman_tier: old.demoman_tier
          }))
      }
      return result.set('deleting', false).removeIn(['data', action.id])
    case DELETE_FAILURE:
      return state.merge(
        { deleting: false
        , deletingError: action.error
        })
    case DISMISS_LAST_DELETE:
      return state.set('lastDelete', null)
    case LOAD_AUTHORS_REQUEST:
      return state.mergeIn(['authors'],
        { data: null
        , fetching: true
        , error: false
        })
    case LOAD_AUTHORS_SUCCESS:
      return state.mergeIn(['authors'],
        { fetching: false
        , data: new Immutable.OrderedMap(
            action.data.map((i) => [i.id, Immutable.fromJS(i)]))
        })
    case LOAD_AUTHORS_FAILURE:
      return state.mergeIn(['authors'],
        { fetching: false
        , error: action.error
        })
    case ADD_AUTHOR_SUCCESS:
      return state.setIn(['authors', 'data', action.data.id],
        Immutable.fromJS(action.data))
    case REMOVE_AUTHOR_SUCCESS:
      return state.removeIn(['authors', 'data', action.extraMapAuthorID])
    // case REMOVE_AUTHOR_SUCCESS:
    // case REMOVE_AUTHOR_FAILURE:
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
      , endpoint: `levels/list`
      }
    })
}


export function loadLevels() {
  return (dispatch, getState) => {
    const fetching = getState().levels.fetching
    if (fetching) {
      return null
    }
    return dispatch(fetch())
  }
}


export function addLevel(name) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [ADD_REQUEST]
      , success: [ADD_SUCCESS]
      , failure: [ADD_FAILURE]
      , endpoint: `levels/add/${name}`
      }
    , name
    })
}


export function updateLevel(id, playerClass, tier) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [UPDATE_REQUEST]
      , success: [UPDATE_SUCCESS]
      , failure: [UPDATE_FAILURE]
      , endpoint: `levels/id/${id}/tier/${playerClass}/${tier}`
      }
    , id
    , playerClass
    , tier
    })
}


export function deleteLevel(id) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [DELETE_REQUEST]
      , success: [DELETE_SUCCESS]
      , failure: [DELETE_FAILURE]
      , endpoint: `levels/id/${id}/delete`
      }
    , id
    })
}


export function dismissLastDelete() {
  return (
    { type: DISMISS_LAST_DELETE
    })
}


function doUndoLastDelete(lastDelete) {
  const {name} = lastDelete
  const soldier = lastDelete.soldier_tier
  const demoman = lastDelete.demoman_tier
  return (
    { [CALL_API]:
      { method: POST
      , started: [ADD_REQUEST]
      , success: [ADD_SUCCESS, DISMISS_LAST_DELETE]
      , failure: [ADD_FAILURE]
      , endpoint: `levels/add/${name}?soldier=${soldier}&demoman=${demoman}`
      }
    , name
    })
}


export function undoLastDelete() {
  return (dispatch, getState) => {
    const {lastDelete} = getState().levels
    dispatch(doUndoLastDelete(lastDelete))
  }
}


export function loadLevelAuthors(id) {
  return (
    { [CALL_API]:
      { method: GET
      , started: [LOAD_AUTHORS_REQUEST]
      , success: [LOAD_AUTHORS_SUCCESS]
      , failure: [LOAD_AUTHORS_FAILURE]
      , endpoint: `levels/id/${id}/authors/list`
      }
    , id
    })
}


export function addLevelAuthor(extraMapID, author) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [ADD_AUTHOR_REQUEST]
      , success: [ADD_AUTHOR_SUCCESS]
      , failure: [ADD_AUTHOR_FAILURE]
      , endpoint: `levels/id/${extraMapID}/authors/add/${author.id}`
      }
    })
}


export function removeLevelAuthor(extraMapID, author) {
  const authorID = author.author_id
  return (
    { [CALL_API]:
      { method: POST
      , started: [REMOVE_AUTHOR_REQUEST]
      , success: [REMOVE_AUTHOR_SUCCESS]
      , failure: [REMOVE_AUTHOR_FAILURE]
      , endpoint: `levels/id/${extraMapID}/authors/remove/${authorID}`
      }
    , extraMapID
    , authorID
    , extraMapAuthorID: author.id
    })
}
