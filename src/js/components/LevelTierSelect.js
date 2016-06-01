import React, {PropTypes as P} from 'react'
import Difficulties from '../constants/Difficulties'

import {FormControl} from 'react-bootstrap'


export default class LevelTierSelect extends React.Component {
  onChange(event) {
    this.props.updateLevel(this.props.id, this.props.tfClass,
                           parseInt(event.target.value))
  }

  render() {
    return (
      <FormControl
        className="small-input"
        componentClass="select"
        disabled={this.props.updating}
        value={this.props.tier}
        onChange={this.onChange.bind(this)}
        >
        {Difficulties.entrySeq().map((item, idx) => {
          const [key, value] = item
          return <option key={idx} value={key}>{`(${key}) ${value}`}</option>
        })}}
      </FormControl>
    )
  }
}


LevelTierSelect.propTypes =
  { tier: P.number.isRequired
  , updating: P.bool.isRequired
  , tfClass: P.number.isRequired
  , updateLevel: P.func.isRequired
  }
