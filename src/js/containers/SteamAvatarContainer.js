import React, {PropTypes as P} from 'react'
import {connect} from 'react-redux'
import cx from 'classnames'
import steam from 'steamidconvert'

import {queueAvatar} from '../redux/avatars'


const Steam = steam()


const url = 'https://static.tempus.xyz/website/img/avatar_'
const defaultAvatars = {
  'tiny':        url + '32x32.jpg',
  'mini':        url + '32x32.jpg',
  'small':       url + '32x32.jpg',
  'medium':      url + '64x64.jpg',
  'mediumlarge': url + '64x64.jpg',
  'large':       url + '184x184.jpg'
}


class SteamAvatar extends React.Component {
  constructor(props) {
    super(props)
  }

  componentDidMount() {
    this.props.queueAvatar([this.getSteamID()])
  }

  getSteamID() {
    if (this.props.steamID64) {
      return this.props.steamID64
    }
    return Steam.convertTo64(this.props.steamID)
  }

  getSteamInfo() {
    if (this.props.avatars) {
      return this.props.avatars[this.getSteamID()]
    }
  }

  getAvatarURL() {
    const steamInfo = this.getSteamInfo()
    if (steamInfo) {
      if (['mini', 'tiny'].includes(this.props.size)) {
        return steamInfo.avatar['small']
      }
      else if (this.props.size === 'mediumlarge') {
        return steamInfo.avatar['large']
      }
      return steamInfo.avatar[this.props.size]
    }
    else {
      return defaultAvatars[this.props.size]
    }
  }

  makeURL() {
    return 'http://steamcommunity.com/profiles/' + this.getSteamID()
  }

  onClick(event) {
    event.stopPropagation()
  }

  getStatus() {
    const steamInfo = this.getSteamInfo()
    return !steamInfo ? 'offline' : steamInfo.status
  }

  getPersonaname() {
    const steamInfo = this.getSteamInfo()
    if (steamInfo) {
      return steamInfo.personaname
    }
    return <i className="fa fa-refresh fa-spin" />
  }

  render() {
    let classes = cx(
      this.props.size,
      { 'steamavatar': true
      , 'online': this.getStatus() === 'online'
      , 'offline': this.getStatus() === 'offline'
      , 'in-game': this.getStatus() === 'in-game'
      })
    const body = <img className={classes} src={this.getAvatarURL()} />
    if (!this.props.noLink)
      return (
        <div>
          <a href={this.makeURL()} onClick={this.onClick}>
            {body}
          </a>
          <span> </span>
          {this.props.showName ? this.getPersonaname() : null}
        </div>
      )
    return body
  }
}


SteamAvatar.propTypes =
{ steamID: P.string
, steamID64: P.string
, size: P.oneOf(['tiny', 'mini', 'small', 'medium', 'mediumlarge', 'large'])
, queueAvatar: P.func.isRequired
, showName: P.bool
}


function mapStateToProps(state) {
  const {avatars} = state
  const {data} = avatars.toJS()
  return {avatars: data}
}


export default connect(
  mapStateToProps,
  {queueAvatar}
)(SteamAvatar)
