import React, {PropTypes as P} from 'react'
import {connect} from 'react-redux'
import steam from 'steamidconvert'

import {queueAvatar} from '../redux/avatars'


const Steam = steam()


class SteamDisplayName extends React.Component {
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

  getPersonaname() {
    const steamInfo = this.getSteamInfo()
    if (steamInfo) {
      return steamInfo.personaname
    }
    return null
  }

  render() {
    const personaname = this.getPersonaname()
    return (
      <span>
        { personaname
          ? personaname
          : <i className="fa fa-refresh fa-spin" />
        }
      </span>
    )
  }
}


SteamDisplayName.propTypes =
{ steamID: P.string
, steamID64: P.string
, queueAvatar: P.func.isRequired
}


function mapStateToProps(state) {
  const {avatars} = state
  const {data} = avatars.toJS()
  return {avatars: data}
}


export default connect(
  mapStateToProps,
  {queueAvatar}
)(SteamDisplayName)
