import React, {PropTypes as P} from 'react'
import IP from 'react-immutable-proptypes'
import {connect} from 'react-redux'
import {loadUsers, addUser, deleteUser} from '../redux/users'

import {Table, Row, Col} from 'react-bootstrap'
import TimeAgo from 'react-timeago'
import Throbber from '../components/Throbber'
import UsersAddForm from '../components/UsersAddForm'
import SteamAvatarContainer from './SteamAvatarContainer'
import SteamDisplayName from './SteamDisplayName'


class UsersApp extends React.Component {
  componentDidMount() {
    this.props.loadUsers()
  }

  onClickDelete(event, id) {
    event.preventDefault()
    if (window.confirm('Delete user?')) {
      this.props.deleteUser(id)
    }
  }

  render() {
    const {fetching, fetchingError, adding, addingError, deletingError,
           data} = this.props
    let errorContent
    if (deletingError) {
      errorContent = (
        <p className="text-danger">
          Error deleting: {deletingError}
        </p>
      )
    }

    let content
    if (fetchingError) {
      content = (
        <p className="text-danger">
          Error loading: {fetchingError}
        </p>
      )
    }
    else if (fetching || !data) {
      content = <Throbber />
    }
    else {
      content = (
        <Row className="users-app">
          <Col lg={6}>
            <Table condensed striped hover>
              <thead>
                <tr>
                  <th>User</th>
                  <th>Superuser</th>
                  <th>Added By</th>
                  <th>Date</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {this.props.data.valueSeq().map((item, idx) => {
                  const steamID = item.get('steamid')
                  const adderSteamID = item.get('adder_steamid')
                  return (
                    <tr key={idx}>
                      <td>
                        <SteamAvatarContainer
                          steamID64={steamID}
                          size="tiny"
                          showName={true} />
                      </td>
                      <td>
                        <b>{item.get('superuser').toString()}</b>
                      </td>
                      <td>
                        {adderSteamID
                        ? <SteamAvatarContainer
                            steamID64={adderSteamID}
                            size="tiny"
                            showName={true} />
                        : 'Command-line'
                        }
                      </td>
                      <td>
                        <TimeAgo date={item.get('timestamp') * 1000} />
                      </td>
                      <td>
                        <a
                          className="pull-right"
                          href="#"
                          onClick={(e) => this.onClickDelete(e, item.get('id'))}
                          >
                          Delete
                        </a>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </Table>
            {errorContent}
            <UsersAddForm
              adding={adding}
              addingError={addingError}
              addUser={this.props.addUser} />
          </Col>
        </Row>
      )
    }
    return (
      <div className="container-fluid">
        <h1 className="page-title">Users</h1>
        {content}
      </div>
    )
  }
}


UsersApp.propTypes =
  { fetching: P.bool.isRequired
  , fetchingEerror: P.string
  , data: IP.orderedMap
  , adding: P.bool.isRequired
  , addingEerror: P.string
  , deleting: P.bool.isRequired
  , deletingEerror: P.string
  }


function mapStateToProps(state) {
  const {users} = state
  return users.toObject()
}


export default connect(
  mapStateToProps,
  {loadUsers, addUser, deleteUser}
)(UsersApp)
