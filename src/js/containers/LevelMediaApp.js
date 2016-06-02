import React, {PropTypes as P} from 'react'
import IP from 'react-immutable-proptypes'
import {connect} from 'react-redux'
import {loadMedia, addMedia, deleteMedia, moveMediaUp,
        moveMediaDown} from '../redux/media'
import {loadLevels} from '../redux/levels'

import {Badge, Modal, Button} from 'react-bootstrap'
import Throbber from '../components/Throbber'
import LevelMediaItem from '../components/LevelMediaItem'
import LevelMediaNewForm from '../components/LevelMediaNewForm'


class LevelMediaApp extends React.Component {
  constructor(props) {
    super(props)
    this.state = {show: false}
  }

  renderBadge() {
    const mc = this.props.mediaCounts
    return (
      <Badge className="level-media-badge" onClick={this.onShow.bind(this)}>
        <i className="fa fa-picture-o" /> {mc.get('0', 0)} <i className="fa fa-youtube fa-1.5x" /> {mc.get('1', 0)}
      </Badge>
    )
  }

  onShow(event) {
    event.preventDefault()
    this.setState({show: true})
    this.props.loadMedia(this.props.levelID)
  }

  hide() {
    this.setState({show: false})
    this.props.loadLevels()
  }

  renderModal() {
    if (!this.state.show) {
      return null
    }
    let {data} = this.props
    let body
    if (!data) {
      body = <Throbber />
    }
    else {
      body = (
        <div>
          <div className="list-group level-media-list">
            {data.valueSeq().map((item, idx) =>
              <LevelMediaItem
                key={item.get('id')}
                first={idx === 0}
                last={idx === (data.size-1)}
                data={item.toJS()}
                deleteMedia={this.props.deleteMedia}
                moveMediaUp={this.props.moveMediaUp}
                moveMediaDown={this.props.moveMediaDown}
                />
            )}
          </div>
          <hr />
          <LevelMediaNewForm
            addMedia={this.props.addMedia}
            levelID={this.props.levelID}
            />
        </div>
      )
    }

    return (
      <Modal show={true} onHide={this.hide.bind(this)}>
        <Modal.Header closeButton>
          <Modal.Title>
            Add/remove media for <strong>{this.props.name}</strong>
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {body}
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={this.hide.bind(this)}>Close</Button>
        </Modal.Footer>
      </Modal>
    )
  }

  render() {
    return (
      <div>
        {this.renderBadge()}
        {this.renderModal()}
      </div>
    )
  }
}


LevelMediaApp.propTypes =
  { levelID: P.number.isRequired
  , fetching: P.bool.isRequired
  , fetchingError: P.string
  , data: IP.orderedMap
  , deleting: P.bool.isRequired
  , deletingError: P.string
  }


function mapStateToProps(state) {
  const {media} = state
  return media.toObject()
}


export default connect(
  mapStateToProps,
  {loadMedia, addMedia, deleteMedia, loadLevels, moveMediaUp, moveMediaDown}
)(LevelMediaApp)
