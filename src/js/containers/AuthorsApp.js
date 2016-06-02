import React, {PropTypes as P} from 'react'
import IP from 'react-immutable-proptypes'
import {connect} from 'react-redux'
import {loadAuthors, addAuthor, deleteAuthor} from '../redux/authors'

import {Table, Row, Col, FormControl, FormGroup} from 'react-bootstrap'
import TimeAgo from 'react-timeago'
import Throbber from '../components/Throbber'
import SteamAvatarContainer from './SteamAvatarContainer'
import SteamDisplayName from './SteamDisplayName'
import AuthorNewForm from '../components/AuthorNewForm'
import EditableInput from '../components/EditableInput'


class AuthorsApp extends React.Component {
  componentDidMount() {
    this.props.loadAuthors()
  }

  onClickDelete(event, id) {
    event.preventDefault()
    if (window.confirm('Delete author?')) {
      this.props.deleteAuthor(id)
    }
  }

  render() {
    const {fetching, fetchingError, data, adding, addingError} = this.props

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
                  <th>Author</th>
                  <th>Date added</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {this.props.data.valueSeq().map((item, idx) => {
                  return (
                    <tr key={idx}>
                      <td>
                        <SteamAvatarContainer steamID64={item.get('steamid')} size="tiny" />
                        <span> </span>
                        <EditableInput
                          value={item.get('name')}
                          onSave={() => console.log('didit!')} />
                      </td>
                      <td width="200">
                        <TimeAgo date={item.get('timestamp') * 1000} />
                      </td>
                      <td>
                        <span className="pull-right">
                          <a href="#" onClick={(e) => this.onClickDelete(e, item.get('id'))}>
                            Delete
                          </a>
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </Table>
            <AuthorNewForm
              adding={adding}
              addingError={addingError}
              addAuthor={this.props.addAuthor}
              />
          </Col>
        </Row>
      )
    }
    return (
      <div className="container-fluid">
        <h1 className="page-title">Authors</h1>
        {content}
      </div>
    )
  }
}


AuthorsApp.propTypes =
  { fetching: P.bool.isRequired
  , fetchingEerror: P.string
  , data: IP.orderedMap
  , deleteAuthor: P.func.isRequired
  }


function mapStateToProps(state) {
  const {authors} = state
  return authors.toObject()
}


export default connect(
  mapStateToProps,
  {loadAuthors, addAuthor, deleteAuthor}
)(AuthorsApp)
