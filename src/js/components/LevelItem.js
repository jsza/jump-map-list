import React, {PropTypes as P} from 'react'
import IP from 'react-immutable-proptypes'
import {JUMP_CLASSES} from '../constants/TFClasses'

import LevelTierSelect from './LevelTierSelect'
import LevelAuthor from './LevelAuthor'


export default class LevelItem extends React.Component {
  onClickDelete(event) {
    event.preventDefault()
    if (window.confirm('Delete "' + this.props.data.name + '"?')) {
      this.props.deleteLevel(this.props.data.id)
    }
  }

  render() {
    const {id, name, author_count, author_name, class_tiers} = this.props.data
    return (
      <tr>
        <td>
          {name}
        </td>
        <td>
          <LevelAuthor
            id={id}
            name={name}
            author_count={author_count}
            author_name={author_name}
            />
        </td>
        {JUMP_CLASSES.map((tfClass, idx) =>
          <td>
            <LevelTierSelect
              key={idx}
              tier={class_tiers.getIn([tfClass.toString(), 'tier'])}
              tfClass={tfClass}
              updateLevel={this.props.updateLevel}
              updating={this.props.updating}
              id={id}
              />
          </td>
        )}
        <td>
          <input className="form-control small-input" />
        </td>
        <td>
          <a
            className="pull-right"
            href="#"
            onClick={this.onClickDelete.bind(this)}>
            <i className="fa fa-remove" />
          </a>
        </td>
      </tr>
    )
  }
}


LevelItem.propTypes =
  { data: IP.record.isRequired
  , updateLevel: P.func.isRequired
  , deleteLevel: P.func.isRequired
  }
