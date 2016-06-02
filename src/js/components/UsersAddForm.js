import React, {PropTypes as P} from 'react'


import {FormGroup, FormControl, Button, Checkbox} from 'react-bootstrap'


export default class UsersAddForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {value: '', superuser: false}
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.adding && !nextProps.adding && !nextProps.addingError) {
      this.setState({value: '', superuser: false})
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

  render() {
    const {adding, addingError} = this.props
    return (
      <div>
        <div className="form-inline">
          <FormControl
            placeholder="Enter Community URL"
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
          <Button
            bsStyle="primary"
            onClick={() => this.handleAdd()}
            disabled={adding}
            >
            <i className="fa fa-fw fa-plus" /> Add User
          </Button>
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
