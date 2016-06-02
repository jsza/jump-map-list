import React, {PropTypes as P} from 'react'
import classnames from 'classnames'

import {Button, FormGroup, FormControl} from 'react-bootstrap'


export default class AuthorNewForm extends React.Component {
  constructor(props) {
    super(props)
    this.state =
      { nameValue: ''
      , urlValue: ''
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
    this.props.addAuthor(this.state.nameValue, this.state.urlValue)
  }

  onInputKeyUp(event) {
    if (event.key === 'Enter') {
      this.onClickAdd()
    }
  }

  renderButton() {
    const {adding} = this.props
    const {nameValue, urlValue} = this.state
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
        disabled={adding || nameValue.length === 0 || urlValue.length === 0}>
        <i className={iconClasses} /> New author
      </Button>
    )
  }

  render() {
    const {addingError} = this.props
    return (
      <div className="form-inline">
        <FormControl
          placeholder="Name"
          value={this.state.nameValue}
          onChange={(e) => this.setState({nameValue: e.target.value})}
          onKeyUp={this.onInputKeyUp.bind(this)}
        />
        <span> </span>
        <FormControl
          placeholder="Steam Community URL"
          value={this.state.urlValue}
          onChange={(e) => this.setState({urlValue: e.target.value})}
          onKeyUp={this.onInputKeyUp.bind(this)}
        />
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


AuthorNewForm.propTypes =
  { adding: P.bool.isRequired
  , addingError: P.string
  , addAuthor: P.func.isRequired
  }
