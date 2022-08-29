import React, { Component } from 'react';
import { FaRegUserCircle } from 'react-icons/fa';

import '../stylesheets/Header.css';

class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      score: '',
    };
  }

  componentDidUpdate() {
    const { userDetails, loggedIn } = this.props;
    if (!loggedIn) {
      return;
    }
    const { username, score } = userDetails;
    const { username: stateName, score: stateScore } = this.state;
    if (score !== stateScore || username !== stateName) {
      this.setState({ username, score });
    }
  }

  handleLogout() {
    const { setUserDetails } = this.props;
    const data = { username: '', score: '', token: '' };
    setUserDetails(data, false);
    window.history.pushState(null, '', '/');
    window.location.reload();
  }

  handleProfileClick() {
    window.history.pushState(null, '', '/profile');
    window.location.reload();
  }

  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    const { loggedIn } = this.props;
    const { username } = this.state;

    return (
      <div className='App-header'>
        <h1
          onClick={() => {
            this.navTo('');
          }}
        >
          Udacitrivia
        </h1>
        <h2
          onClick={() => {
            this.navTo('');
          }}
        >
          List
        </h2>
        <h2
          onClick={() => {
            this.navTo('/add');
          }}
        >
          Add
        </h2>
        <h2
          onClick={() => {
            this.navTo('/play');
          }}
        >
          Play
        </h2>
        {loggedIn ? (
          <h2
            onClick={() => {
              this.handleLogout();
            }}
          >
            Logout
          </h2>
        ) : (
          <div className='user'>
            <h2
              onClick={() => {
                this.navTo('/login');
              }}
            >
              Login
            </h2>
            <h2
              onClick={() => {
                this.navTo('/signup');
              }}
            >
              SignUp
            </h2>
          </div>
        )}
        {loggedIn && (
          <div className='Header-ProfileIcon' onClick={this.handleProfileClick}>
            {<FaRegUserCircle />}
            <p>{username}</p>
          </div>
        )}
      </div>
    );
  }
}

export default Header;
