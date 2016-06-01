import React, {PropTypes as P} from 'react'
import IP from 'react-immutable-proptypes'
import {connect} from 'react-redux'
import {loadLevels, addLevel, updateLevel, deleteLevel,
        dismissLastDelete, undoLastDelete} from '../redux/levels'

import {Table} from 'react-bootstrap'
import Throbber from '../components/Throbber'
import LevelAddForm from '../components/LevelAddForm'
import LevelItem from '../components/LevelItem'
import LevelDeleteAlert from '../components/LevelDeleteAlert'


class LevelsApp extends React.Component {
  componentDidMount() {
    this.props.loadLevels()
  }

  render() {
    const {fetching, fetchingError, data} = this.props
    let content
    if (fetchingError) {
      content = (
        <p className="text-danger">
          {fetchingError}
        </p>
      )
    }
    else if (fetching || !data) {
      content = <Throbber />
    }
    else {
      content = (
        <div className="extra-maps-app">
          <Table condensed striped hover>
            <thead>
              <tr>
                <th>Name</th>
                <th>Author</th>
                <th>Soldier Tier</th>
                <th>Demoman Tier</th>
                <th>URL</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {this.props.data.valueSeq().map((item, idx) =>
                <LevelItem
                  key={idx}
                  data={item.toObject()}
                  updateLevel={this.props.updateLevel}
                  deleteLevel={this.props.deleteLevel}
                  updating={this.props.updating}
                  />
              )}
            </tbody>
          </Table>
          <LevelAddForm
            addLevel={this.props.addLevel}
            adding={this.props.adding}
            addingError={this.props.addingError} />
        </div>
      )
    }
    return (
      <div className="container-fluid">
        <a href="/logout" className="pull-right">Sign out</a>
        <h1 className="page-title">jump.tf Maps</h1>
        <LevelDeleteAlert
          lastDelete={this.props.lastDelete}
          onDismiss={this.props.dismissLastDelete}
          undoLastDelete={this.props.undoLastDelete}
          />
        {content}
      </div>
    )
  }
}


LevelsApp.propTypes =
  { fetching: P.bool.isRequired
  , fetchingError: P.string
  , data: IP.orderedMap
  , updating: P.bool.isRequired
  , updatingError: P.string
  , deleting: P.bool.isRequired
  , deletingError: P.string
  }


function mapStateToProps(state) {
  const {levels} = state
  return levels.toObject()
}


export default connect(
  mapStateToProps,
  {loadLevels, addLevel, updateLevel, deleteLevel,
   dismissLastDelete, undoLastDelete}
)(LevelsApp)
