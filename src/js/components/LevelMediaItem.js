import React, {PropTypes as P} from 'react'
import IP from 'react-immutable-proptypes'

import {Image, ResponsiveEmbed} from 'react-bootstrap'
import TimeAgo from 'react-timeago'
import SteamAvatarContainer from '../containers/SteamAvatarContainer'


export default class LevelMediaItem extends React.Component {
  moveUp(e) {
    const {id} = this.props.data
    if (this.props.first) {
      return
    }
    this.props.moveMediaUp(id)
  }

  moveDown(e) {
    const {id} = this.props.data
    if (this.props.last) {
      return
    }
    this.props.moveMediaDown(id)
  }

  onClickDelete(e) {
    e.preventDefault()
    this.props.deleteMedia(this.props.data.id)
  }

  render() {
    const {first, last} = this.props
    const {media_type, url, id, adder_steamid, timestamp} = this.props.data
    // const youtube = `https://www.youtube.com/v/${url}`
    return (
      <div className="list-group-item level-media-item clearfix">
        <div className="level-media-container">
          { media_type === 0
          ? <a href={url}><Image src={url} thumbnail /></a>
          : <ResponsiveEmbed a16by9 key={id}>
              <iframe ref="iframe"
                src={`https://www.youtube.com/embed/${url}`}
                frameBorder="0"
                allowFullScreen />
            </ResponsiveEmbed>
          }
        </div>
        <span className="remove">
          <a href="#" onClick={this.onClickDelete.bind(this)}>
            Delete
          </a>
        </span>
        <ul className="level-media-info-list">
          <li>
            Added by
            <span> </span>
            <strong style={{display: 'inline-block'}}>
              <SteamAvatarContainer
                steamID64={adder_steamid}
                size="tiny"
                showName
                />
            </strong>
          </li>
          <li>
            <i><TimeAgo date={timestamp*1000} /></i>
          </li>
        </ul>
        <span className="order-up" disabled={first} onClick={(e) => this.moveUp(e)}>
          <i className="fa fa-chevron-up" />
        </span>
        <span className="order-down" disabled={last} onClick={(e) => this.moveDown(e)}>
          <i className="fa fa-chevron-down" />
        </span>
      </div>
    )
  }
}


LevelMediaItem.propTypes =
  { data: P.object.isRequired
  , first: P.bool.isRequired
  , last: P.bool.isRequired
  , moveMediaUp: P.func.isRequired
  , moveMediaDown: P.func.isRequired
  , deleteMedia: P.func.isRequired
  }
