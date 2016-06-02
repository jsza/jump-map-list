import Immutable from 'immutable'
import {CALL_API, GET, POST} from '../middleware/api'


const LOAD_REQUEST = 'MEDIA_LOAD_REQUEST'
const LOAD_SUCCESS = 'MEDIA_LOAD_SUCCESS'
const LOAD_FAILURE = 'MEDIA_LOAD_FAILURE'

const ADD_REQUEST = 'MEDIA_ADD_REQUEST'
const ADD_SUCCESS = 'MEDIA_ADD_SUCCESS'
const ADD_FAILURE = 'MEDIA_ADD_FAILURE'

const DELETE_REQUEST = 'MEDIA_DELETE_REQUEST'
const DELETE_SUCCESS = 'MEDIA_DELETE_SUCCESS'
const DELETE_FAILURE = 'MEDIA_DELETE_FAILURE'


const initialState = Immutable.Record(
  { selectedLevelID: null
  , fetching: false
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
      return state.merge(
          { selectedLevelID: null
          , fetching: false
          , fetchingError: null
          // , data: null
          , adding: false
          , addingError: null
          , deleting: false
          , deletingError: null
          })
    case LOAD_SUCCESS:
      let data = Immutable.OrderedMap()
      action.data.forEach((item) => {
        data = data.set(item.id, Immutable.fromJS(item))
      })
      return state.merge(
        { selectedLevelID: action.levelID
        , fetching: false
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


function fetch(levelID) {
  return (
    { [CALL_API]:
      { method: GET
      , started: [LOAD_REQUEST]
      , success: [LOAD_SUCCESS]
      , failure: [LOAD_FAILURE]
      , endpoint: `levels/id/${levelID}/media/list`
      }
    , levelID
    })
}


export function loadMedia(levelID) {
  return (dispatch, getState) => {
    const {media} = getState()
    if (media.fetching) {
      return null
    }
    if (!levelID) {
      levelID = media.selectedLevelID
    }
    if (!levelID) {
      throw 'no level ID found to refresh media'
    }
    return dispatch(fetch(levelID))
  }
}


export function addMedia(levelID, mediaType, url) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [ADD_REQUEST]
      , success: [ADD_SUCCESS]
      , failure: [ADD_FAILURE]
      , endpoint: `levels/id/${levelID}/media/add/${mediaType}`
      , data: url
      }
    })
}


export function deleteMedia(id) {
  return (
    { [CALL_API]:
      { method: POST
      , started: [DELETE_REQUEST]
      , success: [DELETE_SUCCESS]
      , failure: [DELETE_FAILURE]
      , endpoint: `levelmedia/id/${id}/delete`
      }
    , id
    })
}


function moveMedia(levelMediaID, newIndex) {
  if (newIndex < 1) {
    throw 'should not try to move items to index < 1'
  }
  return (
    { [CALL_API]:
      { method: POST
      , success: [loadMedia]
      , endpoint: `levelmedia/id/${levelMediaID}/move/${newIndex}`
      }
    })
}


export function moveMediaUp(levelMediaID) {
  return (dispatch, getState) => {
    const {data} = getState().media
    const item = data.get(levelMediaID).toJS()
    if (item) {
      const newIndex = item.index - 1
      dispatch(moveMedia(levelMediaID, newIndex))
    }
  }
}


export function moveMediaDown(levelMediaID) {
  return (dispatch, getState) => {
    const {data} = getState().media
    const item = data.get(levelMediaID).toJS()
    if (item) {
      const newIndex = item.index + 1
      dispatch(moveMedia(levelMediaID, newIndex))
    }
  }
}
