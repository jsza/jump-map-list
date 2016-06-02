import React, {PropTypes as P} from 'react'
import classnames from 'classnames'


import {FormGroup, FormControl, Button, Checkbox} from 'react-bootstrap'


export default class UsersAddForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {value: '', superuser: false, success: false}
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.adding && !nextProps.adding && !nextProps.addingError) {
      this.setState({value: '', superuser: false, success: true})
    }
    else {
      this.setState({success: false})
    }
  }

  handleAdd() {
    this.props.addUser(this.state.value.trim(), this.state.superuser)
  }

  onInputChange(event) {
    this.setState({value: event.target.value})
  }

  onInputKeyUp(event) {
    if (event.key === 'Enter') {
      this.handleAdd()
    }
  }

  onCheckboxChange(event) {
    this.setState({superuser: event.target.checked})
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
        onClick={() => this.handleAdd()}
        disabled={adding || !this.state.value.length}
        >
        <i className={iconClasses} /> Add User
      </Button>
    )
  }

  render() {
    const {addingError} = this.props
    return (
      <div>
        <div className="form-inline">
          <FormControl
            placeholder="Steam Community URL"
            value={this.state.value}
            onChange={(e) => this.onInputChange(e)}
            onKeyUp={(e) => this.onInputKeyUp(e)}
            />
          <span> </span>
          <Checkbox
            checked={this.state.superuser}
            readOnly
            onChange={this.onCheckboxChange.bind(this)}
            >
            Superuser
          </Checkbox>
          <span> </span>
          {this.renderButton()}
        </div>
        {addingError
        ? <p className="text-danger">
            Error adding: {addingError}
          </p>
        : null}
      </div>
    )
  }
}


UsersAddForm.propTypes =
  { addUser: P.func.isRequired
  , adding: P.bool.isRequired
  , addingError: P.string
  }
