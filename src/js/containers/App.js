import React from 'react'
import {Link} from 'react-router'
import {LinkContainer} from 'react-router-bootstrap'

import {Navbar, Nav, NavItem} from 'react-bootstrap'


export default class App extends React.Component {
  render() {
    return (
      <div>
        <Navbar id="navbar-main" fixedTop fluid>
          <Navbar.Header>
            <Navbar.Brand>
              <Link to="/" className="navbar-brand">
                jump.tf map list
              </Link>
            </Navbar.Brand>
            <Navbar.Toggle />
          </Navbar.Header>

          <Navbar.Collapse>
            <Nav navbar eventKey={0} className="main-nav-items">
              <LinkContainer to="/authors">
                <NavItem>
                  <i className="fa fa-user" /> Authors
                </NavItem>
              </LinkContainer>
              <LinkContainer to="/users">
                <NavItem>
                  <i className="fa fa-user-secret" /> Users
                </NavItem>
              </LinkContainer>
            </Nav>

            <Nav pullRight>
              <li>
                <a href="/logout" className="pull-right">Sign out</a>
              </li>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        {this.props.children}
      </div>
    )
  }
}
