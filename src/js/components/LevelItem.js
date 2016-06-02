import React, {PropTypes as P} from 'react'
import {JUMP_CLASSES} from '../constants/TFClasses'

import LevelTierSelect from './LevelTierSelect'
import LevelAuthor from './LevelAuthor'
import LevelMediaApp from '../containers/LevelMediaApp'


export default class LevelItem extends React.Component {
  onClickDelete(event) {
    event.preventDefault()
    if (window.confirm('Delete "' + this.props.data.name + '"?')) {
      this.props.deleteLevel(this.props.data.id)
    }
  }

  render() {
    const {id, name, author_count, author_name, class_tiers,
           media_counts} = this.props.data
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
          <td key={idx}>
            <LevelTierSelect
              tier={class_tiers.getIn([tfClass.toString(), 'tier'], -1)}
              tfClass={tfClass}
              updateLevel={this.props.updateLevel}
              updating={this.props.updating}
              id={id}
              />
          </td>
        )}
        <td>
          <LevelMediaApp
            levelID={id}
            name={name}
            mediaCounts={media_counts}
            />
        </td>
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
  { data: P.object.isRequired
  , updateLevel: P.func.isRequired
  , deleteLevel: P.func.isRequired
  }
