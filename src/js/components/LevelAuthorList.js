import React, {PropTypes as P} from 'react'
import IP from 'react-immutable-proptypes'

import Throbber from './Throbber'
import SteamAvatarContainer from '../containers/SteamAvatarContainer'


export default class LevelAuthorList extends React.Component {
  onSelect(author, event) {
    event.preventDefault()
    this.props.onSelect(this.props.id, author.toJS())
  }

  render() {
    const {data, icon} = this.props
    if (!data) {
      return <Throbber />
    }
    return (
      <div className="extra-maps-author-list list-group">
        {data.map((a, idx) =>
          <a key={idx} className="list-group-item level-author-item" href="#" onClick={this.onSelect.bind(this, a)}>
            <i className={`fa fa-${icon}`} /> <SteamAvatarContainer steamID64={a.get('steamid')} size="tiny" /> {a.get('name')}
          </a>
        )}
      </div>
    )
  }
}


LevelAuthorList.propTypes =
  { data: IP.list
  , icon: P.string.isRequired
  }
