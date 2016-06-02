import React, {PropTypes as P} from 'react'
import MediaTypes from '../constants/MediaTypes'


import {FormControl, Button} from 'react-bootstrap'


export default class LevelMediaNewForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {value: '', mediaType: '0'}
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.adding && !nextProps.adding && !nextProps.addingError) {
      this.setState({value: '', mediaType: '0'})
    }
  }

  handleAdd() {
    this.props.addMedia(this.props.levelID, this.state.mediaType,
                        this.state.value.trim())
  }

  onInputChange(event) {
    this.setState({value: event.target.value})
  }

  onInputKeyUp(event) {
    if (event.key === 'Enter') {
      this.handleAdd()
    }
  }

  onSelectChange(event) {
    this.setState({mediaType: event.target.value})
  }

  render() {
    const {adding, addingError} = this.props
    return (
      <div>
        <div className="form-inline">
          <FormControl
            componentClass="select"
            value={this.state.mediaType}
            onChange={(e) => this.onSelectChange(e)}
            >
            {MediaTypes.entrySeq().map((item, idx) => {
              const [key, value] = item
              return (
                <option value={key} key={idx}>
                  {value}
                </option>
              )
            })}
          </FormControl>
          <span> </span>
          <FormControl
            placeholder="Media URL"
            value={this.state.value}
            onChange={(e) => this.onInputChange(e)}
            onKeyUp={(e) => this.onInputKeyUp(e)}
            />
          <span> </span>
          <Button
            bsStyle="primary"
            onClick={() => this.handleAdd()}
            disabled={adding}
            >
            <i className="fa fa-fw fa-plus" /> Add
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


LevelMediaNewForm.propTypes =
  { addMedia: P.func.isRequired
  , adding: P.bool.isRequired
  , addingError: P.string
  }
