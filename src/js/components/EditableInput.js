import React from 'react'
import ReactDOM from 'react-dom'

import {FormControl} from 'react-bootstrap'


export default class EditableInput extends React.Component {
  constructor(props) {
    super(props)
    this.state =
      { editing: false
      , value: ''
      }
  }

  onInputChange(e) {
    this.setState({value: e.target.value})
  }

  onClickEdit(e) {
    e.preventDefault()
    this.setState(
      { editing: true
      , value: this.props.value
      })

    window.setTimeout(this.focusInput.bind(this), 0)
  }

  focusInput() {
    ReactDOM.findDOMNode(this.refs.input).focus()
  }

  stopEditing() {
    this.setState({editing: false})
  }

  render() {

    return (
      <span>
        <span hidden={this.state.editing}>
          {this.props.value}
          <span> &bull; </span>
          <a href="#" onClick={this.onClickEdit.bind(this)}>
            edit
          </a>
        </span>
        <FormControl
          ref="input"
          className="small-input"
          value={this.state.value}
          style={{width: 'auto', display: this.state.editing ? 'inline' : 'none'}}
          onChange={this.onInputChange}
          onBlur={this.stopEditing.bind(this)}
          />
      </span>
    )
  }
}
