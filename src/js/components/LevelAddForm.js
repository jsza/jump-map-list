import React, {PropTypes as P} from 'react'
import classnames from 'classnames'

import {Button, FormGroup, FormControl} from 'react-bootstrap'


export default class LevelAddForm extends React.Component {
  constructor(props) {
    super(props)
    this.state =
      { value: ''
      , success: false
      }
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.adding && !nextProps.adding && !nextProps.addingError) {
      this.setState({value: '', success: true})
    }
    else {
      this.setState({success: false})
    }
  }

  onClickAdd() {
    if (this.state.value.length === 0) {
      return
    }
    this.props.addLevel(this.state.value)
  }

  onInputKeyUp(event) {
    if (event.key === 'Enter') {
      this.onClickAdd()
    }
  }

  renderButton() {
    const {adding} = this.props
    const iconClasses = classnames(
      { 'fa': true
      , 'fa-plus': !adding
      , 'fa-cog fa-spin': adding
      })
    let buttonStyle = 'primary'
    if (this.state.success) {
      buttonStyle = 'success'
    }
    else if (this.props.addingError) {
      buttonStyle = 'danger'
    }
    return (
      <Button
        bsStyle={buttonStyle}
        onClick={this.onClickAdd.bind(this)}
        disabled={adding || !this.state.value.length}>
        <i className={iconClasses} /> Add map
      </Button>
    )
  }

  render() {
    const {addingError} = this.props
    return (
      <div className="form-inline">
        <FormGroup>
          <FormControl
            placeholder="Enter map name"
            value={this.state.value}
            onChange={(e) => this.setState({value: e.target.value})}
            onKeyUp={this.onInputKeyUp.bind(this)}
          />
        </FormGroup>
        <span> </span>
        {this.renderButton()}
        {addingError
        ? <p className="text-danger">
            {addingError}
          </p>
        : null}
      </div>
    )
  }
}


LevelAddForm.propTypes =
  { adding: P.bool.isRequired
  , addingError: P.string
  , addLevel: P.func.isRequired
  }
