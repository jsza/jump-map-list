import React, {PropTypes as P} from 'react'
import {connect} from 'react-redux'
import {loadLevelAuthors, addLevelAuthor, removeLevelAuthor,
        loadLevels} from '../redux/levels'
import {loadAuthors, addAuthor} from '../redux/authors'

import {Modal, Button, Row, Col} from 'react-bootstrap'
import LevelAuthorList from './LevelAuthorList'
import LevelAuthorSearch from './LevelAuthorSearch'
import AuthorNewForm from './AuthorNewForm'


class LevelAuthor extends React.Component {
  constructor(props) {
    super(props)
    this.state = {show: false}
  }

  onShow(event) {
    event.preventDefault()
    this.setState({show: true})
    this.props.loadLevelAuthors(this.props.id)
    this.props.loadAuthors()
  }

  hide() {
    this.setState({show: false})
    this.props.loadLevels()
  }

  renderAuthor() {
    const {author_count, author_name} = this.props
    if (author_count === 0) {
      return <i>Not Set</i>
    }
    else if (author_count === 1) {
      return author_name
    }
    else {
      return <i>Multiple</i>
    }
  }

  renderModal() {
    if (!this.state.show) {
      return null
    }
    const {authors, levelAuthors} = this.props
    let {data} = levelAuthors
    let searchData = authors.data
    if (data) {
      data = data.valueSeq().toList()
    }
    if (searchData) {
      searchData = searchData.valueSeq().toList()
    }
    let filterSearch = searchData
    if (data && searchData) {
      const addedIDs = data.map((i) => i.get('author_id'))
      filterSearch = filterSearch.filter((item) => {
        return !addedIDs.contains(item.get('id'))
      })
    }

    return (
      <Modal show={true} onHide={this.hide.bind(this)}>
        <Modal.Header closeButton>
          <Modal.Title>
            Modify authors for <strong>{this.props.name}</strong>
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <LevelAuthorSearch loadAuthors={this.props.loadAuthors} />
          <Row>
            <Col xs={6}>
              <LevelAuthorList
                id={this.props.id}
                data={data}
                icon="minus"
                onSelect={this.props.removeLevelAuthor}
                />
            </Col>
            <Col xs={6}>
              <LevelAuthorList
                id={this.props.id}
                data={filterSearch}
                icon="plus"
                onSelect={this.props.addLevelAuthor}
                />
            </Col>
          </Row>
          <AuthorNewForm
            addAuthor={this.props.addAuthor}
            {...authors.toObject()}
            />
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
        <span>
          {this.renderAuthor()} &bull; <a href="#" onClick={this.onShow.bind(this)}>modify</a>
        </span>
        {this.renderModal()}
      </div>
    )
  }
}


function mapStateToProps(state) {
  const levelAuthors = state.levels.authors
  const authors = state.authors
  return (
    { levelAuthors: levelAuthors.toObject()
    , authors: authors
    })
}


export default connect(
  mapStateToProps,
  {loadLevelAuthors, loadAuthors, addLevelAuthor, removeLevelAuthor,
   loadLevels, addAuthor}
)(LevelAuthor)
