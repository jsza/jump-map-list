import React, {PropTypes as P} from 'react'


import {FormGroup, FormControl, Button} from 'react-bootstrap'


export default class UsersAddForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {value: ''}
  }

  handleAdd() {
    this.props.addUser(this.state.value.trim())
  }

  onInputChange(event) {
    this.setState({value: event.target.value})
  }

  onInputKeyUp(event) {
    if (event.key === 'Enter') {
      this.handleAdd()
    }
  }

  render() {
    const {addingError} = this.props
    const val = this.state.value.trim()
    const valid = (val.length === 0 ? true : /^\d+$/.test(val))
    return (
      <div>
        <div className="form-inline">
          <FormGroup>
            <FormControl
              placeholder="64-bit steamID"
              value={this.state.value}
              onChange={(e) => this.onInputChange(e)}
              onKeyUp={(e) => this.onInputKeyUp(e)}
              />
          </FormGroup>
          <span> </span>
          <Button
            bsStyle="primary"
            onClick={() => this.handleAdd()}
            disabled={!valid}
            >
            <i className="fa fa-fw fa-plus" /> Add User
          </Button>
          {valid
          ? null
          : <span className="text-danger"> SteamID must only consist of numbers.</span>}
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
  , addingError: P.string
  }
